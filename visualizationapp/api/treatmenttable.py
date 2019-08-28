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

from nepali.datetime import NepaliDate  
from django.db.models import DurationField, F, ExpressionWrapper
import datetime
# from datetime import datetime
# from datetime import timedelta
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


# class TreatmentTableVisualization(APIView):
#       permission_classes = (IsPostOrIsAuthenticated,)
#       def get(self, request, format=None):
#             np_date = NepaliDate()
#             d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
#             pa = Patient.objects.get(uid="864FBA1EC0364E169D67FE6B35034B3C")
#             lessthan18 = d - datetime.timedelta(days=365*18)
#             greaterthan60 = d - datetime.timedelta(days=365*60)
#             print(lessthan18)
#             print("==================")
#             print(greaterthan60)
#             total_patient = Patient.objects.all().count()
#             child_patient=Patient.objects.filter(dob__gt=lessthan18).count()
#             adult_patient=Patient.objects.filter(dob__range=(greaterthan60,lessthan18)).count()
#             old_patient = total_patient-child_patient-adult_patient
#             # old_patient=Patient.objects.annotate(diff=ExpressionWrapper(d - F('dob'), output_field=DurationField())).filter(diff__gt=datetime.timedelta(365*60)).count()
#             # adult_patient=Patient.objects.annotate(diff=ExpressionWrapper(d - F('dob'), output_field=DurationField())).filter(diff__range=(datetime.timedelta(365*18),datetime.timedelta(365*60))).count()
#             # child_patient=Patient.objects.annotate(diff=ExpressionWrapper(d - F('dob'), output_field=DurationField())).filter(diff__lt=datetime.timedelta(1)).count()
            
#             return Response({"child_patient":child_patient,"adult_patient":adult_patient,"old_patient":old_patient})



class TreatmentTableVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, format=None):
            if User.objects.filter(id=request.user.id).exists():
                np_date = NepaliDate()
                d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
                lessthan18 = d - datetime.timedelta(days=365*18)
                greaterthan60 = d - datetime.timedelta(days=365*60)

                treatment_obj = Treatment.objects.all().count()
                treatment_male = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male').count()
                treatment_female = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female').count()
                treatment_child = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18).count()
                treatment_adult = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18)).count()
                treatment_old = treatment_obj-treatment_child-treatment_adult

                total_fv = Treatment.objects.filter(fluoride_varnish=True).count()
                female_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fluoride_varnish=True).count()
                male_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fluoride_varnish=True).count()
                child__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,fluoride_varnish=True).count()
                adult__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),fluoride_varnish=True).count()
                old__patients_receiving_FV = total_fv-child__patients_receiving_FV-adult__patients_receiving_FV

                total_need_sealant = Screeing.objects.filter(need_sealant=True).count()
                sealant_male = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',need_sealant=True).count()
                sealant_female = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',need_sealant=True).count()
                sealant_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,need_sealant=True).count()
                sealant_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),need_sealant=True).count()
                sealant_old = total_need_sealant-sealant_child-sealant_adult

                cavities_prevented_male = 0.2*male_patients_receiving_FV+0.1*sealant_male
                cavities_prevented_female = 0.2*female_patients_receiving_FV+0.1*sealant_female
                cavities_prevented_child = 0.2*child__patients_receiving_FV+0.1*sealant_child
                cavities_prevented_adult = 0.2*adult__patients_receiving_FV+0.1*sealant_adult
                cavities_prevented_old = 0.2*old__patients_receiving_FV+0.1*sealant_old
                total_cavities = cavities_prevented_male+cavities_prevented_female

                total_encounter = Encounter.objects.all().count()
                contact_male = Encounter.objects.select_related('patient').filter(patient__gender='male').count()
                contact_female = Encounter.objects.select_related('patient').filter(patient__gender='female').count()
                contact_child = Encounter.objects.select_related('patient').filter(patient__dob__gt=lessthan18).count()
                contact_adult = Encounter.objects.select_related('patient').filter(patient__dob__range=(greaterthan60, lessthan18)).count()
                contact_old= total_encounter-contact_child-contact_adult

                return Response([["Number of Cavities Prevented",cavities_prevented_male, cavities_prevented_female, cavities_prevented_child, cavities_prevented_adult, cavities_prevented_old,total_cavities],\
                    ["Contacts", contact_male, contact_female, contact_child, contact_adult, contact_old, total_encounter]])
            return Response({"treatment_obj":"do not have a permission"},status=400)


