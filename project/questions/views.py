# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from .models import Question

def question_content(request, question_id):
    question= Question.objects.get(id = question_id)
    context={}
    context['question'] = question
    return render(request, 'questions/question_content.html', context)

def question_ask(request):
    context = {}
    return render(request, 'questions/question_ask.html', context)

def question_list(request):
    context = {
        'questions': Question.objects.all()
    }
    return render(request, 'questions/question_list.html', context)