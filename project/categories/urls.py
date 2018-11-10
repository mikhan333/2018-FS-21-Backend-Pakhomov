
from django.conf.urls import url, include
from django.contrib import admin

from categories import views as categories_views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', categories_views.category_detail, name='category_detail'),
    url(r'^$', categories_views.CategoryList.as_view(), name='category_list'),
    url(r'^create/$', categories_views.CategoryCreate.as_view(), name='category_create'),
]
#category_list