# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from flagapp.api.flag import FlagListView,  FlagUpdateView



app_name = 'flagapp'

urlpatterns = [
	path('flags', FlagListView.as_view()),
	path('flags/<flag_id>', FlagUpdateView.as_view()),
    ]
