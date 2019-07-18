# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from treatmentapp.api.visualization import Visualization, Visualization1
from rest_framework.urlpatterns import format_suffix_patterns
from treatmentapp.api.treatment import PatientTreatmentView, PatientTreatmentUpdateView


app_name = 'treatmentapp'

urlpatterns = [
	path('visualizations', Visualization.as_view()),
	path('visualization/locations', Visualization1.as_view()),
	path('encounter/<encounter_id>/treatment', PatientTreatmentView.as_view()),
	path('encounter/<encounter_id>/treatment/update', PatientTreatmentUpdateView.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
