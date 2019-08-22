# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from addressapp.api.geography import GeographyListView, GeographyUpdateView
from addressapp.api.activity import ActivityAreaListView, ActivityAreaUpdateView, ActivityListView
from rest_framework.urlpatterns import format_suffix_patterns

from addressapp.api.address import AddressList

# from userapp.api.staticpage import StaticPageView

app_name = 'addressapp'

urlpatterns = [
	path('geography', GeographyListView.as_view()),
	path('geography/<pk>', GeographyUpdateView.as_view(),name="geography-detail"),
	path("events", ActivityListView.as_view()),
	path('activities', ActivityAreaListView.as_view()),
	path('activities/<pk>', ActivityAreaUpdateView.as_view()),
	path('addresses', AddressList.as_view()),
	# path('addresses/<district>', MunicipalityList.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
