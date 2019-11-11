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

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class TreatMentBarGraph(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id):
            treatment=['EXO','ART','SEAL', 'SDF', 'FV']
            total_sdf = Visualization.objects.filter(sdf=True).count()
            total_exo = Visualization.objects.filter(exo=True).count()
            total_art = Visualization.objects.filter(art=True).count()
            total_seal = Visualization.objects.filter(seal=True).count()
            total_fv = Visualization.objects.filter(fv=True).count()

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
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can create"},status=400)
