
from django.conf.urls import url, include

from django.contrib.auth.decorators import login_required
from oauthlib.uri_validate import path

from core import views as core_views

from jsonrpc import jsonrpc_site

urlpatterns = [
    url(r'^$', core_views.main_page, name='main_page'),
    url(r'^login/$', core_views.Login.as_view(), name='login'),
    url(r'^logout/$', core_views.Logout.as_view(), name='logout'),
    url(r'^register/$', core_views.register, name='register'),
    url(r'^profile/$', login_required(core_views.profile), name='profile'),

    url(r'^api/$', jsonrpc_site.dispatch, name='api'),
]
