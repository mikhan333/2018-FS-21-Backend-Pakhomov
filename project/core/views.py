# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from .models import User

def main_page(request):
    context = {}
    context['name'] = 'Main page'
    if request.user.is_authenticated():
        context['auth_url'] = 'core:profile'
        context['auth_url_name'] = 'Profile'
    else:
        context['auth_url'] = 'core:login'
        context['auth_url_name'] = 'Login'
    return render(request, 'core/main_page.html', context)

class Login(LoginView):

    template_name = 'core/login.html'

class Logout(LogoutView):

    template_name = 'core/logout.html'



class RegisterForm(UserCreationForm):
    template_name = 'core/register.html'


def register(request):
    us = User()
    if request.method == 'GET':
        form = RegisterForm(instance = us)
        return render(request, 'core/register.html', {'form' : form})

    elif request.method == 'POST':
        form=RegisterForm(request.POST, instance = us)
        if form.is_valid():
            us=form.save()
            return redirect('core:login')
        else:
            return render(request, 'core/register.html', {'form': form})

def profile(request):
    context = {}
    return render(request, 'core/profile.html', context)