# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from addressapp.api.geography import GeographyListView
from addressapp.api.activity import ActivityAreaListView
from rest_framework.urlpatterns import format_suffix_patterns

# from userapp.api.staticpage import StaticPageView

app_name = 'addressapp'

urlpatterns = [
	path('geography', GeographyListView.as_view()),
	path('activity', ActivityAreaListView.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
