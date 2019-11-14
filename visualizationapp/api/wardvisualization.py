import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from patientapp.models import Patient
from treatmentapp.serializers.visualization import VisualizatioSerializer
from addressapp.models import Geography


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.conf import settings
from dental.settings import MEDIA_ROOT
import os
from django.http import JsonResponse
from nepali.datetime import NepaliDate
import datetime

from django.db.models import Q
from treatmentapp.models import Treatment

from encounterapp.models import Encounter, History, Refer, Screeing

from visualizationapp.models import Visualization

np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365*18)
greaterthan60 = d - datetime.timedelta(days=365*60)

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)



class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class WardVisualization1(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if CustomUser.objects.select_related('role').filter(id=request.user.id,role__name='warduser'):
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                print(i)
                district=['Kids', 'Adults', 'Other Adults']
                total=[]
                male=[]
                female=[]
                patient_objlist=Patient.objects.all()
                patient_female = Patient.objects.select_related('geography').filter(geography=i,gender='female').count()
                patient_male = Patient.objects.select_related('geography').filter(geography=i,gender='male').count()
                total_patient = Patient.objects.select_related('geography').filter(geography=i).count()
                female_child = Patient.objects.select_related('geography').filter(geography=i,gender='female',dob__gt=lessthan18).count()
                female_adult = Patient.objects.select_related('geography').filter(geography=i,gender='female',dob__range=(greaterthan60,lessthan18)).count()
                male_adult = Patient.objects.select_related('geography').filter(geography=i,gender='male',dob__range=(greaterthan60,lessthan18)).count()
                male_child = Patient.objects.select_related('geography').filter(geography=i,gender='male',dob__gt=lessthan18).count()
                old_male = patient_male-male_adult-male_child
                old_female = patient_female-female_child-female_adult
                male.append(male_child)
                male.append(male_adult)
                male.append(old_male)
                female.append(female_child)
                female.append(female_adult)
                female.append(old_female)
                total.append(female_child+male_child)
                total.append(female_adult+male_adult)
                total.append(old_female+old_male)

                # male.append()


                locationChart = {
                'data': {
                'labels': district,
                'datasets': [
                {
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
        return Response({"message":"only ward user can see"},status=400)


class WardTreatmentTableVisualization1(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, format=None):
            if CustomUser.objects.select_related('role').filter(id=request.user.id,role__name='warduser').exists():
                customuser_obj = CustomUser.objects.get(id=request.user.id)
                for i in customuser_obj.location.all():
                    treatment_obj = Treatment.objects.all().count()
                    treatment_male = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',encounter_id__geography=i).count()
                    treatment_female = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',encounter_id__geography=i).count()
                    treatment_child = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,encounter_id__geography=i).count()
                    treatment_adult = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),encounter_id__geography=i).count()
                    treatment_old = treatment_obj-treatment_child-treatment_adult

                    total_fv = Treatment.objects.filter(fv_applied=True).count()
                    female_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fv_applied=True,encounter_id__geography=i).count()
                    male_patients_receiving_FV=Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fv_applied=True,encounter_id__geography=i).count()
                    child__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,fv_applied=True,encounter_id__geography=i).count()
                    adult__patients_receiving_FV = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),fv_applied=True,encounter_id__geography=i).count()
                    old__patients_receiving_FV = total_fv-child__patients_receiving_FV-adult__patients_receiving_FV

                    total_need_sealant = Screeing.objects.filter(need_sealant=True).count()
                    sealant_male = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',need_sealant=True,encounter_id__geography=i).count()
                    sealant_female = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',need_sealant=True,encounter_id__geography=i).count()
                    sealant_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,need_sealant=True,encounter_id__geography=i).count()
                    sealant_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),need_sealant=True,encounter_id__geography=i).count()
                    sealant_old = total_need_sealant-sealant_child-sealant_adult

                    cavities_prevented_male = 0.2*male_patients_receiving_FV+0.1*sealant_male
                    cavities_prevented_female = 0.2*female_patients_receiving_FV+0.1*sealant_female
                    cavities_prevented_child = 0.2*child__patients_receiving_FV+0.1*sealant_child
                    cavities_prevented_adult = 0.2*adult__patients_receiving_FV+0.1*sealant_adult
                    cavities_prevented_old = 0.2*old__patients_receiving_FV+0.1*sealant_old
                    total_cavities = cavities_prevented_male+cavities_prevented_female

                    total_encounter = Encounter.objects.all().count()
                    contact_male = Encounter.objects.select_related('patient','geography').filter(patient__gender='male',geography=i).count()
                    contact_female = Encounter.objects.select_related('patient','geography').filter(patient__gender='female',geography=i).count()
                    contact_child = Encounter.objects.select_related('patient','geography').filter(patient__dob__gt=lessthan18,geography=i).count()
                    contact_adult = Encounter.objects.select_related('patient','geography').filter(patient__dob__range=(greaterthan60, lessthan18),geography=i).count()
                    contact_old= total_encounter-contact_child-contact_adult

                    return Response([["Number of Cavities Prevented",cavities_prevented_male, cavities_prevented_female, cavities_prevented_child, cavities_prevented_adult, cavities_prevented_old,total_cavities],\
                        ["Contacts", contact_male, contact_female, contact_child, contact_adult, contact_old, total_encounter]])
            return Response({"treatment_obj":"do not have a permission"},status=400)

