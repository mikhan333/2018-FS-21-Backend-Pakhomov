"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from core.views import main_page

from categories.views import category_detail
from categories.views import categories

from questions.views import question_content
from questions.views import question_ask
from questions.views import questions

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', main_page),

    url(r'^categories/(\d+)/$', category_detail),
    url(r'^categories/$', categories),

    url(r'^questions/(\d+)/$', question_content),
    url(r'^questions/ask/$', question_ask),
    url(r'^questions/$', questions),
]
