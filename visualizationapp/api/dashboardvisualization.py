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
from encounterapp.models import Screeing,Encounter,Refer

from nepali.datetime import NepaliDate
from django.db.models import DurationField, F, ExpressionWrapper
import datetime
from django.db.models import Q

from visualizationapp.models import Visualization
from addressapp.models import Activity

from visualizationapp.serializers.visualization import OverViewVisualization
import datetime

from visualizationapp.serializers.visualization import TreatMentBarGraphVisualization
from addressapp.models import Address, District, Municipality ,Ward

import logging
# Get an instance of a logger
from django.db.models import Count, Case, When, Value
logger = logging.getLogger(__name__)


np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365*18)
greaterthan60 = d - datetime.timedelta(days=365*60)



today_date = datetime.date.today()
last_30_days = datetime.date.today() + datetime.timedelta(-30)

today_date_obj = str(NepaliDate.from_date(today_date))
last_30_days_obj = str(NepaliDate.from_date(last_30_days))


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class VisualizationSetting(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id):
            district=['Kids','Teen','Adult', 'Old Adult']
            kid_exo = Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_art = Visualization.objects.filter(art=True,age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_seal = Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_sdf = Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_fv = Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_exo = Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_art = Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_seal = Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_sdf = Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_fv = Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_exo = Visualization.objects.filter(exo=True,age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_art = Visualization.objects.filter(art=True,age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_seal = Visualization.objects.filter(seal=True,age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_sdf = Visualization.objects.filter(sdf=True,age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_fv = Visualization.objects.filter(fv=True,age__range=(18,60),created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_adult_exo = Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_adult_art = Visualization.objects.filter(art=True,age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_adult_seal = Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_adult_sdf = Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_adult_fv = Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()

            exo_data=[kid_exo, teen_exo, adult_exo, old_adult_exo]
            fv_data=[kid_fv, teen_fv, adult_fv, old_adult_fv]
            art_data=[kid_art, teen_art, adult_art, old_adult_art]
            seal_data=[kid_seal, teen_seal, adult_seal, old_adult_seal]
            sdf_data=[kid_sdf, teen_sdf, adult_sdf, old_adult_sdf]



            locationChart = {
            'data': {
            'labels': district,
            'datasets': [{
            'label': "EXO",
            'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            'borderColor': 'rgba(255, 206, 86, 1)',
            'borderWidth': 1,
            'data': exo_data},
            {
            'label': "ART",
            'backgroundColor': 'rgba(81, 264, 210, 0.2)',
            'borderColor': 'rgba(81, 264, 210, 1)',
            'borderWidth': 1,
            'data': art_data},
            {
            'label': "SEAL",
            'backgroundColor': 'rgba(16, 152, 247, 0.2)',
            'borderColor': 'rgba(16, 152, 247, 1)',
            'borderWidth': 1,
            'data': seal_data},
            {
            'label': "SDF",
            'backgroundColor': 'rgba(87, 50, 200, 0.2)',
            'borderColor': 'rgba(87, 50, 200, 1)',
            'borderWidth': 1,
            'data': sdf_data},
            {
            'label': "FV",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': fv_data}]
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
            # 'text': "Setting-wise treatment distribution",
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


class VisualizationSettingFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location_list = serializer.validated_data['location']

            district=['Community Outreach','Health Post', 'School Seminar','Training']
            health_post_obj = Activity.objects.get(name="Health Post")
            seminar_obj = Activity.objects.get(name="School Seminar")
            outreach_obj = Activity.objects.get(name="Community Outreach")
            training = Activity.objects.get(name="Training")
            age_group = serializer.validated_data['age_group']
            health_post_exo=[]
            health_post_art=[]
            health_post_seal=[]
            health_post_sdf=[]
            health_post_fv=[]

            seminar_exo=[]
            seminar_art=[]
            seminar_seal=[]
            seminar_sdf=[]
            seminar_fv=[]

            outreach_exo=[]
            outreach_art=[]
            outreach_seal=[]
            outreach_sdf=[]
            outreach_fv=[]

            training_exo=[]
            training_art=[]
            training_seal=[]
            training_sdf=[]
            training_fv=[]

            kid_exo=[]
            kid_art=[]
            kid_seal=[]
            kid_sdf=[]
            kid_fv=[]

            teen_exo=[]
            teen_art=[]
            teen_seal=[]
            teen_sdf=[]
            teen_fv=[]

            adult_exo=[]
            adult_art=[]
            adult_seal=[]
            adult_sdf=[]
            adult_fv=[]

            old_adult_exo=[]
            old_adult_art=[]
            old_adult_seal=[]
            old_adult_sdf=[]
            old_adult_fv=[]
            if not location_list:
                health_post_exo.append(Visualization.objects.filter(exo=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).count())
                health_post_art.append(Visualization.objects.filter(art=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).count())
                health_post_seal.append(Visualization.objects.filter(seal=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).count())
                health_post_sdf.append(Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).count())
                health_post_fv.append(Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).count())

                seminar_exo.append(Visualization.objects.filter(exo=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).count())
                seminar_art.append(Visualization.objects.filter(art=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).count())
                seminar_seal.append(Visualization.objects.filter(seal=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).count())
                seminar_sdf.append(Visualization.objects.filter(sdf=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).count())
                seminar_fv.append(Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).count())

                outreach_exo.append(Visualization.objects.filter(exo=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).count())
                outreach_art.append(Visualization.objects.filter(art=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).count())
                outreach_seal.append(Visualization.objects.filter(seal=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).count())
                outreach_sdf.append(Visualization.objects.filter(sdf=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).count())
                outreach_fv.append(Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).count())

                training_exo.append(Visualization.objects.filter(exo=True,activities_id=training.id).filter(created_at__range=[start_date,end_date]).count())
                training_art.append(Visualization.objects.filter(art=True,activities_id=training.id).filter(created_at__range=[start_date,end_date]).count())
                training_seal.append(Visualization.objects.filter(seal=True,activities_id=training.id).filter(created_at__range=[start_date,end_date]).count())
                training_sdf.append(Visualization.objects.filter(sdf=True,activities_id=training.id).filter(created_at__range=[start_date,end_date]).count())
                training_fv.append(Visualization.objects.filter(fv=True,activities_id=training.id).filter(created_at__range=[start_date,end_date]).count())
                district1=['Kids','Teen','Adult', 'Old Adult']
                kid_exo.append(Visualization.objects.filter(exo=True,age__lt=12).filter(created_at__range=[start_date,end_date]).count())
                kid_art.append(Visualization.objects.filter(art=True,age__lt=12).filter(created_at__range=[start_date,end_date]).count())
                kid_seal.append(Visualization.objects.filter(seal=True,age__lt=12).filter(created_at__range=[start_date,end_date]).count())
                kid_sdf.append(Visualization.objects.filter(sdf=True,age__lt=12).filter(created_at__range=[start_date,end_date]).count())
                kid_fv.append(Visualization.objects.filter(fv=True,age__lt=12).filter(created_at__range=[start_date,end_date]).count())

                teen_exo.append(Visualization.objects.filter(exo=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date]).count())
                teen_art.append(Visualization.objects.filter(art=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date]).count())
                teen_seal.append(Visualization.objects.filter(seal=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date]).count())
                teen_sdf.append(Visualization.objects.filter(sdf=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date]).count())
                teen_fv.append(Visualization.objects.filter(fv=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date]).count())

                adult_exo.append(Visualization.objects.filter(exo=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date]).count())
                adult_art.append(Visualization.objects.filter(art=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date]).count())
                adult_seal.append(Visualization.objects.filter(seal=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date]).count())
                adult_sdf.append(Visualization.objects.filter(sdf=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date]).count())
                adult_fv.append(Visualization.objects.filter(fv=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date]).count())

                old_adult_exo.append(Visualization.objects.filter(exo=True,age__gt=60).filter(created_at__range=[start_date,end_date]).count())
                old_adult_art.append(Visualization.objects.filter(art=True,age__gt=60).filter(created_at__range=[start_date,end_date]).count())
                old_adult_seal.append(Visualization.objects.filter(seal=True,age__gt=60).filter(created_at__range=[start_date,end_date]).count())
                old_adult_sdf.append(Visualization.objects.filter(sdf=True,age__gt=60).filter(created_at__range=[start_date,end_date]).count())
                old_adult_fv.append(Visualization.objects.filter(fv=True,age__gt=60).filter(created_at__range=[start_date,end_date]).count())

            else:
                for location in location_list:
                    health_post_exo.append(Visualization.objects.filter(exo=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    health_post_art.append(Visualization.objects.filter(art=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    health_post_seal.append(Visualization.objects.filter(seal=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    health_post_sdf.append(Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    health_post_fv.append(Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    seminar_exo.append(Visualization.objects.filter(exo=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    seminar_art.append(Visualization.objects.filter(art=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    seminar_seal.append(Visualization.objects.filter(seal=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    seminar_sdf.append(Visualization.objects.filter(sdf=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    seminar_fv.append(Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    outreach_exo.append(Visualization.objects.filter(exo=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    outreach_art.append(Visualization.objects.filter(art=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    outreach_seal.append(Visualization.objects.filter(seal=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    outreach_sdf.append(Visualization.objects.filter(sdf=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    outreach_fv.append(Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    training_exo.append(Visualization.objects.filter(exo=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    training_art.append(Visualization.objects.filter(art=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    training_seal.append(Visualization.objects.filter(seal=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    training_sdf.append(Visualization.objects.filter(sdf=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    training_fv.append(Visualization.objects.filter(fv=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    district1=['Kids','Teen','Adult', 'Old Adult']
                    kid_exo.append(Visualization.objects.filter(exo=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    kid_art.append(Visualization.objects.filter(art=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    kid_seal.append(Visualization.objects.filter(seal=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    kid_sdf.append(Visualization.objects.filter(sdf=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    kid_fv.append(Visualization.objects.filter(fv=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    teen_exo.append(Visualization.objects.filter(exo=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    teen_art.append(Visualization.objects.filter(art=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    teen_seal.append(Visualization.objects.filter(seal=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    teen_sdf.append(Visualization.objects.filter(sdf=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    teen_fv.append(Visualization.objects.filter(fv=True,age__range=(12,19)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    adult_exo.append(Visualization.objects.filter(exo=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    adult_art.append(Visualization.objects.filter(art=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    adult_seal.append(Visualization.objects.filter(seal=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    adult_sdf.append(Visualization.objects.filter(sdf=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    adult_fv.append(Visualization.objects.filter(fv=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    old_adult_exo.append(Visualization.objects.filter(exo=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    old_adult_art.append(Visualization.objects.filter(art=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    old_adult_seal.append(Visualization.objects.filter(seal=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    old_adult_sdf.append(Visualization.objects.filter(sdf=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())
                    old_adult_fv.append(Visualization.objects.filter(fv=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

            exo_data=[sum(outreach_exo),sum(health_post_exo),sum(seminar_exo),sum(training_exo)]
            fv_data=[sum(outreach_fv),sum(health_post_fv),sum(seminar_fv),sum(training_fv)]
            art_data=[sum(outreach_art),sum(health_post_art),sum(seminar_art),sum(training_art)]
            seal_data=[sum(outreach_seal),sum(health_post_seal),sum(seminar_seal),sum(training_seal)]
            sdf_data=[sum(outreach_sdf),sum(health_post_sdf),sum(seminar_sdf),sum(training_sdf)]


            exo_data1=[sum(kid_exo), sum(teen_exo), sum(adult_exo), sum(old_adult_exo)]
            fv_data1=[sum(kid_fv), sum(teen_fv), sum(adult_fv), sum(old_adult_fv)]
            art_data1=[sum(kid_art), sum(teen_art), sum(adult_art), sum(old_adult_art)]
            seal_data1=[sum(kid_seal), sum(teen_seal), sum(adult_seal), sum(old_adult_seal)]
            sdf_data1=[sum(kid_sdf), sum(teen_sdf), sum(adult_sdf), sum(old_adult_sdf)]
            if age_group == "Age Group":
                locationChart = {
                'data': {
                'labels': district1,
                'datasets': [{
                'label': "EXO",
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'borderColor': 'rgba(255, 206, 86, 1)',
                'borderWidth': 1,
                'data': exo_data1},
                {
                'label': "ART",
                'backgroundColor': 'rgba(81, 264, 289, 0.2)',
                'borderColor': 'rgba(81, 264, 210, 1)',
                'borderWidth': 1,
                'data': art_data1},
                {
                'label': "SEAL",
                'backgroundColor': 'rgba(16, 152, 247, 0.2)',
                'borderColor': 'rgba(16, 152, 247, 1)',
                'borderWidth': 1,
                'data': seal_data1},
                {
                'label': "SDF",
                'backgroundColor': 'rgba(87, 50, 200, 0.2)',
                'borderColor': 'rgba(87, 50, 200, 1)',
                'borderWidth': 1,
                'data': sdf_data1},
                {
                'label': "FV",
                'backgroundColor': 'rgba(239, 62, 54, 0.2)',
                'borderColor': 'rgba(239, 62, 54, 1)',
                'borderWidth': 1,
                'data': fv_data1}]
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
                # 'text': "Setting-wise treatment distribution",
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
                }}}}
            else:
                locationChart = {
                'data': {
                'labels': district,
                'datasets': [{
                'label': "EXO",
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'borderColor': 'rgba(255, 206, 86, 1)',
                'borderWidth': 1,
                'data': exo_data},
                {
                'label': "ART",
                'backgroundColor': 'rgba(81, 264, 289, 0.2)',
                'borderColor': 'rgba(81, 264, 210, 1)',
                'borderWidth': 1,
                'data': art_data},
                {
                'label': "SEAL",
                'backgroundColor': 'rgba(16, 152, 247, 0.2)',
                'borderColor': 'rgba(16, 152, 247, 1)',
                'borderWidth': 1,
                'data': seal_data},
                {
                'label': "SDF",
                'backgroundColor': 'rgba(87, 50, 200, 0.2)',
                'borderColor': 'rgba(87, 50, 200, 1)',
                'borderWidth': 1,
                'data': sdf_data},
                {
                'label': "FV",
                'backgroundColor': 'rgba(239, 62, 54, 0.2)',
                'borderColor': 'rgba(239, 62, 54, 1)',
                'borderWidth': 1,
                'data': fv_data}]
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
                # 'text': "Setting-wise treatment distribution",
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
                }}}}
            return JsonResponse({"locationChart":locationChart},status=200)
        return Response({"message":serializer.errors},status=400)


class PieChartVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        health_post_obj = Activity.objects.get(name = 'Health Post')
        school_seminar_obj = Activity.objects.get(name = 'School Seminar')
        community_outreach_obj = Activity.objects.get(name = 'Community Outreach')
        training_obj = Activity.objects.get(name = 'Training')
        data = []
        data_label=[]
        for activities_obj in Activity.objects.all():
            data_label.append(activities_obj.name)
            a=[]
            a.append(Visualization.objects.filter(exo=True,created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).count())
            a.append(Visualization.objects.filter(art=True,created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).count())
            a.append(Visualization.objects.filter(seal=True,created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).count())
            a.append(Visualization.objects.filter(sdf=True,created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).count())
            a.append(Visualization.objects.filter(fv=True,created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).count())
            data.append(sum(a))
        locationChart = {
        'data': {
        'labels': data_label,
        'datasets': [
        {
        'label': "Female",
        'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)','rgba(230, 232, 230, 0.5)'],
        'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)','rgba(230, 232, 230, 1)'],
        'borderWidth': 1,
        'data':data
        }]},
        'options': {
        'aspectRatio': 1.5,
        'title': {
        'display': 'true',
        # 'text': "Activity Distribution Chart",
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

class PieChartVisualizationFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            age_group = serializer.validated_data['age_group']
            location_list = serializer.validated_data['location']
            label_data = ['Health Post', 'School Seminar', 'Community Outreach', 'Training']

            health_post_obj = Activity.objects.get(name = 'Health Post')
            school_seminar_obj = Activity.objects.get(name = 'School Seminar')
            community_outreach_obj = Activity.objects.get(name = 'Community Outreach')
            training_obj = Activity.objects.get(name = 'Training')

            health_post_count=[]
            school_seminar_count=[]
            community_outreach_count=[]
            training_count=[]
            if not location_list:
                if(age_group=="alltreatment"):
                    data = []
                    data_label=[]
                    for activities_obj in Activity.objects.all():
                        data_label.append(activities_obj.name)
                        a=[]
                        a.append(Visualization.objects.filter(exo=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                        a.append(Visualization.objects.filter(art=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                        a.append(Visualization.objects.filter(seal=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                        a.append(Visualization.objects.filter(sdf=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                        a.append(Visualization.objects.filter(fv=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                        data.append(sum(a))
                    locationChart = {
                    'data': {
                    'labels': data_label,
                    'datasets': [
                    {
                    'label': "Female",
                    'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)','rgba(230, 232, 230, 0.5)'],
                    'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)','rgba(230, 232, 230, 1)'],
                    'borderWidth': 1,
                    'data':data
                    }]},
                    'options': {
                    'aspectRatio': 1.5,
                    'title': {
                    'display': 'true',
                    # 'text': "Activity Distribution Chart",
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

                if(age_group=='exo'):
                    health_post_count.append(Visualization.objects.filter(exo=True,activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).count())
                    school_seminar_count.append(Visualization.objects.filter(exo=True,activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).count())
                    community_outreach_count.append(Visualization.objects.filter(exo=True,activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).count())
                    training_count.append(Visualization.objects.filter(exo=True,activities_id=training_obj.id,created_at__range=[start_date,end_date]).count())
                if(age_group=='art'):
                    health_post_count.append(Visualization.objects.filter(art=True,activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).count())
                    school_seminar_count.append(Visualization.objects.filter(art=True,activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).count())
                    community_outreach_count.append(Visualization.objects.filter(art=True,activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).count())
                    training_count.append(Visualization.objects.filter(art=True,activities_id=training_obj.id,created_at__range=[start_date,end_date]).count())
                if(age_group=='seal'):
                    health_post_count.append(Visualization.objects.filter(seal=True,activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).count())
                    school_seminar_count.append(Visualization.objects.filter(seal=True,activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).count())
                    community_outreach_count.append(Visualization.objects.filter(seal=True,activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).count())
                    training_count.append(Visualization.objects.filter(seal=True,activities_id=training_obj.id,created_at__range=[start_date,end_date]).count())
                if(age_group=='sdf'):
                    health_post_count.append(Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).count())
                    school_seminar_count.append(Visualization.objects.filter(sdf=True,activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).count())
                    community_outreach_count.append(Visualization.objects.filter(sdf=True,activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).count())
                    training_count.append(Visualization.objects.filter(sdf=True,activities_id=training_obj.id,created_at__range=[start_date,end_date]).count())
                if(age_group=='fv'):
                    health_post_count.append(Visualization.objects.filter(fv=True,activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).count())
                    school_seminar_count.append(Visualization.objects.filter(fv=True,activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).count())
                    community_outreach_count.append(Visualization.objects.filter(fv=True,activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).count())
                    training_count.append(Visualization.objects.filter(fv=True,activities_id=training_obj.id,created_at__range=[start_date,end_date]).count())
            else:
                if(age_group=="alltreatment"):
                    data = []
                    data_label=[]
                    for activities_obj in Activity.objects.all():
                        data_label.append(activities_obj.name)
                        a=[]
                        for location in location_list:
                            a.append(Visualization.objects.filter(exo=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).count())
                            a.append(Visualization.objects.filter(art=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).count())
                            a.append(Visualization.objects.filter(seal=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).count())
                            a.append(Visualization.objects.filter(sdf=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).count())
                            a.append(Visualization.objects.filter(fv=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).count())
                        data.append(sum(a))

                    locationChart = {
                    'data': {
                    'labels': data_label,
                    'datasets': [
                    {
                    'label': "Female",
                    'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)','rgba(230, 232, 230, 0.5)'],
                    'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)','rgba(230, 232, 230, 1)'],
                    'borderWidth': 1,
                    'data':data
                    }]},
                    'options': {
                    'aspectRatio': 1.5,
                    'title': {
                    'display': 'true',
                    # 'text': "Activity Distribution Chart",
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
                for location in location_list:
                    if(age_group=="alltreatment"):
                        data = []
                        data_label=[]
                        for activities_obj in Activity.objects.all():
                            data_label.append(activities_obj.name)
                            a=[]
                            a.append(Visualization.objects.filter(exo=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                            a.append(Visualization.objects.filter(art=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                            a.append(Visualization.objects.filter(seal=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                            a.append(Visualization.objects.filter(sdf=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                            a.append(Visualization.objects.filter(fv=True,created_at__range=[start_date,end_date],activities_id=activities_obj.id).count())
                            data.append(sum(a))
                        locationChart = {
                        'data': {
                        'labels': data_label,
                        'datasets': [
                        {
                        'label': "Female",
                        'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)','rgba(230, 232, 230, 0.5)'],
                        'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)','rgba(230, 232, 230, 1)'],
                        'borderWidth': 1,
                        'data':data
                        }]},
                        'options': {
                        'aspectRatio': 1.5,
                        'title': {
                        'display': 'true',
                        # 'text': "Activity Distribution Chart",
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

                    if age_group=='exo':
                        health_post_count.append(Visualization.objects.filter(exo=True,activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        school_seminar_count.append(Visualization.objects.filter(exo=True,activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        community_outreach_count.append(Visualization.objects.filter(exo=True,activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        training_count.append(Visualization.objects.filter(exo=True,activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())

                    if age_group=='art':
                        health_post_count.append(Visualization.objects.filter(art=True,activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        school_seminar_count.append(Visualization.objects.filter(art=True,activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        community_outreach_count.append(Visualization.objects.filter(art=True,activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        training_count.append(Visualization.objects.filter(art=True,activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())

                    if age_group=='seal':
                        health_post_count.append(Visualization.objects.filter(seal=True,activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        school_seminar_count.append(Visualization.objects.filter(seal=True,activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        community_outreach_count.append(Visualization.objects.filter(seal=True,activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        training_count.append(Visualization.objects.filter(seal=True,activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())

                    if age_group=='sdf':
                        health_post_count.append(Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        school_seminar_count.append(Visualization.objects.filter(sdf=True,activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        community_outreach_count.append(Visualization.objects.filter(sdf=True,activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        training_count.append(Visualization.objects.filter(sdf=True,activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())

                    if age_group=='fv':
                        health_post_count.append(Visualization.objects.filter(fv=True,activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        school_seminar_count.append(Visualization.objects.filter(fv=True,activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        community_outreach_count.append(Visualization.objects.filter(fv=True,activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
                        training_count.append(Visualization.objects.filter(fv=True,activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).count())
            locationChart = {
            'data': {
            'labels': ['Community Outreach', 'Health Post', 'School Seminar','Training'],
            'datasets': [
            {
            'label': "Female",
            'backgroundColor': ['rgba(255, 206, 86, 0.5)', 'rgba(239, 62, 54, 0.5)', 'rgba(81, 264, 210, 0.5)', 'rgba(16, 152, 247, 0.5)'],
            'borderColor': ['rgba(255, 206, 86, 0.5)', 'rgba(239, 62, 54, 1)', 'rgba(81, 264, 210, 1)', 'rgba(16, 152, 247, 1)'],
            'borderWidth': 1,
            'data': [[sum(community_outreach_count)],[sum(health_post_count)], [sum(school_seminar_count)], [sum(training_count)]]
            }]},
            'options': {
            'aspectRatio': 1.5,
            'title': {
            'display': 'true',
            # 'text': "Activity Distribution Chart",
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
