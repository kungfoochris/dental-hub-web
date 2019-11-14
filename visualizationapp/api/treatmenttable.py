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
from visualizationapp.models import Visualization
from nepali.datetime import NepaliDate
from django.db.models import DurationField, F, ExpressionWrapper
from visualizationapp.serializers.visualization import TreatMentBarGraphVisualization
import datetime
# from datetime import datetime
# from datetime import timedelta
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365*18)
greaterthan60 = d - datetime.timedelta(days=365*60)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class TreatmentTableVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, format=None):
            if User.objects.filter(id=request.user.id).exists():
                # np_date = NepaliDate()
                # d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
                # lessthan18 = d - datetime.timedelta(days=365*18)
                # greaterthan60 = d - datetime.timedelta(days=365*60)

                treatment_obj = Treatment.objects.all().count()

                treatment_male = Visualization.objects.filter(gender='male').count()
                treatment_female = Visualization.objects.filter(gender='female').count()
                treatment_child = Visualization.objects.filter(age__lt=18).count()
                treatment_adult = Visualization.objects.filter(age__range=(18, 60)).count()
                treatment_old = Visualization.objects.filter(age__gt=60).count()

                total_fv = Visualization.objects.filter(fv=True).count()
                female_patients_receiving_FV=Visualization.objects.filter(gender='female',fv=True).count()
                male_patients_receiving_FV=Visualization.objects.filter(gender='male',fv=True).count()
                child__patients_receiving_FV = Visualization.objects.filter(age__lt=18,fv=True).count()
                adult__patients_receiving_FV = Visualization.objects.filter(age__range=(18, 60),fv=True).count()
                old__patients_receiving_FV = Visualization.objects.filter(age__gt=60,fv=True).count()

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
                contact_male = Visualization.objects.filter(gender='male').count()
                contact_female = Visualization.objects.filter(gender='female').count()
                contact_child = Visualization.objects.filter(age__lt=18).count()
                contact_adult = Visualization.objects.filter(age__range=(18, 60)).count()
                contact_old= Visualization.objects.filter(age__gt=60).count()
                total_contact = contact_male+contact_female

                return Response([["Number of Cavities Prevented",round(cavities_prevented_male,2), round(cavities_prevented_female,2), round(cavities_prevented_child,2), round(cavities_prevented_adult,2), round(cavities_prevented_old,2),round(total_cavities,2)],\
                    ["Contacts", contact_male, contact_female, contact_child, contact_adult, contact_old, total_contact]])
            return Response({"treatment_obj":"do not have a permission"},status=400)

class TreatmentTableVisualizationFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']

            treatment_male = Visualization.objects.filter(gender='male').filter(created_at__range=[start_date,end_date],geography_id=location).count()
            treatment_female = Visualization.objects.filter(gender='female').filter(created_at__range=[start_date,end_date],geography_id=location).count()
            treatment_child = Visualization.objects.filter(age__lt=18).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            treatment_adult = Visualization.objects.filter(age__range=(18, 60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            treatment_old = Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()

            total_fv = Visualization.objects.filter(fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            female_patients_receiving_FV=Visualization.objects.filter(gender='female',fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            male_patients_receiving_FV=Visualization.objects.filter(gender='male',fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            child__patients_receiving_FV = Visualization.objects.filter(age__lt=18,fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            adult__patients_receiving_FV = Visualization.objects.filter(age__range=(18, 60),fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            old__patients_receiving_FV = Visualization.objects.filter(age__gt=60,fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).count()

            total_need_sealant = Screeing.objects.select_related('encounter_id').filter(need_sealant=True).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location).count()
            sealant_male = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',need_sealant=True).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location).count()
            sealant_female = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',need_sealant=True).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location).count()
            sealant_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,need_sealant=True).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location).count()
            sealant_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),need_sealant=True).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location).count()
            sealant_old = total_need_sealant-sealant_child-sealant_adult

            cavities_prevented_male = 0.2*male_patients_receiving_FV+0.1*sealant_male
            cavities_prevented_female = 0.2*female_patients_receiving_FV+0.1*sealant_female
            cavities_prevented_child = 0.2*child__patients_receiving_FV+0.1*sealant_child
            cavities_prevented_adult = 0.2*adult__patients_receiving_FV+0.1*sealant_adult
            cavities_prevented_old = 0.2*old__patients_receiving_FV+0.1*sealant_old
            total_cavities = cavities_prevented_male+cavities_prevented_female

            total_encounter = Encounter.objects.all().count()
            contact_male = Visualization.objects.filter(gender='male').filter(created_at__range=[start_date,end_date],geography_id=location).count()
            contact_female = Visualization.objects.filter(gender='female').filter(created_at__range=[start_date,end_date],geography_id=location).count()
            contact_child = Visualization.objects.filter(age__lt=18).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            contact_adult = Visualization.objects.filter(age__range=(18, 60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            contact_old= Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()
            total_contact = contact_male+contact_female

            return Response([["Number of Cavities Prevented",round(cavities_prevented_male,2), round(cavities_prevented_female,2), round(cavities_prevented_child,2), round(cavities_prevented_adult,2), round(cavities_prevented_old,2),round(total_cavities,2)],\
                ["Contacts", contact_male, contact_female, contact_child, contact_adult, contact_old, total_contact]])
        return Response(serializer.error)
