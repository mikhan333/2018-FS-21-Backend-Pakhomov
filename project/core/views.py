# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def main_page(request):
    context = {}
    context['name']='Main page'
    return render(request, 'core/main_page.html', context)