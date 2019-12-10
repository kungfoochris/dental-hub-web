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
from django.db.models import Count
from addressapp.models import Activity

np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365+18)
greaterthan60 = d - datetime.timedelta(days=365+60)

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
                # patient_objlist=Patient.objects.all()
                patient_female = Visualization.objects.filter(geography_id=i.id,gender='female').count()
                patient_male = Visualization.objects.filter(geography_id=i.id,gender='male').count()
                total_patient = Visualization.objects.filter(geography_id=i.id).count()
                female_child = Visualization.objects.filter(geography_id=i.id,gender='female',age__lt=18).count()
                female_adult = Visualization.objects.filter(geography_id=i.id,gender='female',age__range=(19,60)).count()
                male_adult = Visualization.objects.filter(geography_id=i.id,gender='male',age__range=(19,60)).count()
                male_child = Visualization.objects.filter(geography_id=i.id,gender='male',age__lt=18).count()
                old_male = Visualization.objects.filter(geography_id=i.id,gender='male',age__gt=60).count()
                old_female = Visualization.objects.filter(geography_id=i.id,gender='female',age__gt=60).count()
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
                    total_treatment = Visualization.objects.values('encounter_id').annotate(Count("encounter_id")).filter(geography_id=i.id).count()
                    treatment_male = Visualization.objects.values('encounter_id').annotate(Count("encounter_id")).filter(gender='male',geography_id=i.id).count()
                    treatment_female = Visualization.objects.values('encounter_id').annotate(Count("encounter_id")).filter(gender='female',geography_id=i.id).count()
                    treatment_child = Visualization.objects.values('encounter_id').annotate(Count("encounter_id")).filter(age__lt=18,geography_id=i.id).count()
                    treatment_adult = Visualization.objects.values('encounter_id').annotate(Count("encounter_id")).filter(age__range=(18, 60),geography_id=i.id).count()
                    treatment_old = Visualization.objects.values('encounter_id').annotate(Count("encounter_id")).filter(age__gt=60,geography_id=i.id).count()

                    female_patients_receiving_FV=Visualization.objects.filter(gender='female',fv=True,geography_id=i.id).count()
                    male_patients_receiving_FV=Visualization.objects.filter(gender='male',fv=True,geography_id=i.id).count()
                    child__patients_receiving_FV = Visualization.objects.filter(age__lt=18,fv=True,geography_id=i.id).count()
                    adult__patients_receiving_FV = Visualization.objects.filter(age__range=(18, 60),fv=True,geography_id=i.id).count()
                    old__patients_receiving_FV = Visualization.objects.filter(age__gt=60,fv=True,geography_id=i.id).count()

                    sealant_male = Visualization.objects.filter(gender='male',need_sealant=True,geography_id=i.id).count()
                    sealant_female = Visualization.objects.filter(gender='female',need_sealant=True,geography_id=i.id).count()
                    sealant_child = Visualization.objects.filter(age__lt=18,need_sealant=True,geography_id=i.id).count()
                    sealant_adult = Visualization.objects.filter(age__range=(18, 60),need_sealant=True,geography_id=i.id).count()
                    sealant_old = Visualization.objects.filter(age__gt=60,need_sealant=True,geography_id=i.id).count()

                    cavities_prevented_male = 0.2+male_patients_receiving_FV+0.1+sealant_male
                    cavities_prevented_female = 0.2+female_patients_receiving_FV+0.1+sealant_female
                    cavities_prevented_child = 0.2+child__patients_receiving_FV+0.1+sealant_child
                    cavities_prevented_adult = 0.2+adult__patients_receiving_FV+0.1+sealant_adult
                    cavities_prevented_old = 0.2+old__patients_receiving_FV+0.1+sealant_old
                    total_cavities = cavities_prevented_male+cavities_prevented_female


                    return Response([["Number of Cavities Prevented",round(cavities_prevented_male,2), round(cavities_prevented_female,2), round(cavities_prevented_child,2), round(cavities_prevented_adult,2), round(cavities_prevented_old,2),round(total_cavities,2)],\
                        ["Contacts", round(treatment_male,2), round(treatment_female,2), round(treatment_child,2), round(treatment_adult,2), round(treatment_old,2), round(total_treatment,2)]])
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

                    total_fv = Visualization.objects.filter(fv=True,geography_id=i.id).count()
                    totalfv_male = Visualization.objects.filter(gender='male',fv=True,geography_id=i.id).count()
                    totalfv_female = Visualization.objects.filter(gender='female',fv=True,geography_id=i.id).count()
                    totalfv_child = Visualization.objects.filter(age__lt=18,fv=True,geography_id=i.id).count()
                    totalfv_adult = Visualization.objects.filter(age__range=(18,60),fv=True,geography_id=i.id).count()
                    totalfv_old = Visualization.objects.filter(age__gt=60,fv=True,geography_id=i.id).count()


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
            health_post_obj = Activity.objects.get(name="Health Post")
            seminar_obj = Activity.objects.get(name="School Seminar")
            outreach_obj = Activity.objects.get(name="Community Outreach")
            training_obj = Activity.objects.get(name="Training")
            for i in customuser_obj.location.all():
                health_post=[]
                school_seminar=[]
                community=[]
                training=[]
                health_count = Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=i.id).count()
                school_count = Visualization.objects.filter(activities_id=seminar_obj.id,geography_id=i.id).count()
                community_count = Visualization.objects.filter(activities_id=outreach_obj.id,geography_id=i.id).count()
                training_count = Visualization.objects.filter(activities_id=training_obj.id,geography_id=i.id).count()
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
                    total_sdf = Visualization.objects.filter(geography_id=i.id,sdf=True).count()
                    total_sdf_male = Visualization.objects.filter(geography_id=i.id,sdf=True,gender="male").count()
                    total_sdf_female = Visualization.objects.filter(geography_id=i.id,sdf=True,gender="female").count()


                    total_seal = Visualization.objects.filter(geography_id=i.id,seal=True).count()
                    total_seal_male = Visualization.objects.filter(geography_id=i.id,seal=True,gender="male").count()
                    total_seal_female = Visualization.objects.filter(geography_id=i.id,seal=True,gender="female").count()

                    total_art = Visualization.objects.filter(geography_id=i.id,art=True).count()
                    total_art_male = Visualization.objects.filter(geography_id=i.id,art=True,gender="male").count()
                    total_art_female = Visualization.objects.filter(geography_id=i.id,art=True,gender="female").count()

                    total_exo = Visualization.objects.filter(geography_id=i.id,exo=True).count()
                    total_exo_male = Visualization.objects.filter(geography_id=i.id,exo=True,gender="male").count()
                    total_exo_female = Visualization.objects.filter(geography_id=i.id,exo=True,gender="female").count()

                    total_fv = Visualization.objects.filter(geography_id=i.id,fv=True).count()
                    totalfv_male = Visualization.objects.filter(geography_id=i.id,fv=True,gender="male").count()
                    totalfv_female = Visualization.objects.filter(geography_id=i.id,fv=True,gender="female").count()
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
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        total_patient = Visualization.objects.filter(geography_id=i.id,created_at__month=x).count()
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


