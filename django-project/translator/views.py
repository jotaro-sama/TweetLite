from django.shortcuts import render
from django.http import HttpResponse
import logging

from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from watson_developer_cloud import WatsonException
from watson_developer_cloud import WatsonApiException

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
    #return HttpResponse(translation['translations'][0]['translation'])
    return HttpResponse('Please be sure to enter text the right way.')

#For further improvement, I could write a template instead of hardcoding HTML here. 
#Not worth it now
def translate(request):
    text = request.GET.get('text', '')
    print(text)
    #text = 'a'
    #text.replace('+', ' ').replace('%3F', '?').replace('%0D%0A', '\r\n').replace('%0A', '\r\n')
    USERNAME = PASSWORD = ''
    dir_path = path.dirname(path.realpath(__file__))
    with open(path.join(dir_path, '.ibmwcred'), 'r') as configfile:
        data = configfile.read().split(linesep)
        USERNAME = data[0].split()[1]
        PASSWORD = data[1].split()[1]    
    language_translator = LanguageTranslator(
        username=USERNAME,
        password=PASSWORD)
    language = ''
    try:
        language = language_translator.identify(text)['languages'][0]['language']
        print(language)
    except WatsonApiException as err:
        language = 'en'
    except WatsonException as err:
        language = 'en'

    phrases = text.split('\n')
    rez = ''

    if language != 'en':
        try:
            for idx, phrase in enumerate(phrases):
                phrases[idx] = language_translator.translate(
                text=phrase,
                model_id=language+'-en')['translations'][0]['translation']
                print('intermediate: '+phrases[idx]+'\n')
        except WatsonApiException as err:
            rez = rez + 'Translation from recognized language not supported. Translating from english.<br>'

    for idx, phrase in enumerate(phrases):
        if idx != 0:
            rez = rez + '<br>'
        try:
            translation = language_translator.translate(
            text=phrase,
            model_id='en-ja')
            #rez = rez + '<pre>' + translation['translations'][0]['translation'] + '</pre>'
            rez = translation['translations'][0]['translation']
        except WatsonApiException as err:
            rez = rez + 'Could not translate sentence.'
    return HttpResponse(rez + '<br><small>Translation powered by IBM Watson<small>')