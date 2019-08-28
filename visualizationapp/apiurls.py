# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from treatmentapp.api.visualization import Visualization, Visualization1
from rest_framework.urlpatterns import format_suffix_patterns


from visualizationapp.api.loginvisualization import LoginVisualization
from visualizationapp.api.treatmenttable import TreatmentTableVisualization

from visualizationapp.api.treatmentbargraph import TreatMentBarGraph
from visualizationapp.api.table import TreatmentTable1Visualization, TreatmentTable2Visualization,\
Table3Visualization,Table4Visualization, VisualizationSetting



app_name = 'visualizationapp'

urlpatterns = [
	path('loginvisualization', LoginVisualization.as_view()),
	path('treatment',TreatmentTableVisualization.as_view()),
	path('treatmentnargraph',TreatMentBarGraph.as_view()),
	path('table',TreatmentTable1Visualization.as_view()),
	path('table1', TreatmentTable2Visualization.as_view()),
	path('table2',Table3Visualization.as_view()),
	path('table3',Table4Visualization.as_view()),
	path('settingsgraph',VisualizationSetting.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