class WardStrategicData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if CustomUser.objects.select_related('role').filter(id=request.user.id,role__name='warduser').exists():
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                encounter_male = Visualization.objects.filter(gender='male',geography_id=i.id).values('encounter_id').annotate(Count('encounter_id')).count()
                encounter_female = Visualization.objects.filter(gender='female',geography_id=i.id).values('encounter_id').annotate(Count('encounter_id')).count()
                encounter_child = Visualization.objects.filter(age__lt=18,geography_id=i.id).values('encounter_id').annotate(Count('encounter_id')).count()
                encounter_adult = Visualization.objects.filter(age__range=(18, 60),geography_id=i.id).values('encounter_id').annotate(Count('encounter_id')).count()
                encounter_old = Visualization.objects.filter(age__gt=60,geography_id=i.id).values('encounter_id').annotate(Count('encounter_id')).count()

                total_refer = Visualization.objects.filter(refer_hp=True,geography_id=i.id).count()
                refer_male = Visualization.objects.filter(gender='male',refer_hp=True,geography_id=i.id).count()
                refer_female = Visualization.objects.filter(gender='female',refer_hp=True,geography_id=i.id).count()
                refer_child = Visualization.objects.filter(age__lt=18,refer_hp=True,geography_id=i.id).count()
                refer_adult = Visualization.objects.filter(age__range=(18,60),refer_hp=True,geography_id=i.id).count()
                refer_old = Visualization.objects.filter(age__gt=60,refer_hp=True,geography_id=i.id).count()

                total_refer = Visualization.objects.filter(refer_hp=True,geography_id=i.id).count()
                total_seal_male = Visualization.objects.filter(gender='male',seal=True,geography_id=i.id).count()
                total_seal_female = Visualization.objects.filter(gender='female',seal=True,geography_id=i.id).count()
                total_seal_child = Visualization.objects.filter(age__lt=18,seal=True,geography_id=i.id).count()
                total_seal_adult = Visualization.objects.filter(age__range=(18,60),seal=True,geography_id=i.id).count()
                total_seal_old = Visualization.objects.filter(age__gt=60,seal=True,geography_id=i.id).count()

                totalfv_male = Visualization.objects.filter(gender='male',fv=True,geography_id=i.id).count()
                totalfv_female = Visualization.objects.filter(gender='female',fv=True,geography_id=i.id).count()
                totalfv_child = Visualization.objects.filter(age__lt=18,fv=True,geography_id=i.id).count()
                totalfv_adult = Visualization.objects.filter(age__range=(18,60),fv=True,geography_id=i.id).count()
                totalfv_adult = Visualization.objects.filter(age__gt=60,fv=True,geography_id=i.id).count()

                total_exo_male = Visualization.objects.filter(gender='male',exo=True,geography_id=i.id).count()
                total_exo_female = Visualization.objects.filter(gender='female',exo=True,geography_id=i.id).count()
                total_exo_child = Visualization.objects.filter(age__lt=18,exo=True,geography_id=i.id).count()
                total_exo_adult = Visualization.objects.filter(age__range=(18,60),exo=True,geography_id=i.id).count()
                total_exo_old = Visualization.objects.filter(age__gt=60,exo=True,geography_id=i.id).count()


                total_art_male = Visualization.objects.filter(gender='male',art=True,geography_id=i.id).count()
                total_art_female = Visualization.objects.filter(gender='female',art=True,geography_id=i.id).count()
                total_art_child = Visualization.objects.filter(age__lt=18,art=True,geography_id=i.id).count()
                total_art_adult = Visualization.objects.filter(age__range=(18,60),art=True,geography_id=i.id).count()
                total_art_old = Visualization.objects.filter(age__gt=60,art=True,geography_id=i.id).count()


                total_sdf_male = Visualization.objects.filter(gender='male',sdf=True,geography_id=i.id).count()
                total_sdf_female = Visualization.objects.filter(gender='female',sdf=True,geography_id=i.id).count()
                total_sdf_child = Visualization.objects.filter(age__lt=18,sdf=True,geography_id=i.id).count()
                total_sdf_adult = Visualization.objects.filter(age__range=(18,60),sdf=True,geography_id=i.id).count()
                total_sdf_old = Visualization.objects.filter(age__gt=60,sdf=True,geography_id=i.id).count()

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


            return Response([["Preventive Ratio",round(preventive_ratio_male,2), round(preventive_ratio_female,2), round(preventive_ratio_child,2), round(preventive_ratio_adult,2), round(preventive_ratio_old,2),round(preventive_ratio_total,2)],\
                ["Early Intervention Ratio",round(early_intervention_ratio_male,2), round(early_intervention_ratio_female,2), round(early_intervention_ratio_child,2), round(early_intervention_ratio_adult,2), round(early_intervention_ratio_old,2),round(early_intervention_ratio_total,2)],\
                ["% Recall",str(round(recall_percent_male,2))+"%", str(round(recall_percent_female,2))+"%", str(round(recall_percent_child,2))+"%", str(round(recall_percent_adult,2))+"%", str(round(recall_percent_old,2))+"%",str(round(recall_percent_total,2))+"%"]])
        return Response({"treatment_obj":"do not have a permission"},status=400)
