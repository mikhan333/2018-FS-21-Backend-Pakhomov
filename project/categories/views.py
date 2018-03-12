# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def category_detail(request, category_id):
    return HttpResponse('Это категория номер: {}'.format(category_id))

def categories(request):
    return HttpResponse('Это список всех категорий')
