from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from questions import views as questions_views

from jsonrpc import jsonrpc_site

urlpatterns = [
    url(r'^(?P<pk>\d+)/detail/$', questions_views.question_content, name='question_content'),
    url(r'^create/$', login_required(questions_views.QuestionCreate.as_view()), name='question_create'),
    url(r'^(?P<pk>\d+)/edit/$', questions_views.QuestionEdit.as_view(), name='question_edit'),
    url(r'^$', questions_views.question_list, name='question_list'),
    url(r'^(?P<pk>\d+)/comments/$', questions_views.question_comments, name='question_comments'),
    url(r'^(?P<pk>\d+)/likes/$', questions_views.QuestionLikeAjaxView.as_view(), name='question_likes'),

    #url(r'^api/$', jsonrpc_site.dispatch, name='api'),
]
