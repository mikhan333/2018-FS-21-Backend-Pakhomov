from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from questions import views as questions_views

urlpatterns = [
    url(r'^(?P<pk>\d+)/detail/$', questions_views.question_content, name='question_content'),
    url(r'^create/$', login_required(questions_views.QuestionCreate.as_view()), name='question_create'),
    url(r'^(?P<pk>\d+)/edit/$', questions_views.QuestionEdit.as_view(), name='question_edit'),
    url(r'^$', questions_views.question_list, name='question_list'),
]
