import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from patientapp.models import Patient
from treatmentapp.serializers.visualization import VisualizatioSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.conf import settings
from dental.settings import MEDIA_ROOT
import os
from django.http import JsonResponse

from nepali.datetime import NepaliDate
from visualizationapp.models import Visualization

from visualizationapp.serializers.visualization import TreatMentBarGraphVisualization

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class Visualization1(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id,admin=True):
            district=['Kids', 'Adults', 'Other Adults']
            total=[]
            male=[]
            female=[]
            child_female_count = Visualization.objects.filter(gender='female',age__lt=18).count()
            child_male_count = Visualization.objects.filter(gender='male',age__lt=18).count()
            child_total_patient = Visualization.objects.filter(age__lt=18).count()
            female.append(child_female_count)
            male.append(child_male_count)
            total.append(child_total_patient)

            adult_female_count = Visualization.objects.filter(gender='female',age__range=[60,18]).count()
            adult_male_count = Visualization.objects.filter(gender='male',age__range=[60,18]).count()
            adult_total_patient = Visualization.objects.filter(age__range=[60,18]).count()
            female.append(adult_female_count)
            male.append(adult_male_count)
            total.append(adult_total_patient)

            old_female_count = Visualization.objects.filter(gender='female',age__gt=60).count()
            old_male_count = Visualization.objects.filter(gender='male',age__gt=60).count()
            old_total_patient = Visualization.objects.filter(age__gt=60).count()
            female.append(old_female_count)
            male.append(old_male_count)
            total.append(old_total_patient)

            locationChart = {
            'data': {
            'labels': district,
            'datasets': [{
            'label': "Total",
            'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            'borderColor': 'rgba(255, 206, 86, 1)',
            'borderWidth': 1,
            'data': total},
            {
            'label': "Female",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': female},
            {
            'label': "Male",
            'backgroundColor': 'rgba(64, 224, 208, 0.2)',
            'borderColor': 'rgba(64, 224, 208, 1)',
            'borderWidth': 1,
            'data': male}]
            },
            'options': {
            'aspectRatio': 1.5,
            'scales': {
            'yAxes': [{
            'ticks': {
            'beginAtZero':'true'}
            }]
            },
            'title': {
            'display': 'true',
            'text': "Age-wise Gender Distribution",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"
            },
            'legend': {
            'display': 'true',
            'position': 'bottom',
            'labels': {
            'usePointStyle': 'true',
            'padding': 20,
            'fontFamily': "'Maven Pro', sans-serif"
      }
    }
  }
            }
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can create"},status=400)


class VisualizationFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']
            district=['Kids', 'Adults', 'Other Adults']
            total=[]
            male=[]
            female=[]
            child_female_count = Visualization.objects.filter(gender='female',age__lt=18).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            child_male_count = Visualization.objects.filter(gender='male',age__lt=18).filter(created_at__range=[end_date,start_date],geography_id=location).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            child_total_patient = Visualization.objects.filter(age__lt=18).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            female.append(child_female_count)
            male.append(child_male_count)
            total.append(child_total_patient)

            adult_female_count = Visualization.objects.filter(gender='female',age__range=[60,18]).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            adult_male_count = Visualization.objects.filter(gender='male',age__range=[60,18]).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            adult_total_patient = Visualization.objects.filter(age__range=[60,18]).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            female.append(adult_female_count)
            male.append(adult_male_count)
            total.append(adult_total_patient)

            old_female_count = Visualization.objects.filter(gender='female',age__gt=60).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            old_male_count = Visualization.objects.filter(gender='male',age__gt=60).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            old_total_patient = Visualization.objects.filter(age__gt=60).filter(created_at__range=[end_date,start_date],geography_id=location).count()
            female.append(old_female_count)
            male.append(old_male_count)
            total.append(old_total_patient)

            locationChart = {
            'data': {
            'labels': district,
            'datasets': [{
            'label': "Total",
            'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            'borderColor': 'rgba(255, 206, 86, 1)',
            'borderWidth': 1,
            'data': total},
            {
            'label': "Female",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': female},
            {
            'label': "Male",
            'backgroundColor': 'rgba(64, 224, 208, 0.2)',
            'borderColor': 'rgba(64, 224, 208, 1)',
            'borderWidth': 1,
            'data': male}]
            },
            'options': {
            'aspectRatio': 1.5,
            'scales': {
            'yAxes': [{
            'ticks': {
            'beginAtZero':'true'}
            }]
            },
            'title': {
            'display': 'true',
            'text': "Age-wise Gender Distribution",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"
            },
            'legend': {
            'display': 'true',
            'position': 'bottom',
            'labels': {
            'usePointStyle': 'true',
            'padding': 20,
            'fontFamily': "'Maven Pro', sans-serif"
      }
    }
  }
            }
            return JsonResponse({"locationChart":locationChart})
        return Response(serializer.error)
