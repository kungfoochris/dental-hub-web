# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from patientapp.api.patient import PatientListView
from rest_framework.urlpatterns import format_suffix_patterns

# from userapp.api.staticpage import StaticPageView

app_name = 'patientapp'

urlpatterns = [
	path('patients', PatientListView.as_view(), name='user-list'),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
