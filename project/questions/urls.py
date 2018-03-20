from django.conf.urls import url, include
from django.contrib import admin

from questions import views as questions_views

urlpatterns = [
    url(r'^(?P<question_id>\d+)/$', questions_views.question_content, name='question_content'),
    url(r'^ask/$', questions_views.question_ask, name='question_ask'),
    url(r'^$', questions_views.question_list, name='question_list'),
]
