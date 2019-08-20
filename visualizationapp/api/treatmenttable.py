import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from patientapp.models import Patient

from rest_framework import filters
from userapp.models import User, CustomUser
import os
from django.http import JsonResponse
from treatmentapp.models import Treatment

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class TreatmentTableVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, format=None):
            if CustomUser.objects.select_related('role').filter(role__name='warduser').exists():
                  treatment_obj = Treatment.objects.all().count()
                  treatment_male = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male').count()
                  treatment_female = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female').count()
                  return Response({"treatment_obj":treatment_obj,'treatment_male':treatment_male,'treatment_female':treatment_female})
            return Response({"treatment_obj":"do not have a permission"},status=400)