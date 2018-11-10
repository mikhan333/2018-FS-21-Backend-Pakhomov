# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Question, Answer, Like
from django import forms
from django.views.generic import UpdateView, CreateView, DetailView, View
from django.core.files.base import ContentFile

from django.shortcuts import render
from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error
from django.http import JsonResponse
from django.core.serializers import serialize
import json, base64


@jsonrpc_method('api.upload_file')
def upload_file(request, file_content, file_name):
    content = base64.b64decode(file_content).decode('utf-8')
    key = generate_key(file_name)
    quest = Question.objects.all().first()

    quest.photo.save("{}/{}".format(quest.id, key), ContentFile(content.encode('utf-8')))
    return content.decode('utf8')

import base64
import hashlib

def generate_key(filename):
    h = hashlib.new('md5')
    h.update(filename.encode('utf-8'))
    return h.hexdigest()


from adjacent.utils import get_connection_parameters
from adjacent.client import Client


@jsonrpc_method('api.question_content')
def question_content(request, pk):
    question = get_object_or_404(Question, id = pk)
    answers = question.answers.all().order_by('created').select_related('author')

    answer = Answer()

    context = {
         'categories': question.categories.all(),
         'question': question,
         'answers': answers,
         'token': get_connection_parameters(request.user)['token'],
    }


    if request.method == 'GET':
        form = AnswerForm(instance=answer)
        context['form'] = form
        return render(request, 'questions/question_content.html', context)

    elif request.method == 'POST':
        answer.answers = question
        form = AnswerForm(request.POST, instance = answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.save()
            context['form'] = form

            client = Client()
            client.publish('answers_question_{}'.format(question.pk), {})
            client.send()

            return redirect('questions:question_content', pk=question.id)
        else:
            context['form'] = form
            # return JsonResponse({'categories': serialize('json', question.categories.all()),
            #                     'question': serialize('json', [question]),
            #                     'answers': serialize('json', answers)})
            return render(request, 'questions/question_content.html', context)




@jsonrpc_method('api.question_list')
def question_list(request):
    context = {
        'questions': Question.objects.all().order_by("-created").annotate_manager().filt_del(request.user),
    }

    return render(request, 'questions/question_list.html', context)



@jsonrpc_method('api.question_comments')
def question_comments(request, pk):
    question = get_object_or_404(Question, id=pk)
    answers = question.answers.all()
    # context = {
    #     'categories': serialize('json', question.categories.all()),
    #     'question':  serialize('json', [question]),
    #     'answers': serialize('json', answers.order_by('created')),
    # }
    #return JsonResponse(context)

    context = {
        'categories': question.categories.all(),
        'question': question,
        'answers': answers.order_by('created'),
    }
    return render(request, 'questions/commentsdiv.html', context)


class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields = 'name', 'data'


class QuestionCreate(CreateView):

    model = Question
    fields = 'name', 'categories', 'is_archive', 'data',
    context_object_name = 'question'
    template_name = 'questions/question_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('questions:question_content', kwargs={'pk': self.object.pk})


class QuestionEdit(UpdateView):

    model = Question
    fields = 'name', 'categories', 'is_archive', 'data',
    context_object_name = 'question'
    template_name = 'questions/question_edit.html'

    def get_queryset(self):
        queryset=super(QuestionEdit, self).get_queryset()
        queryset=queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('questions:question_content', kwargs = { 'pk': self.object.pk})

    def form_valid(self, form):
        response = super(QuestionEdit, self).form_valid(form)
        return HttpResponse("OK")


class QuestionLikeAjaxView(View):

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.question_object = get_object_or_404(Question, id=pk)
        return super(QuestionLikeAjaxView, self).dispatch(request, *args, **kwargs)

    def post(self, pk):
        if not self.question_object.likes.filter(author=self.request.user).exists():
            like = Like()
            like.questions = self.question_object
            like.author = self.request.user
            like.save()
        return HttpResponse(Like.objects.filter(questions=self.question_object).count())


