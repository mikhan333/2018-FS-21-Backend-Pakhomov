# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

def main_page(request):

    return HttpResponse('Это главная страница')