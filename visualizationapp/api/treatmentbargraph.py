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
from encounterapp.models import Screeing,Encounter
from django.db.models import Q
from visualizationapp.models import Visualization
from visualizationapp.serializers.visualization import TreatMentBarGraphVisualization
from nepali.datetime import NepaliDate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class TreatMentBarGraph(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id):
            treatment=['EXO','ART','SEAL', 'SDF', 'FV']
            total_sdf = Visualization.objects.filter(sdf=True,active=True).count()
            total_exo = Visualization.objects.filter(exo=True,active=True).count()
            total_art = Visualization.objects.filter(art=True,active=True).count()
            total_seal = Visualization.objects.filter(seal=True,active=True).count()
            total_fv = Visualization.objects.filter(fv=True,active=True).count()

            locationChart = {
            'data': {
            'labels': treatment,
            'datasets': [
            {
            'label': "Number of cavities prevented",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': [total_exo,total_art,total_seal,total_sdf,total_fv]},
            ]},
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
            'text': "Bar graph of treatment data",
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
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can create"},status=400)

class TreatMentBarGraphFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():

            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']
            treatment=['EXO','ART','SEAL', 'SDF', 'FV']
            total_sdf = Visualization.objects.filter(sdf=True,active=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            total_exo = Visualization.objects.filter(exo=True,active=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            total_art = Visualization.objects.filter(art=True,active=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            total_seal = Visualization.objects.filter(seal=True,active=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            total_fv = Visualization.objects.filter(fv=True,active=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()

            locationChart = {
            'data': {
            'labels': treatment,
            'datasets': [
            {
            'label': "Number of cavities prevented",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': [total_exo,total_art,total_seal,total_sdf,total_fv]},
            ]},
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
            'text': "Bar graph of treatment data",
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
            return JsonResponse({"locationChart":locationChart},status=200)
        return Response(serializer.error)
