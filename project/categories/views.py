# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, reverse
from .models import Category
from django.db import models
from django import forms
from django.views.generic import ListView

class CategoriesListForm(forms.Form):
    sort = forms.ChoiceField(choices=(
        ('name', 'Name asc'),
        ('-name', 'Name desc'),
        ('id', 'ID'),
    ), required=False)
    search = forms.CharField(required=False)


def category_detail(request, pk=None):
    category = Category.objects.get(id=pk)
    questions = category.questions.all().filter(is_archive=False).select_related('author')

    form = CategoriesListForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            questions = questions.order_by(data['sort'])
        if data['search']:
            questions = questions.filter(name__icontains=data['search'])

    context={
        'category': category,
        'questions': questions,
        'category_questions_form': form
    }

    return render(request, 'categories/category_detail.html', context)



class CategoryList(ListView):
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    model = Category

    def get_queryset(self):

        q=super(CategoryList, self).get_queryset()
        self.form=CategoriesListForm(self.request.GET)

        if self.form.is_valid():
            if self.form.cleaned_data['sort']:
                q = q.order_by(self.form.cleaned_data['sort'])
            if self.form.cleaned_data['search']:
                q=q.filter(title=self.form.cleaned_data['search'])
        return q.annotate(questions_count = models.Count('questions__id', distinct=True),
                          answers_count = models.Count('questions__answers__id', distinct=True),
                          likes_count = models.Count('questions__likes', distinct=True))

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['categories_form']=self.form
        return context


'''
def category_list(request):
    categories = Category.objects.all()
   # dop = Category.objects.all().annotate(question_count=models.Count('questions'))
   # , answer_count = models.Count('questions__answers__id')
    form = CategoriesListForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            categories = categories.order_by(data['sort'])
        if data['search']:
            categories = categories.filter(name__icontains=data['search'])

    context = {
        'categories': categories,
        'categories_form': form,
   #     'dop': dop,
    }
    return render(request, 'categories/category_list.html', context)
'''