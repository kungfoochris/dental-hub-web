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
            district=['Male','Female','Kids', 'Adults', 'Other Adults']
            total=[]
            male=[]
            female=[]
            female_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fv_applied=True).count()
            male_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fv_applied=True).count()
            child__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__lt=18,fv_applied=True).count()
            adult__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__range=(19, 60),fv_applied=True).count()
            old__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__gt=60,fv_applied=True).count()

            sealant_male = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',need_sealant=True).count()
            sealant_female = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',need_sealant=True).count()
            sealant_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__age__lt=18,need_sealant=True).count()
            sealant_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__age__range=(19, 60),need_sealant=True).count()
            sealant_old = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__age__gt=60,need_sealant=True).count()

            cavities_prevented_male = 0.2*male_patients_receiving_FV+0.1*sealant_male
            cavities_prevented_female = 0.2*female_patients_receiving_FV+0.1*sealant_female
            cavities_prevented_child = 0.2*child__patients_receiving_FV+0.1*sealant_child
            cavities_prevented_adult = 0.2*adult__patients_receiving_FV+0.1*sealant_adult
            cavities_prevented_old = 0.2*old__patients_receiving_FV+0.1*sealant_old

            contact_male = Encounter.objects.select_related('patient').filter(patient__gender='male').count()
            contact_female = Encounter.objects.select_related('patient').filter(patient__gender='female').count()
            contact_child = Encounter.objects.select_related('patient').filter(patient__age__lt=18).count()
            contact_adult = Encounter.objects.select_related('patient').filter(patient__age__range=(19, 60)).count()
            contact_old= Encounter.objects.select_related('patient').filter(patient__age__gt=60).count()
            
            locationChart = {
            'data': {
            'labels': district,
            'datasets': [
            # {
            # 'label': "Total",
            # 'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            # 'borderColor': 'rgba(255, 206, 86, 1)',
            # 'borderWidth': 1,
            # 'data': total},
            {
            'label': "Number of cavities prevented",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': [cavities_prevented_male,cavities_prevented_female,cavities_prevented_child,contact_adult,contact_old]},
            {
            'label': "CONTACTS",
            'backgroundColor': 'rgba(64, 224, 208, 0.2)',
            'borderColor': 'rgba(64, 224, 208, 1)',
            'borderWidth': 1,
            'data': [contact_male,contact_female,contact_child,contact_adult,contact_old]}]
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