# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Question
from django import forms
from django.views.generic import UpdateView, CreateView

def question_content(request, pk):
    question =get_object_or_404(Question, id = pk)
    context = {
        'categories': question.categories.all(),
        'question': question
    }
    return render(request, 'questions/question_content.html', context)






class QuestionCreate(CreateView):

    model = Question
    fields = 'name', 'categories', 'is_archive', 'data',
    context_object_name = 'question'
    template_name = 'questions/question_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('questions:question_content', kwargs= { 'pk': self.object.pk})


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
        return reverse('questions:question_content', kwargs= { 'pk': self.object.pk})







def question_list(request):
    context = {
        'questions': Question.objects.all()
    }
    return render(request, 'questions/question_list.html', context)

'''

class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields = 'name', 'categories', 'is_archive', 'data'

def question_create(request):
    question=Question()

    if request.method == 'GET':
        form = QuestionForm(instance=question)
        return render(request, 'questions/question_create.html', {'form' : form})

    elif request.method == 'POST':
        form=QuestionForm(request.POST, instance = question)
        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.save()
            return redirect('questions:question_content', pk = question.id)
        else:
            return render(request, 'questions/question_create.html', {'form': form})
            
            
def question_edit(request, pk = None):
    question = get_object_or_404(Question, id = pk, author = request.user)

    if request.method == 'GET':
        form = QuestionForm(instance=question)
        return render(request, 'questions/question_edit.html', {'form' : form, 'question': question })

    elif request.method == 'POST':
        form=QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('questions:question_content', pk = question.pk)
        else:
            return render(request, 'questions/question_edit.html', {'form': form, 'question': question})

'''

