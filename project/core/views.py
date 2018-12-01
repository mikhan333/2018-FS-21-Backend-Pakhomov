# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic.edit import FormView
from .models import User
from questions.models import Question
from django.db import models
import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from uuid import uuid4


def main_page(request):
    context = {}
    context['name'] = 'Main page'
    questions = Question.objects.all().filt_del(request.user).order_by("-created")[0:10].annotate_manager()
    context['questions'] = questions
    if request.user.is_authenticated():
        context['auth_url'] = 'core:profile'
        context['auth_url_name'] = 'Profile'
    else:
        context['auth_url'] = 'core:login'
        context['auth_url_name'] = 'Login'
    return render(request, 'core/main_page.html', context)


class Login(LoginView):

    template_name = 'core/login.html'


@csrf_exempt
def login_front(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        username = data['login']
        password = data['password']
        if not User.objects.filter(username=username).exists():
            return HttpResponseForbidden('error')

        user = get_object_or_404(User, username=username)

        if check_password(password, user.password):
            return JsonResponse({'token': uuid4()})
        else:
            return HttpResponseForbidden('error')




class Logout(LogoutView):

    template_name = 'core/logout.html'


class RegisterForm(UserCreationForm):
    template_name = 'core/register.html'

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


def register(request):
    us = User()

    if request.method == 'GET':
        form = RegisterForm(instance = us)
        return render(request, 'core/register.html', {'form' : form})

    elif request.method == 'POST':
        form = RegisterForm(request.POST, instance = us)
        if form.is_valid():
            us = form.save()
            return redirect('core:login')
        else:
            return render(request, 'core/register.html', {'form': form})


def profile(request):
    quest = Question.objects.filter(author=request.user).aggregate(question_count=models.Count('id', distinct=True))
    questions = Question.objects.filter(author=request.user)
    context = {
        'quest': quest,
        'questions': questions,
        'client': request.user,
    }
    return render(request, 'core/profile.html', context)