class WardTableVisualization2(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, format=None):
            if CustomUser.objects.select_related('role').filter(id=request.user.id,role__name='warduser').exists():
                customuser_obj = CustomUser.objects.get(id=request.user.id)
                for i in customuser_obj.location.all():
                    total_sdf = Visualization.objects.filter(geography_id=i.id,sdf=True).count()
                    total_sdf_male = Visualization.objects.filter(geography_id=i.id,sdf=True,gender='male').count()
                    total_sdf_female = Visualization.objects.filter(geography_id=i.id,sdf=True,gender='female').count()
                    total_sdf_child = Visualization.objects.filter(geography_id=i.id,sdf=True,age__lt=18).count()
                    total_sdf_adult = Visualization.objects.filter(geography_id=i.id,sdf=True,age__range=(18,60)).count()
                    total_sdf_old = Visualization.objects.filter(geography_id=i.id,sdf=True,age__gt=60).count()

                    total_seal = Visualization.objects.filter(geography_id=i.id,seal=True).count()
                    total_seal_male = Visualization.objects.filter(geography_id=i.id,seal=True,gender='male').count()
                    total_seal_female = Visualization.objects.filter(geography_id=i.id,seal=True,gender='female').count()
                    total_seal_child = Visualization.objects.filter(geography_id=i.id,seal=True,age__lt=18).count()
                    total_seal_adult = Visualization.objects.filter(geography_id=i.id,seal=True,age__range=(18,60)).count()
                    total_seal_old = Visualization.objects.filter(geography_id=i.id,seal=True,age__gt=60).count()

                    total_art = Visualization.objects.filter(geography_id=i.id,art=True).count()
                    total_art_male = Visualization.objects.filter(geography_id=i.id,art=True,gender='male').count()
                    total_art_female = Visualization.objects.filter(geography_id=i.id,art=True,gender='female').count()
                    total_art_child = Visualization.objects.filter(geography_id=i.id,art=True,age__lt=18).count()
                    total_art_adult = Visualization.objects.filter(geography_id=i.id,art=True,age__range=(18,60)).count()
                    total_art_old = Visualization.objects.filter(geography_id=i.id,art=True,age__gt=60).count()

                    total_exo = Visualization.objects.filter(geography_id=i.id,exo=True).count()
                    total_exo_male = Visualization.objects.filter(geography_id=i.id,exo=True,gender='male').count()
                    total_exo_female = Visualization.objects.filter(geography_id=i.id,exo=True,gender='female').count()
                    total_exo_child = Visualization.objects.filter(geography_id=i.id,exo=True,age__lt=18).count()
                    total_exo_adult = Visualization.objects.filter(geography_id=i.id,exo=True,age__range=(18,60)).count()
                    total_exo_old = Visualization.objects.filter(geography_id=i.id,exo=True,age__gt=60).count()

                total_fv = Treatment.objects.select_related('encounter_id').filter(fv_applied=True,encounter_id__geography=i).count()
                totalfv_male = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fv_applied=True,encounter_id__geography=i).count()
                totalfv_female = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fv_applied=True,encounter_id__geography=i).count()
                totalfv_child = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,fv_applied=True,encounter_id__geography=i).count()
                totalfv_adult = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60,lessthan18),fv_applied=True,encounter_id__geography=i).count()
                totalfv_old = total_fv-totalfv_child-totalfv_adult


                return Response([["EXO",total_exo_male, total_exo_female, total_exo_child, total_exo_adult,total_exo_old,total_exo],\
                    ["ART",total_art_male, total_art_female,total_art_child, total_art_adult, total_art_old,total_art],\
                    ["SEAL",total_seal_male, total_seal_female, total_seal_child, total_seal_adult, total_seal_old,total_seal],\
                    ["SDF",total_sdf_male, total_sdf_female, total_sdf_child, total_sdf_adult, total_sdf_old,total_sdf],\
                    ["FV",totalfv_male, totalfv_female, totalfv_child, totalfv_adult, totalfv_old,total_fv]])
            return Response({"treatment_obj":"do not have a permission"},status=400)


