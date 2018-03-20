
from django.conf.urls import url, include
from django.contrib import admin

from core import views as core_views

urlpatterns = [
    url(r'^$', core_views.main_page, name='main_page')
]
