# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from encounterapp.api.history import PatientHistoryView, PatientHistoryUpdateView
from encounterapp.api.encounter import EncounterView, EncounterUpdateView
from encounterapp.api.refer import PatientReferView, PatientReferUpdateView
from encounterapp.api.screeing import PatientScreeingView, PatientScreeingUpdateView
from encounterapp.api.encounter_type import EncounterTypeView


from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'encounterapp'

urlpatterns = [
	path('patients/<patient_id>/encounter', EncounterView.as_view()),
	path('patients/<patient_id>/encounter/<encounter_id>', EncounterUpdateView.as_view()),
	path('encounter/<encounter_id>/history', PatientHistoryView.as_view()),
	path('encounter/<encounter_id>/history/update', PatientHistoryUpdateView.as_view()),
	path('encounter/<encounter_id>/refer', PatientReferView.as_view()),
	path('encounter/<encounter_id>/refer/update', PatientReferUpdateView.as_view()),
	path('encounter/<encounter_id>/screeing', PatientScreeingView.as_view()),
	path('encounter/<encounter_id>/screeing/update', PatientScreeingUpdateView.as_view()),
	path('encounter/type', EncounterTypeView.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
