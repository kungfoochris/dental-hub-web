# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from encounterapp.api.history import PatientHistoryView, PatientHistoryUpdateView
from encounterapp.api.encounter import EncounterView, EncounterUpdateView
from encounterapp.api.refer import PatientReferView, PatientReferUpdateView
from encounterapp.api.screeing import PatientScreeingView, PatientScreeingUpdateView
from encounterapp.api.modifydelete import ModifyDeleteDetail,EncounterAdminStatus,EncounterFlagDead,EncounterRestore,Recyclebin,CheckRestoreExpiry,CheckModifyExpiry



app_name = 'encounterapp'

urlpatterns = [
	path('patients/<patient_id>/encounters', EncounterView.as_view()),
	path('patients/<patient_id>/encounters/<encounter_id>', EncounterUpdateView.as_view()),
	path('encounter/<encounter_id>/history', PatientHistoryView.as_view()),
	path('encounter/<encounter_id>/history/update', PatientHistoryUpdateView.as_view()),
	path('encounter/<encounter_id>/refer', PatientReferView.as_view()),
	path('encounter/<encounter_id>/refer/update', PatientReferUpdateView.as_view()),
	path('encounter/<encounter_id>/screening', PatientScreeingView.as_view()),
	path('encounter/<encounter_id>/screening/update', PatientScreeingUpdateView.as_view()),
	path('modifydelete', ModifyDeleteDetail.as_view()),
	path('encounterstatus/<id>', EncounterAdminStatus.as_view()),
	path('flagdead/<id>', EncounterFlagDead.as_view()),
	path('encounterrestore/<encounter_id>', EncounterRestore.as_view()),
	path('recyclebin', Recyclebin.as_view()),
	path('checkmodifyexpiry', CheckModifyExpiry.as_view()),
	path('checkrestoreexpiry', CheckRestoreExpiry.as_view()),
	

    ]
