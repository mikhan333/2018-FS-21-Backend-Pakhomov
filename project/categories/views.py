# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, reverse
from .models import Category

def category_detail(request, category_id=None):
    category = Category.objects.get(id=category_id)
    context={
        'category': category,
        'questions': category.questions.all().filter(is_archive=False)
    }

    return render(request, 'categories/category_detail.html', context)


def category_list(request):
    context = {
        'categories': Category.objects.all()
    }

    return render(request, 'categories/category_list.html', context)
