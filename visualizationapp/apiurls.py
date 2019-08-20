# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from treatmentapp.api.visualization import Visualization, Visualization1
from rest_framework.urlpatterns import format_suffix_patterns


from visualizationapp.api.loginvisualization import LoginVisualization
from visualizationapp.api.treatmenttable import TreatmentTableVisualization


app_name = 'visualizationapp'

urlpatterns = [
	path('loginvisualization', LoginVisualization.as_view()),
	path('treatment',TreatmentTableVisualization.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
