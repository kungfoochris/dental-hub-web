# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from userapp.api.user import UserListView
from rest_framework.urlpatterns import format_suffix_patterns

# from userapp.api.staticpage import StaticPageView

app_name = 'userapp'

urlpatterns = [
	path('users', UserListView.as_view(), name='user-list'),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
