# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from treatmentapp.api.visualization import Visualization, Visualization1
from rest_framework.urlpatterns import format_suffix_patterns


from visualizationapp.api.loginvisualization import LoginVisualization,LoginVisualization1
from visualizationapp.api.treatmenttable import TreatmentTableVisualization

from visualizationapp.api.treatmentbargraph import TreatMentBarGraph
from visualizationapp.api.table import OverviewVisualization1, TreatmentTable2Visualization,\
Table3Visualization,Table4Visualization, VisualizationSetting

from visualizationapp.api.wardvisualization import WardVisualization1,\
WardTreatmentTableVisualization1,WardTableVisualization2,\
WardSettingVisualization, WardTreatmentVisualization,\
WardUserlineVisualization


from visualizationapp.api.filtervisualization import OverviewVisualization

from visualizationapp.api.crosssectional import SectionalVisualization


from visualizationapp.api.wardlinechart import WardlineVisualization

from visualizationapp.api.visualization_table import TableVisualization

from visualizationapp.api.datavisualization import DataVisualization

from visualizationapp.api.treatmentlinechart import TreatmentVisualizationLineChart,\
TreatmentVisualizationLineChart1, TreatmentVisualizationLineChart2


app_name = 'visualizationapp'

urlpatterns = [
	path('loginvisualization', LoginVisualization.as_view()),
	path('loginvisualization1', LoginVisualization1.as_view()),
	path('treatment',TreatmentTableVisualization.as_view()),
	path('treatmentnargraph',TreatMentBarGraph.as_view()),

	path('overviewvisualization1',OverviewVisualization1.as_view()),
	path('table1', TreatmentTable2Visualization.as_view()),
	path('table2',Table3Visualization.as_view()),
	path('table3',Table4Visualization.as_view()),
	path('settingsgraph',VisualizationSetting.as_view()),

	path('wardvisualization',WardVisualization1.as_view()),
	path('wardtablevisualization',WardTreatmentTableVisualization1.as_view()),
	path('wardtreatmenttablevisualizaation',WardTableVisualization2.as_view()),
	path('wardsettingsgraph',WardSettingVisualization.as_view()),
	path('wardtreatmentgraph',WardTreatmentVisualization.as_view()),
	path('overviewvisualization/<start_date>/<end_date>/<location_id>',OverviewVisualization.as_view()),
	path('sectional',SectionalVisualization.as_view()),
	path('treatmentvisualizationlinechart',TreatmentVisualizationLineChart.as_view()),
	path('treatmentvisualizationlinechart1',TreatmentVisualizationLineChart1.as_view()),
	path('treatmentvisualizationlinechart2',TreatmentVisualizationLineChart2.as_view()),
	path('wardlineVisualization',WardlineVisualization.as_view()),
	path('tablvisualization',TableVisualization.as_view()),
	path('data',DataVisualization.as_view()),
	path('waruserlinechart',WardUserlineVisualization.as_view()),
	]
urlpatterns = format_suffix_patterns(urlpatterns)
