# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from treatmentapp.api.treatment import PatientTreatmentView
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'treatmentapp'

urlpatterns = [
	path('encounter/<encounter_id>/treatment', PatientTreatmentView.as_view()),

    ]
urlpatterns = format_suffix_patterns(urlpatterns)
