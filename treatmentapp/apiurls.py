# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
# from treatmentapp.api.visualization import Visualization1,VisualizationFilter
from rest_framework.urlpatterns import format_suffix_patterns
from treatmentapp.api.treatment import PatientTreatmentView, PatientTreatmentUpdateView

from treatmentapp.api.data import BarGraphData, PICHartGraphData

from treatmentapp.api.recall import Recall



app_name = 'treatmentapp'

urlpatterns = [
	# path('visualizations', Visualization.as_view()),
	# path('visualizations', Visualization1.as_view()),
	# path('visualizationsfilter',VisualizationFilter.as_view()),
	path('encounter/<encounter_id>/treatment', PatientTreatmentView.as_view()),
	path('encounter/<encounter_id>/treatment/update', PatientTreatmentUpdateView.as_view()),
	path('bargraphdata',BarGraphData.as_view()),
	path('paichartgraphdata', PICHartGraphData.as_view()),
	path('recalls/<geography_id>',Recall.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
