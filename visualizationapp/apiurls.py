# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path

# from treatmentapp.api.visualization import Visualization, Visualization1

from visualizationapp.api.dashboard import OverviewVisualization1,\
TreatmentActivityList,TreatmentbyWardList,DateReturn

from visualizationapp.api.dashboardvisualization import VisualizationSetting,\
VisualizationSettingFilter,PieChartVisualization,PieChartVisualizationFilter

from visualizationapp.api.wardlinechart import WardlineVisualization,\
WardlineVisualizationFilter

from rest_framework.urlpatterns import format_suffix_patterns


from visualizationapp.api.loginvisualization import LoginVisualization,LoginVisualization1

from visualizationapp.api.treatmenttable import TreatmentTableBasicData,\
TreatmentStrategicData
# TreatmentTableListfilter

from visualizationapp.api.treatmentbargraph import TreatMentBarGraph,\
TreatMentBarGraphFilter




from visualizationapp.api.wardvisualization import WardVisualization1,\
WardTreatmentTableVisualization1,WardTableVisualization2,\
WardSettingVisualization, WardTreatmentVisualization,\
WardUserlineVisualization,WardStrategicData


# from visualizationapp.api.filtervisualization import OverviewVisualization

from visualizationapp.api.crosssectional import SectionalVisualization




from visualizationapp.api.visualization_table import TableVisualization

from visualizationapp.api.datavisualization import DataVisualization

from visualizationapp.api.treatmentlinechart import TreatmentPreventionRatioVisualization,\
TreatmentEarlyIntervention, TreatmentRecallDistribution


from visualizationapp.api.longitudinal import LongitudinalVisualization,\
LongitudinalVisualization1


app_name = 'visualizationapp'

urlpatterns = [
	path('loginvisualization', LoginVisualization.as_view()),
	path('loginvisualization1', LoginVisualization1.as_view()),

	path('treatmentnargraph',TreatMentBarGraph.as_view()),
	path('treatmentnargraphfilter',TreatMentBarGraphFilter.as_view()),

	path('overviewvisualization',OverviewVisualization1.as_view()),
	path('treatmentactivities', TreatmentActivityList.as_view()),
	path('treatmentwards',TreatmentbyWardList.as_view()),
	path('returndate',DateReturn.as_view()),
	path('overviewbargraph',VisualizationSetting.as_view()),
	path('settingsgraphfilter',VisualizationSettingFilter.as_view()),
	path('overviewpiechart',PieChartVisualization.as_view()),
	path('piechartfilter',PieChartVisualizationFilter.as_view()),
	path('dashboardlinechart',WardlineVisualization.as_view()),
	path('wardlineVisualizationfilter',WardlineVisualizationFilter.as_view()),


	path('treatmentstrategicdatas',TreatmentStrategicData.as_view()),


	path('treatment',TreatmentTableBasicData.as_view()),
	path('preventionratio',TreatmentPreventionRatioVisualization.as_view()),
	path('earlyintervention',TreatmentEarlyIntervention.as_view()),
	path('recalldistribution',TreatmentRecallDistribution.as_view()),




	path('wardvisualization',WardVisualization1.as_view()),
	path('wardtablevisualization',WardTreatmentTableVisualization1.as_view()),
	path('wardtreatmenttablevisualizaation',WardTableVisualization2.as_view()),
	path('wardsettingsgraph',WardSettingVisualization.as_view()),
	path('wardtreatmentgraph',WardTreatmentVisualization.as_view()),
	# path('overviewvisualization/<start_date>/<end_date>/<location_id>',OverviewVisualization.as_view()),
	path('sectional',SectionalVisualization.as_view()),


	path('tablvisualization',TableVisualization.as_view()),
	path('data',DataVisualization.as_view()),
	path('waruserlinechart',WardUserlineVisualization.as_view()),
	path('longitudinal',LongitudinalVisualization.as_view()),
	path('longitudinal1',LongitudinalVisualization1.as_view()),


	path('wardstrategicdata',WardStrategicData.as_view()),



	]
urlpatterns = format_suffix_patterns(urlpatterns)
