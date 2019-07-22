# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from addressapp.api.geography import GeographyListView, GeographyUpdateView
from addressapp.api.activity import ActivityAreaListView, ActivityAreaUpdateView
from rest_framework.urlpatterns import format_suffix_patterns

# from userapp.api.staticpage import StaticPageView

app_name = 'addressapp'

urlpatterns = [
	path('geography', GeographyListView.as_view()),
	path('geography/<pk>', GeographyUpdateView.as_view()),
	path('activities', ActivityAreaListView.as_view()),
	path('activities/<pk>', ActivityAreaUpdateView.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