class WardSettingVisualization(APIView):
      def get(self, request, format=None):
        if CustomUser.objects.select_related('role').filter(id=request.user.id,role__name='warduser').exists():
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                health_post=[]
                school_seminar=[]
                community=[]
                training=[]
                health_count = Patient.objects.select_related('activity_area','geography').filter(activity_area__name='Health Post',geography=i).count()
                school_count = Patient.objects.select_related('activity_area','geography').filter(activity_area__name='School Seminar',geography=i).count()
                community_count = Patient.objects.select_related('activity_area','geography').filter(activity_area__name='Community Outreach',geography=i).count()
                training_count = Patient.objects.select_related('activity_area','geography').filter(activity_area__name='Training',geography=i).count()
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
        return Response({"message":"only ward user can see"},status=400)



class WardTreatmentVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, format=None):
            if CustomUser.objects.select_related('role').filter(id=request.user.id,role__name='warduser').exists():
                customuser_obj = CustomUser.objects.get(id=request.user.id)
                district=['EXO', 'ART', 'SEAL','SDF','FV']
                total=[]
                male=[]
                female=[]
                for i in customuser_obj.location.all():
                    total_sdf = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__geography=i).count()

                    total_sdf_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                        |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                        |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                        |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                        |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                        |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                        |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                        |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__patient__gender='male',encounter_id__geography=i).count()

                    total_sdf_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                        |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                        |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                        |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                        |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                        |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                        |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                        |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__patient__gender='female',encounter_id__geography=i).count()


                    total_seal = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAl') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                        |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                        |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                        |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                        |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                        |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                        |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                        |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__geography=i).count()

                    total_seal_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                        |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                        |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                        |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                        |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                        |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                        |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                        |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__patient__gender='male',encounter_id__geography=i).count()

                    total_seal_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                        |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                        |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                        |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                        |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                        |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                        |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                        |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__patient__gender='female',encounter_id__geography=i).count()

                    total_art = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                        |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                        |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                        |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                        |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                        |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                        |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                        |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__geography=i).count()

                    total_art_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                        |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                        |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                        |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                        |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                        |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                        |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                        |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__patient__gender='male',encounter_id__geography=i).count()

                    total_art_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                        |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                        |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                        |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                        |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                        |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                        |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                        |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__patient__gender='female',encounter_id__geography=i).count()


                    total_exo = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                        |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                        |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                        |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                        |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                        |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                        |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                        |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__geography=i).count()

                    total_exo_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                        |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                        |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                        |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                        |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                        |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                        |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                        |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__patient__gender='male',encounter_id__geography=i).count()

                    total_exo_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                        |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                        |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                        |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                        |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                        |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                        |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                        |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__patient__gender='female',encounter_id__geography=i).count()


                    total_fv = Treatment.objects.select_related('encounter_id').filter(fv_applied=True,encounter_id__geography=i).count()
                    totalfv_male = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fv_applied=True,encounter_id__geography=i).count()
                    totalfv_female = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fv_applied=True,encounter_id__geography=i).count()
                    male.append(total_exo_male)
                    male.append(total_art_male)
                    male.append(total_seal_male)
                    male.append(total_sdf_male)
                    male.append(totalfv_male)
                    female.append(total_exo_female)
                    female.append(total_art_female)
                    female.append(total_seal_female)
                    female.append(total_sdf_female)
                    female.append(totalfv_female)
                    total.append(total_exo)
                    total.append(total_art)
                    total.append(total_seal)
                    total.append(total_sdf)
                    total.append(total_fv)
                locationChart = {
                'data': {
                'labels': district,
                'datasets': [
                {
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
                'text': "Treatment-wise Gender Distribution",
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




class WardUserlineVisualization(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            geography=[]
            geography_patient=[]
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                v=[]
                for x in month:
                    if Patient.objects.filter(geography__id=i.id).exists():
                        total_patient = Patient.objects.filter(geography__id=i.id,created_at__month=x).count()
                        v.append(total_patient)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)"]
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 2.2,
            'title': {
            'display': 'true',
            'text': "Month-wise contact distribution",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"
            },
            'legend': {
            'position': "bottom"
            },
            'labels':{
            'usePointStyle': 'true'
            },
            'scales': {
            'yAxes': [{
            'ticks': {
            'fontColor': "rgba(0,0,0,0.5)",
            'fontStyle': "bold",
            'beginAtZero': 'false',
            'maxTicksLimit': 6,
            'padding': 20
            },
            'gridLines': {
            'drawTicks': 'true',
            'display': 'true'
            }
            }],
            'xAxes': [{
            'gridLines': {
            'zeroLineColor': "transparent"
            },
            'ticks': {
            'padding': 20,
            'fontColor': "rgba(0,0,0,0.5)",
            'fontStyle': "bold"
            }}]}}
            }
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)
