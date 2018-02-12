from django.shortcuts import render
from django.http import HttpResponse

from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from os import linesep, path
import json

def index(request):
    USERNAME = PASSWORD = ''
    dir_path = path.dirname(path.realpath(__file__))
    with open(path.join(dir_path, '.ibmwcred'), 'r') as configfile:
        data = configfile.read().split(linesep)
        USERNAME = data[0].split()[1]
        PASSWORD = data[1].split()[1]    
    language_translator = LanguageTranslator(
        username=USERNAME,
        password=PASSWORD)
    #translation = language_translator.list_identifiable_languages()
    translation = language_translator.translate(
        text='Hello',
        model_id='en-ja')
    #lang = language_translator.identify('Hello')['languages'][0]['language']
    #return HttpResponse(str(lang))
    return HttpResponse(translation['translations'][0]['translation'])

def translate(request, text):
    #text = request.GET.get('text', '').decode('utf-8')
    #text = 'a'
    USERNAME = PASSWORD = ''
    dir_path = path.dirname(path.realpath(__file__))
    with open(path.join(dir_path, '.ibmwcred'), 'r') as configfile:
        data = configfile.read().split(linesep)
        USERNAME = data[0].split()[1]
        PASSWORD = data[1].split()[1]    
    language_translator = LanguageTranslator(
        username=USERNAME,
        password=PASSWORD)
    language = language_translator.identify('Hello')['languages'][0]['language']

    translation = language_translator.translate(
        text=text.replace('+', ' '),
        #model_id='en-'+language)
        model_id=str(language) + '-ja')
    return HttpResponse(translation['translations'][0]['translation'])