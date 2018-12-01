# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, reverse
from .models import Category
from django.db import models
from django import forms
from django.views.generic import ListView
from django.core.serializers import serialize
from jsonrpc import jsonrpc_method
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import UpdateView, CreateView
import json
from django.views.decorators.csrf import csrf_exempt


class CategoriesListForm(forms.Form):
    sort = forms.ChoiceField(choices=(
        ('name', 'Name asc'),
        ('-name', 'Name desc'),
        ('id', 'ID'),
    ), required=False)
    search = forms.CharField(required=False)


@jsonrpc_method('api.category_detail')
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

    context = {
        'category': category,
        'questions': questions,
        'category_questions_form': form,
    }
    # return json.loads(serialize('json', [context['category']]))
    return render(request, 'categories/category_detail.html', context)


def category_list_front(request):
    categories = Category.objects.all()
    context = {
       'categories': serialize('json', categories),
    }
    return JsonResponse(context)


class CategoryList(ListView):
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    model = Category

    def get_queryset(self):

        q = super(CategoryList, self).get_queryset()
        self.form = CategoriesListForm(self.request.GET)

        if self.form.is_valid():
            if self.form.cleaned_data['sort']:
                q = q.order_by(self.form.cleaned_data['sort'])
            if self.form.cleaned_data['search']:
                q = q.filter(name=self.form.cleaned_data['search'])
        return q.annotate(questions_count = models.Count('questions__id', distinct=True),
                          answers_count = models.Count('questions__answers__id', distinct=True),
                          likes_count = models.Count('questions__likes', distinct=True))

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['categories_form']=self.form
        return context


@csrf_exempt
def category_create_front(request):

    if request.method == 'POST':
        str = request.body.__str__()
        str = str.replace(' ', '')
        start = str.find("name=")+15
        str = str[start:]
        end = str.find("---") - 2
        name = str[:end]
        if Category.objects.filter(name=name).exists():
            return HttpResponseForbidden('error')
        else:
            category = Category()
            category.name = name
            category.save()
            return HttpResponse('OK')


class CategoryCreate(CreateView):

    model = Category
    fields = 'name',
    context_object_name = 'category'
    template_name = 'categories/category_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CategoryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})

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