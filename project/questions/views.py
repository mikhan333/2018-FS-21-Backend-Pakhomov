# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def question_content(request, question_id):
    return HttpResponse('Это вопрос номер: {}'.format(question_id))

def question_ask(request):
    return HttpResponse('Здесь можно задать свой вопрос')

def questions(request):
    return HttpResponse('Здесь список последних вопросов')