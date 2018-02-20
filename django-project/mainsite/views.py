from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from os import linesep, path
from random import SystemRandom
from json import loads
import urllib.parse
import oauth2 as oauth
import urllib
import string
import time
import hashlib
import hmac
import base64
import math
import random
import sys

from .models import twitterer

def index(request):
    return render(request, 'mainsite/index.html')

def sign(request):
    #Server Links
    REQUEST_URL = "https://api.twitter.com/oauth/request_token";
    ACCESS_URL = "https://api.twitter.com/oauth/access_token";
    AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize";

    #Consumer keys
    dir_path = path.dirname(path.realpath(__file__))
    with open(path.join(dir_path, '.twapicred'), 'r') as TweetCred:
        creds = TweetCred.read().split(linesep)
    TOKEN = creds[0].split()[1]
    callback_url = urllib.parse.quote(creds[1].split()[1], '')
    TOKEN_SECRET = creds[2].split()[1]

    #Access keys
    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""

    HEADER_TITLE = "Authorization"

    #Consumer key
    HEADER = 'OAuth oauth_callback="%s", oauth_consumer_key="' % callback_url + TOKEN + '", '

    #Nonce
    HEADER += 'oauth_nonce="'
    NONCE = ""
    for i in range(32):
        NONCE += chr(random.randint(97, 122))
    HEADER += NONCE
    HEADER += '", '

    #Timestamp
    TIMESTAMP = str(int(time.time()))

    #Signature
    HEADER += 'oauth_signature="'
    PARAMETER_STRING = "oauth_callback=" + callback_url + "&oauth_consumer_key=" + TOKEN + "&oauth_nonce=" + NONCE + "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + TIMESTAMP + "&oauth_version=1.0"
    BASE_STRING = 'POST&' + urllib.parse.quote(REQUEST_URL, '') + '&' + urllib.parse.quote(PARAMETER_STRING, '')
    SIGNING_KEY = urllib.parse.quote(TOKEN_SECRET, '') + '&'
    print("DEBUG : SIGNING KEY " + SIGNING_KEY + " BASE STRING " + BASE_STRING + "\n")
    HEADER += urllib.parse.quote(base64.standard_b64encode(hmac.new(SIGNING_KEY.encode(), BASE_STRING.encode(), hashlib.sha1).digest()).decode('ascii'))
    HEADER += '", '

    #Signature Method
    HEADER += 'oauth_signature_method="HMAC-SHA1", '

    #Timestamp
    HEADER += 'oauth_timestamp="' + TIMESTAMP + '", '

    #Version
    HEADER += 'oauth_version="1.0"'

    print(HEADER_TITLE + ":\n" + HEADER)

    HTTP_REQUEST = urllib.request.Request(REQUEST_URL)
    HTTP_REQUEST.add_header(HEADER_TITLE, HEADER)
    body = urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read().decode('utf-8')
    print('body: '+ body)
    params = body.split('&')

    oauth_token = params[0].split('=')[1]
    oauth_token_secret = params[1].split('=')[1]

    print('Successfully retrieved request token! Redirecting...')
    loggee = twitterer.objects.create(oauth_token=oauth_token, request_only_token=oauth_token, oauth_token_secret=oauth_token_secret)

    return HttpResponseRedirect('https://api.twitter.com/oauth/authenticate?oauth_token='+oauth_token)

def logged(request):
    dir_path = path.dirname(path.realpath(__file__))
    with open(path.join(dir_path, '.twapicred'), 'r') as TweetCred:
        creds = TweetCred.read().split(linesep)
    oauth_consumer_key = creds[0].split()[1]
    consumer_secret = creds[2].split()[1]

    verifier = request.GET.get('oauth_verifier', '')
    request_token = request.GET.get('oauth_token', '')
    user = twitterer.objects.get(request_only_token=request_token)    
    consumer = oauth.Consumer(key=oauth_consumer_key, secret=consumer_secret)
    
    if not user.logged:
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        token = oauth.Token(user.oauth_token, user.oauth_token_secret)
        token.set_verifier(verifier)
        client = oauth.Client(consumer, token)

        resp, content = client.request(access_token_url, "POST")
        print('Access response: ' + str(content))
        user.oauth_token = content.decode('utf-8').split('&')[0].split('=')[1]
        user.oauth_token_secret = content.decode('utf-8').split('&')[1].split('=')[1]
        user.twitter_id = content.decode('utf-8').split('&')[2].split('=')[1]
        user.logged = True
        user.save()

    print('Access token: ' + str(user.oauth_token))
    print('Token secret: ' + str(user.oauth_token_secret))
    print('Twitter ID: ' + str(user.twitter_id))

    get_info_url = 'https://api.twitter.com/1.1/users/show.json'
    access_token = oauth.Token(user.oauth_token, user.oauth_token_secret)
    client = oauth.Client(consumer, access_token)
    
    resp, content = client.request(get_info_url + '?user_id=' + user.twitter_id, "GET")
    user_info = loads(content.decode('utf-8'))
    bio = user_info['description'] 
    name = user_info['name']

    TRANSLATOR_URL = 'http://127.0.0.1:8000/translator/'
    resp = urllib.request.urlopen(TRANSLATOR_URL + '?text=' + urllib.parse.quote(bio, ''))
    translated_bio = resp.read()

    context = { 'name' : name, 'bio' : translated_bio.decode('utf-8')}

    return render(request, 'mainsite/translated.html', context=context)