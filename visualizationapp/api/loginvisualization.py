import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from patientapp.models import Patient

from rest_framework import filters
from userapp.models import User
import os
from django.http import JsonResponse
from treatmentapp.models import Treatment
from encounterapp.models import Encounter

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class LoginVisualization(APIView):
      def get(self, request, format=None):
            health_post=[]
            school_seminar=[]
            community=[]
            training=[]
            health_count = Patient.objects.select_related('activity_area').filter(activity_area__name='Health Post').count()
            school_count = Patient.objects.select_related('activity_area').filter(activity_area__name='School Seminar').count()
            community_count = Patient.objects.select_related('activity_area').filter(activity_area__name='Community Outreach').count()
            training_count = Patient.objects.select_related('activity_area').filter(activity_area__name='Training').count()
            health_post.append(health_count)
            school_seminar.append(school_count)
            community.append(community_count)
            training.append(training_count)
            locationChart = {
            'data': {
            'labels': ['Health Post', 'School Seminar', 'Community Outreach', 'Training'],
            'datasets': [
            {
            'label': "Female",
            'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)'],
            'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)'],
            'borderWidth': 1,
            'data': [health_post, school_seminar, community, training]
            }]},
            'options': {
            'responsive':'true',
            'maintainAspectRatio': 'false',
            'aspectRatio': 1.5,
            # 'scales': {
            # 'yAxes': [{
            # 'display': 'false',
            # }],

            # # 'xAxes': [{
            # # 'display': 'false',
            # # }]
            # },
            'title': {
            'display': 'true',
            'text': "Activity Distribution Chart",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"},
            'legend': {
            'display': 'true',
            'position': 'bottom',
            'labels': {
            'usePointStyle': 'true',
            'padding': 20,
            'fontFamily': "'Maven Pro', sans-serif"}
            }}}
            return JsonResponse({"locationChart":locationChart})


class LoginVisualization1(APIView):
    def get(self, request, format=None):
        total_encounter = Encounter.objects.all().count()
        total_patient = Patient.objects.all().count()
        return Response({'total_encounter':total_encounter,'total_patient':total_patient})
