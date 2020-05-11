# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path

from treatmentapp.api.treatment import PatientTreatmentView, PatientTreatmentUpdateView

from treatmentapp.api.data import BarGraphData, PICHartGraphData

from treatmentapp.api.recall import Recall



app_name = 'treatmentapp'

urlpatterns = [
	path('encounter/<encounter_id>/treatment', PatientTreatmentView.as_view()),
	path('encounter/<encounter_id>/treatment/update', PatientTreatmentUpdateView.as_view()),
	path('bargraphdata',BarGraphData.as_view()),
	path('paichartgraphdata', PICHartGraphData.as_view()),
	path('recalls/<geography_id>',Recall.as_view()),
    ]
