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

from visualizationapp.api.wardvisualization import WardVisualization1,WardTreatmentTableVisualization1,\
WardTableVisualization2,WardSettingVisualization, WardTreatmentVisualization


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
	path('wardvisualization',WardVisualization1.as_view()),
	path('wardtablevisualization',WardTreatmentTableVisualization1.as_view()),
	path('wardtreatmenttablevisualizaation',WardTableVisualization2.as_view()),
	path('wardsettingsgraph',WardSettingVisualization.as_view()),
	path('wardtreatmentgraph',WardTreatmentVisualization.as_view()),
	]
urlpatterns = format_suffix_patterns(urlpatterns)
