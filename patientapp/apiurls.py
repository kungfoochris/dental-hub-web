# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from patientapp.api.patient import PatientListView,PatientAdd,PatientUpdateView
from rest_framework.urlpatterns import format_suffix_patterns

# from userapp.api.staticpage import StaticPageView

app_name = 'patientapp'

urlpatterns = [
	path('patients/<geography_id>', PatientListView.as_view(), name='user-list'),
	path('patients', PatientAdd.as_view()),
	path('patient/<patient_id>',PatientUpdateView.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
