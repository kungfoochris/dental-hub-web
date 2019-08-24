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
from encounterapp.models import Screeing,Encounter

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
                  treatment_child = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__lt=18).count()
                  treatment_adult = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__range=(19, 60)).count()
                  treatment_old = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__gt=60).count()

                  female_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fluoride_varnish=True).count()
                  male_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fluoride_varnish=True).count()
                  child__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__lt=18,fluoride_varnish=True).count()
                  adult__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__range=(19, 60),fluoride_varnish=True).count()
                  old__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__age__gt=60,fluoride_varnish=True).count()

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


                  return Response({"cavities_prevented":["Number of Cavities Prevented",cavities_prevented_male,cavities_prevented_female,cavities_prevented_child,cavities_prevented_adult,cavities_prevented_old],\
                    'contact':["Contacts", contact_male,contact_female,contact_child,contact_adult,contact_old]})
            return Response({"treatment_obj":"do not have a permission"},status=400)
