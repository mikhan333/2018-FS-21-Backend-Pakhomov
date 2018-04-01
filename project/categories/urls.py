
from django.conf.urls import url, include
from django.contrib import admin

from categories import views as categories_views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', categories_views.category_detail, name='category_detail'),
    url(r'^$', categories_views.category_list, name='category_list'),
]
