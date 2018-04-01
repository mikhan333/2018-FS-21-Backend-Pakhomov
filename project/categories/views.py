# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, reverse
from .models import Category
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
    questions = category.questions.all().filter(is_archive=False)


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







def category_list(request):
    categories = Category.objects.all()

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
    }
    return render(request, 'categories/category_list.html', context)
