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
from visualizationapp.serializers.visualization import TreatMentBarGraphVisualization,\
TreatmentStrategicDataSerializer
from django.db.models import Q
from django.db.models import Count
import datetime
# from datetime import datetime
# from datetime import timedelta
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365+18)
greaterthan60 = d - datetime.timedelta(days=365+60)

today_date = datetime.date.today()
last_30_days = datetime.date.today() + datetime.timedelta(-30)

today_date_obj = str(NepaliDate.from_date(today_date))
last_30_days_obj = str(NepaliDate.from_date(last_30_days))

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class TreatmentTableBasicData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatmentStrategicDataSerializer
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            treatment_obj = Treatment.objects.all().count()

            treatment_male = Visualization.objects.filter(gender='male',created_at__range=[last_30_days_obj,today_date_obj]).count()
            treatment_female = Visualization.objects.filter(gender='female',created_at__range=[last_30_days_obj,today_date_obj]).count()
            treatment_child = Visualization.objects.filter(age__lt=18,created_at__range=[last_30_days_obj,today_date_obj]).count()
            treatment_adult = Visualization.objects.filter(age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            treatment_old = Visualization.objects.filter(age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_fv = Visualization.objects.filter(fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            female_patients_receiving_FV=Visualization.objects.filter(gender='female',fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            male_patients_receiving_FV=Visualization.objects.filter(gender='male',fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            child__patients_receiving_FV = Visualization.objects.filter(age__lt=18,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult__patients_receiving_FV = Visualization.objects.filter(age__range=(18,60),fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old__patients_receiving_FV = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_need_sealant = Visualization.objects.filter(need_sealant=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sealant_male = Visualization.objects.filter(gender='male',need_sealant=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sealant_female = Visualization.objects.filter(gender='female',need_sealant=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sealant_child = Visualization.objects.filter(age__lt=18,need_sealant=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sealant_adult = Visualization.objects.filter(age__range=(18, 60),need_sealant=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sealant_old = Visualization.objects.filter(age__gt=60,need_sealant=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            cavities_prevented_male = 0.2+male_patients_receiving_FV+0.1+sealant_male
            cavities_prevented_female = 0.2+female_patients_receiving_FV+0.1+sealant_female
            cavities_prevented_child = 0.2+child__patients_receiving_FV+0.1+sealant_child
            cavities_prevented_adult = 0.2+adult__patients_receiving_FV+0.1+sealant_adult
            cavities_prevented_old = 0.2+old__patients_receiving_FV+0.1+sealant_old
            total_cavities = cavities_prevented_male+cavities_prevented_female

            total_encounter = Encounter.objects.all().count()
            contact_male = Visualization.objects.filter(gender='male',created_at__range=[last_30_days_obj,today_date_obj]).count()
            contact_female = Visualization.objects.filter(gender='female',created_at__range=[last_30_days_obj,today_date_obj]).count()
            contact_child = Visualization.objects.filter(age__lt=18,created_at__range=[last_30_days_obj,today_date_obj]).count()
            contact_adult = Visualization.objects.filter(age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            contact_old= Visualization.objects.filter(age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_contact = contact_male+contact_female

            return Response([["Number of Cavities Prevented",round(cavities_prevented_male,2), round(cavities_prevented_female,2), round(cavities_prevented_child,2), round(cavities_prevented_adult,2), round(cavities_prevented_old,2),round(total_cavities,2)],\
                ["Contacts", contact_male, contact_female, contact_child, contact_adult, contact_old, total_contact]])
        return Response({"treatment_obj":"do not have a permission"},status=400)

    def post(self, request, format=None):
        serializer = TreatmentStrategicDataSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']
            health_post = serializer.validated_data['health_post']
            seminar = serializer.validated_data['seminar']
            outreach = serializer.validated_data['outreach']
            training = serializer.validated_data['training']

            if location=="All Location":
                treatment_male = Visualization.objects.filter(gender='male',created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_female = Visualization.objects.filter(gender='female',created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_child = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_adult = Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_old = Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                total_fv = Visualization.objects.filter(fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                female_patients_receiving_FV=Visualization.objects.filter(gender='female',fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                male_patients_receiving_FV=Visualization.objects.filter(gender='male',fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                child__patients_receiving_FV = Visualization.objects.filter(age__lt=18,fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                adult__patients_receiving_FV = Visualization.objects.filter(age__range=(18,60),fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                old__patients_receiving_FV = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                total_need_sealant = Visualization.objects.filter(need_sealant=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_male = Visualization.objects.filter(gender='male',need_sealant=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_female = Visualization.objects.filter(gender='female',need_sealant=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_child = Visualization.objects.filter(age__lt=18,need_sealant=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_adult = Visualization.objects.filter(age__range=(18, 60),need_sealant=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_old = Visualization.objects.filter(age__gt=60,need_sealant=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                cavities_prevented_male = 0.2+male_patients_receiving_FV+0.1+sealant_male
                cavities_prevented_female = 0.2+female_patients_receiving_FV+0.1+sealant_female
                cavities_prevented_child = 0.2+child__patients_receiving_FV+0.1+sealant_child
                cavities_prevented_adult = 0.2+adult__patients_receiving_FV+0.1+sealant_adult
                cavities_prevented_old = 0.2+old__patients_receiving_FV+0.1+sealant_old
                total_cavities = cavities_prevented_male+cavities_prevented_female

                contact_male = Visualization.objects.filter(gender='male',created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_female = Visualization.objects.filter(gender='female',created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_child = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_adult = Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_old= Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_contact = contact_male+contact_female
            else:
                treatment_male = Visualization.objects.filter(gender='male',created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_female = Visualization.objects.filter(gender='female',created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_child = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_adult = Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                treatment_old = Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                total_fv = Visualization.objects.filter(fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                female_patients_receiving_FV=Visualization.objects.filter(gender='female',fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                male_patients_receiving_FV=Visualization.objects.filter(gender='male',fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                child__patients_receiving_FV = Visualization.objects.filter(age__lt=18,fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                adult__patients_receiving_FV = Visualization.objects.filter(age__range=(18,60),fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                old__patients_receiving_FV = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                total_need_sealant = Visualization.objects.filter(need_sealant=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_male = Visualization.objects.filter(gender='male',need_sealant=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_female = Visualization.objects.filter(gender='female',need_sealant=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_child = Visualization.objects.filter(age__lt=18,need_sealant=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_adult = Visualization.objects.filter(age__range=(18, 60),need_sealant=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                sealant_old = Visualization.objects.filter(age__gt=60,need_sealant=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                cavities_prevented_male = 0.2+male_patients_receiving_FV+0.1+sealant_male
                cavities_prevented_female = 0.2+female_patients_receiving_FV+0.1+sealant_female
                cavities_prevented_child = 0.2+child__patients_receiving_FV+0.1+sealant_child
                cavities_prevented_adult = 0.2+adult__patients_receiving_FV+0.1+sealant_adult
                cavities_prevented_old = 0.2+old__patients_receiving_FV+0.1+sealant_old
                total_cavities = cavities_prevented_male+cavities_prevented_female

                # total_encounter = Encounter.objects.filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_male = Visualization.objects.filter(gender='male',created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_female = Visualization.objects.filter(gender='female',created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_child = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_adult = Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                contact_old= Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_contact = contact_male+contact_female
            return Response([["Number of Cavities Prevented",round(cavities_prevented_male,2), round(cavities_prevented_female,2), round(cavities_prevented_child,2), round(cavities_prevented_adult,2), round(cavities_prevented_old,2),round(total_cavities,2)],\
                ["Contacts", contact_male, contact_female, contact_child, contact_adult, contact_old, total_contact]])
        return Response(serializer.error)


class TreatmentStrategicData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatmentStrategicDataSerializer
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            encounter_male = Visualization.objects.values('encounter_id').annotate(Count('encounter_id')).filter(gender='male',created_at__range=[last_30_days_obj,today_date_obj]).count()
            encounter_female = Visualization.objects.values('encounter_id').annotate(Count('encounter_id')).filter(gender='female',created_at__range=[last_30_days_obj,today_date_obj]).count()
            encounter_child = Visualization.objects.values('encounter_id').annotate(Count('encounter_id')).filter(age__lt=18,created_at__range=[last_30_days_obj,today_date_obj]).count()
            encounter_adult = Visualization.objects.values('encounter_id').annotate(Count('encounter_id')).filter(age__range=(18, 60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            encounter_old = Visualization.objects.values('encounter_id').annotate(Count('encounter_id')).filter(age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_refer = Visualization.objects.filter(refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_male = Visualization.objects.filter(gender='male',refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_female = Visualization.objects.filter(gender='female',refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_child = Visualization.objects.filter(age__lt=18,refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_adult = Visualization.objects.filter(age__range=(18,60),refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_old = Visualization.objects.filter(age__gt=60,refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_refer = Visualization.objects.filter(refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_seal_male = Visualization.objects.filter(gender='male',seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_seal_female = Visualization.objects.filter(gender='female',seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_seal_child = Visualization.objects.filter(age__lt=18,seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_seal_adult = Visualization.objects.filter(age__range=(18,60),seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_seal_old = Visualization.objects.filter(age__gt=60,seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            totalfv_male = Visualization.objects.filter(gender='male',fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            totalfv_female = Visualization.objects.filter(gender='female',fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            totalfv_child = Visualization.objects.filter(age__lt=18,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            totalfv_adult = Visualization.objects.filter(age__range=(18,60),fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            totalfv_old = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_exo_male = Visualization.objects.filter(gender='male',exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_exo_female = Visualization.objects.filter(gender='female',exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_exo_child = Visualization.objects.filter(age__lt=18,exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_exo_adult = Visualization.objects.filter(age__range=(18,60),exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_exo_old = Visualization.objects.filter(age__gt=60,exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_art_male = Visualization.objects.filter(gender='male',art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_art_female = Visualization.objects.filter(gender='female',art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_art_child = Visualization.objects.filter(age__lt=18,art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_art_adult = Visualization.objects.filter(age__range=(18,60),art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_art_old = Visualization.objects.filter(age__gt=60,art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_sdf_male = Visualization.objects.filter(gender='male',sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_sdf_female = Visualization.objects.filter(gender='female',sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_sdf_child = Visualization.objects.filter(age__lt=18,sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_sdf_adult = Visualization.objects.filter(age__range=(18,60),sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            total_sdf_old = Visualization.objects.filter(age__gt=60,sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()

            try:
                preventive_ratio_male = (total_seal_male+totalfv_male)/(total_exo_male+total_art_male+total_sdf_male)
            except:
                preventive_ratio_male=0
            try:
                preventive_ratio_female = (total_seal_female+totalfv_female)/(total_exo_female+total_art_female+total_sdf_female)
            except:
                preventive_ratio_female=0
            try:
                preventive_ratio_child = (total_seal_child+totalfv_child)/(total_exo_child+total_art_child+total_sdf_child)
            except:
                preventive_ratio_child=0
            try:
                preventive_ratio_adult = (total_seal_adult+totalfv_adult)/(total_exo_adult+total_art_adult+total_sdf_adult)
            except:
                preventive_ratio_adult=0
            try:
                preventive_ratio_old = (total_seal_old+totalfv_old)/(total_exo_old+total_art_old+total_sdf_old)
            except:
                preventive_ratio_old=0

            preventive_ratio_total = preventive_ratio_male + preventive_ratio_female


            try:
                early_intervention_ratio_male = (total_art_male+total_sdf_male)/total_exo_male
            except:
                early_intervention_ratio_male=0

            try:
                early_intervention_ratio_female = (total_art_female+total_sdf_female)/total_exo_female
            except:
                early_intervention_ratio_female=0

            try:
                early_intervention_ratio_child = (total_art_child+total_sdf_child)/total_exo_child
            except:
                early_intervention_ratio_child=0

            try:
                early_intervention_ratio_adult = (total_art_adult+total_sdf_adult)/total_exo_adult
            except:
                early_intervention_ratio_adult=0

            try:
                early_intervention_ratio_old = (total_art_old+total_sdf_old)/total_exo_old
            except:
                early_intervention_ratio_old=0

            early_intervention_ratio_total = early_intervention_ratio_male+early_intervention_ratio_female

            try:
                recall_percent_male = (refer_male/encounter_male)*100
            except:
                recall_percent_male=0

            try:
                recall_percent_female = (refer_female/encounter_female)*100
            except:
                recall_percent_female=0

            try:
                recall_percent_child = (refer_child/encounter_child)*100
            except:
                recall_percent_child=0

            try:
                recall_percent_adult = (refer_adult/encounter_adult)*100
            except:
                recall_percent_adult=0

            try:
                recall_percent_old = (refer_old/encounter_old)*100
            except:
                recall_percent_old=0

            recall_percent_total = recall_percent_male+recall_percent_female


            return Response([["Preventive Ratio",round(preventive_ratio_male,2), round(preventive_ratio_female,2), round(preventive_ratio_child,2), round(preventive_ratio_adult,2), round(preventive_ratio_old,2),round(preventive_ratio_total,2)],\
                ["Early Intervention Ratio",round(early_intervention_ratio_male,2), round(early_intervention_ratio_female,2), round(early_intervention_ratio_child,2), round(early_intervention_ratio_adult,2), round(early_intervention_ratio_old,2),round(early_intervention_ratio_total,2)],\
                ["% Recall",str(round(recall_percent_male,2))+"%", str(round(recall_percent_female,2))+"%", str(round(recall_percent_child,2))+"%", str(round(recall_percent_adult,2))+"%", str(round(recall_percent_old,2))+"%",str(round(recall_percent_total,2))+"%"]])
        return Response({"treatment_obj":"do not have a permission"},status=400)

    def post(self, request, format=None):
        serializer = TreatmentStrategicDataSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']
            health_post = serializer.validated_data['health_post']
            seminar = serializer.validated_data['seminar']
            outreach = serializer.validated_data['outreach']
            training = serializer.validated_data['training']

            if location=="All Location":
                encounter_male = Visualization.objects.filter(gender='male',created_at__range=[start_date,end_date]).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_female = Visualization.objects.filter(gender='female',created_at__range=[start_date,end_date]).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_child = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date]).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_adult = Visualization.objects.filter(age__range=(18, 60),created_at__range=[start_date,end_date]).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_old = Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date]).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                refer_male = Visualization.objects.filter(gender='male',refer_hp=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_female = Visualization.objects.filter(gender='female',refer_hp=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_child = Visualization.objects.filter(age__lt=18,refer_hp=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_adult = Visualization.objects.filter(age__range=(18,60),refer_hp=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_old = Visualization.objects.filter(age__gt=60,refer_hp=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                total_refer = Visualization.objects.filter(refer_hp=True,created_at__range=[start_date,end_date]).count()
                total_seal_male = Visualization.objects.filter(gender='male',seal=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_female = Visualization.objects.filter(gender='female',seal=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_child = Visualization.objects.filter(age__lt=18,seal=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_adult = Visualization.objects.filter(age__range=(18,60),seal=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_old = Visualization.objects.filter(age__gt=60,seal=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                totalfv_male = Visualization.objects.filter(gender='male',fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_female = Visualization.objects.filter(gender='female',fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_child = Visualization.objects.filter(age__lt=18,fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_adult = Visualization.objects.filter(age__range=(18,60),fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_adult = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                total_exo_male = Visualization.objects.filter(gender='male',exo=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_female = Visualization.objects.filter(gender='female',exo=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_child = Visualization.objects.filter(age__lt=18,exo=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_adult = Visualization.objects.filter(age__range=(18,60),exo=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_old = Visualization.objects.filter(age__gt=60,exo=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                total_art_male = Visualization.objects.filter(gender='male',art=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_female = Visualization.objects.filter(gender='female',art=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_child = Visualization.objects.filter(age__lt=18,art=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_adult = Visualization.objects.filter(age__range=(18,60),art=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_old = Visualization.objects.filter(age__gt=60,art=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                total_sdf_male = Visualization.objects.filter(gender='male',sdf=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_female = Visualization.objects.filter(gender='female',sdf=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_child = Visualization.objects.filter(age__lt=18,sdf=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_adult = Visualization.objects.filter(age__range=(18,60),sdf=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_old = Visualization.objects.filter(age__gt=60,sdf=True,created_at__range=[start_date,end_date]).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                try:
                    preventive_ratio_male = (total_seal_male+totalfv_male)/(total_exo_male+total_art_male+total_sdf_male)
                except:
                    preventive_ratio_male=0
                try:
                    preventive_ratio_female = (total_seal_female+totalfv_female)/(total_exo_female+total_art_female+total_sdf_female)
                except:
                    preventive_ratio_female=0
                try:
                    preventive_ratio_child = (total_seal_child+totalfv_child)/(total_exo_child+total_art_child+total_sdf_child)
                except:
                    preventive_ratio_child=0
                try:
                    preventive_ratio_adult = (total_seal_adult+totalfv_adult)/(total_exo_adult+total_art_adult+total_sdf_adult)
                except:
                    preventive_ratio_adult=0
                try:
                    preventive_ratio_old = (total_seal_old+totalfv_old)/(total_exo_old+total_art_old+total_sdf_old)
                except:
                    preventive_ratio_old=0

                preventive_ratio_total = preventive_ratio_male+preventive_ratio_female


                try:
                    early_intervention_ratio_male = (total_art_male+total_sdf_male)/total_exo_male
                except:
                    early_intervention_ratio_male=0

                try:
                    early_intervention_ratio_female = (total_art_female+total_sdf_female)/total_exo_female
                except:
                    early_intervention_ratio_female=0

                try:
                    early_intervention_ratio_child = (total_art_child+total_sdf_child)/total_exo_child
                except:
                    early_intervention_ratio_child=0

                try:
                    early_intervention_ratio_adult = (total_art_adult+total_sdf_adult)/total_exo_adult
                except:
                    early_intervention_ratio_adult=0

                try:
                    early_intervention_ratio_old = (total_art_old+total_sdf_old)/total_exo_old
                except:
                    early_intervention_ratio_old=0

                early_intervention_ratio_total = early_intervention_ratio_male+early_intervention_ratio_female

                try:
                    recall_percent_male = (refer_male/encounter_male)*100
                except:
                    recall_percent_male=0

                try:
                    recall_percent_female = (refer_female/encounter_female)*100
                except:
                    recall_percent_female=0

                try:
                    recall_percent_child = (refer_child/encounter_child)*100
                except:
                    recall_percent_child=0

                try:
                    recall_percent_adult = (refer_adult/encounter_adult)*100
                except:
                    recall_percent_adult=0

                try:
                    recall_percent_old = (refer_old/encounter_old)*100
                except:
                    recall_percent_old=0

                recall_percent_total = recall_percent_male+recall_percent_female
            else:
                encounter_male = Visualization.objects.filter(gender='male',created_at__range=[start_date,end_date],geography_id=location).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_female = Visualization.objects.filter(gender='female',created_at__range=[start_date,end_date],geography_id=location).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_child = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date],geography_id=location).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_adult = Visualization.objects.filter(age__range=(18, 60),created_at__range=[start_date,end_date],geography_id=location).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                encounter_old = Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],geography_id=location).values('encounter_id').annotate(Count('encounter_id')).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                refer_male = Visualization.objects.filter(gender='male',refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_female = Visualization.objects.filter(gender='female',refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_child = Visualization.objects.filter(age__lt=18,refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_adult = Visualization.objects.filter(age__range=(18,60),refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                refer_old = Visualization.objects.filter(age__gt=60,refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                total_refer = Visualization.objects.filter(refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).count()
                total_seal_male = Visualization.objects.filter(gender='male',seal=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_female = Visualization.objects.filter(gender='female',seal=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_child = Visualization.objects.filter(age__lt=18,seal=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_adult = Visualization.objects.filter(age__range=(18,60),seal=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_seal_old = Visualization.objects.filter(age__gt=60,seal=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                totalfv_male = Visualization.objects.filter(gender='male',fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_female = Visualization.objects.filter(gender='female',fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_child = Visualization.objects.filter(age__lt=18,fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_adult = Visualization.objects.filter(age__range=(18,60),fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                totalfv_adult = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                total_exo_male = Visualization.objects.filter(gender='male',exo=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_female = Visualization.objects.filter(gender='female',exo=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_child = Visualization.objects.filter(age__lt=18,exo=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_adult = Visualization.objects.filter(age__range=(18,60),exo=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_exo_old = Visualization.objects.filter(age__gt=60,exo=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                total_art_male = Visualization.objects.filter(gender='male',art=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_female = Visualization.objects.filter(gender='female',art=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_child = Visualization.objects.filter(age__lt=18,art=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_adult = Visualization.objects.filter(age__range=(18,60),art=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_art_old = Visualization.objects.filter(age__gt=60,art=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                total_sdf_male = Visualization.objects.filter(gender='male',sdf=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_female = Visualization.objects.filter(gender='female',sdf=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_child = Visualization.objects.filter(age__lt=18,sdf=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_adult = Visualization.objects.filter(age__range=(18,60),sdf=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                total_sdf_old = Visualization.objects.filter(age__gt=60,sdf=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                try:
                    preventive_ratio_male = (total_seal_male+totalfv_male)/(total_exo_male+total_art_male+total_sdf_male)
                except:
                    preventive_ratio_male=0
                try:
                    preventive_ratio_female = (total_seal_female+totalfv_female)/(total_exo_female+total_art_female+total_sdf_female)
                except:
                    preventive_ratio_female=0
                try:
                    preventive_ratio_child = (total_seal_child+totalfv_child)/(total_exo_child+total_art_child+total_sdf_child)
                except:
                    preventive_ratio_child=0
                try:
                    preventive_ratio_adult = (total_seal_adult+totalfv_adult)/(total_exo_adult+total_art_adult+total_sdf_adult)
                except:
                    preventive_ratio_adult=0
                try:
                    preventive_ratio_old = (total_seal_old+totalfv_old)/(total_exo_old+total_art_old+total_sdf_old)
                except:
                    preventive_ratio_old=0

                preventive_ratio_total = preventive_ratio_male+preventive_ratio_female+preventive_ratio_child+preventive_ratio_old


                try:
                    early_intervention_ratio_male = (total_art_male+total_sdf_male)/total_exo_male
                except:
                    early_intervention_ratio_male=0

                try:
                    early_intervention_ratio_female = (total_art_female+total_sdf_female)/total_exo_female
                except:
                    early_intervention_ratio_female=0

                try:
                    early_intervention_ratio_child = (total_art_child+total_sdf_child)/total_exo_child
                except:
                    early_intervention_ratio_child=0

                try:
                    early_intervention_ratio_adult = (total_art_adult+total_sdf_adult)/total_exo_adult
                except:
                    early_intervention_ratio_adult=0

                try:
                    early_intervention_ratio_old = (total_art_old+total_sdf_old)/total_exo_old
                except:
                    early_intervention_ratio_old=0

                early_intervention_ratio_total = early_intervention_ratio_male+early_intervention_ratio_female+early_intervention_ratio_child+early_intervention_ratio_adult+early_intervention_ratio_old

                try:
                    recall_percent_male = (refer_male/encounter_male)*100
                except:
                    recall_percent_male=0

                try:
                    recall_percent_female = (refer_female/encounter_female)*100
                except:
                    recall_percent_female=0

                try:
                    recall_percent_child = (refer_child/encounter_child)*100
                except:
                    recall_percent_child=0

                try:
                    recall_percent_adult = (refer_adult/encounter_adult)*100
                except:
                    recall_percent_adult=0

                try:
                    recall_percent_old = (refer_old/encounter_old)*100
                except:
                    recall_percent_old=0

                recall_percent_total = recall_percent_male+recall_percent_female
            return Response([["Preventive Ratio",round(preventive_ratio_male,2), round(preventive_ratio_female,2), round(preventive_ratio_child,2), round(preventive_ratio_adult,2), round(preventive_ratio_old,2),round(preventive_ratio_total,2)],\
                ["Early Intervention Ratio",round(early_intervention_ratio_male,2), round(early_intervention_ratio_female,2), round(early_intervention_ratio_child,2), round(early_intervention_ratio_adult,2), round(early_intervention_ratio_old,2),round(early_intervention_ratio_total,2)],\
                ["% Recall",str(round(recall_percent_male,2))+"%", str(round(recall_percent_female,2))+"%", str(round(recall_percent_child,2))+"%", str(round(recall_percent_adult,2))+"%", str(round(recall_percent_old,2))+"%",str(round(recall_percent_total,2))+"%"]])

        return Response(serializer.error)
