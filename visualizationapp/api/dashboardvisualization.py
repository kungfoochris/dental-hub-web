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
from django.db.models import Sum
import logging
# Get an instance of a logger
from django.db.models import Count, Case, When, Value
logger = logging.getLogger(__name__)


np_date = NepaliDate()
# d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
# lessthan18 = d - datetime.timedelta(days=365*18)
# greaterthan60 = d - datetime.timedelta(days=365*60)



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
            kid_exo = Visualization.objects.filter(age__lt=12, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('exo'))['exo__sum']
            if kid_exo is None:
                kid_exo = 0
            kid_art = Visualization.objects.filter(age__lt=12, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('art'))['art__sum']
            if kid_art is None:
                kid_art = 0
            kid_seal = Visualization.objects.filter(age__lt=12, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('seal'))['seal__sum']
            if kid_seal is None:
                kid_seal = 0
            kid_sdf = Visualization.objects.filter(age__lt=12, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('sdf'))['sdf__sum']
            if kid_sdf is None:
                kid_sdf = 0
            kid_fv = Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()


            teen_exo = Visualization.objects.filter(age__range=(12,18), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('exo'))['exo__sum']
            if teen_exo is None:
                teen_exo = 0
            teen_art = Visualization.objects.filter(age__range=(12,18), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('art'))['art__sum']
            if teen_art is None:
                teen_art = 0
            teen_seal = Visualization.objects.filter(age__range=(12,18), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('seal'))['seal__sum']
            if teen_seal is None:
                teen_seal = 0
            teen_sdf = Visualization.objects.filter(age__range=(12,18), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('sdf'))['sdf__sum']
            if teen_sdf is None:
                teen_sdf = 0
            teen_fv = Visualization.objects.filter(fv=True,age__range=(12,18),created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_exo = Visualization.objects.filter(age__range=(19,60), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('exo'))['exo__sum']
            if adult_exo is None:
                adult_exo = 0
            adult_art = Visualization.objects.filter(age__range=(19,60), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('art'))['art__sum']
            if adult_art is None:
                adult_art = 0
            adult_seal = Visualization.objects.filter(age__range=(19,60), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('seal'))['seal__sum']
            if adult_seal is None:
                adult_seal = 0
            adult_sdf = Visualization.objects.filter(age__range=(19,60), created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('sdf'))['sdf__sum']
            if adult_sdf is None:
                adult_sdf = 0
            adult_fv = Visualization.objects.filter(fv=True,age__range=(19,60),created_at__range=[last_30_days_obj,today_date_obj]).count()


            old_adult_exo = Visualization.objects.filter(age__gt=60, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('exo'))['exo__sum']
            if old_adult_exo is None:
                old_adult_exo = 0
            old_adult_art = Visualization.objects.filter(age__gt=60, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('art'))['art__sum']
            if old_adult_art is None:
                old_adult_art = 0
            old_adult_seal = Visualization.objects.filter(age__gt=60, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('seal'))['seal__sum']
            if old_adult_seal is None:
                old_adult_seal = 0
            old_adult_sdf = Visualization.objects.filter(age__gt=60, created_at__range=[last_30_days_obj, today_date_obj]).aggregate(Sum('sdf'))['sdf__sum']
            if old_adult_sdf is None:
                old_adult_sdf = 0
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
                if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    health_post_exo.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    health_post_exo.append(0)

                if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    health_post_art.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    health_post_art.append(0)

                if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    health_post_seal.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    health_post_seal.append(0)

                if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    health_post_sdf.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    health_post_sdf.append(0)

                health_post_fv.append(Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date]).count())


                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    seminar_exo.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    seminar_exo.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    seminar_art.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    seminar_art.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    seminar_seal.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    seminar_seal.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    seminar_sdf.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    seminar_sdf.append(0)
                seminar_fv.append(Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).count())

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    outreach_exo.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    outreach_exo.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    outreach_art.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    outreach_art.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    outreach_seal.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    outreach_seal.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    outreach_sdf.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    outreach_sdf.append(0)
                outreach_fv.append(Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date]).count())


                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    training_exo.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    training_exo.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    training_art.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    training_art.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    training_seal.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    training_seal.append(0)

                if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    training_sdf.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    training_sdf.append(0)
                training_fv.append(Visualization.objects.filter(fv=True,activities_id=training.id).filter(created_at__range=[start_date,end_date]).count())

                district1=['Kids','Teen','Adult', 'Old Adult']
                if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    kid_exo.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    kid_exo.append(0)

                if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    kid_art.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    kid_art.append(0)

                if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    kid_seal.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    kid_seal.append(0)

                if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    kid_sdf.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    kid_sdf.append(0)
                kid_fv.append(Visualization.objects.filter(fv=True,age__lt=12).filter(created_at__range=[start_date,end_date]).count())

                if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    teen_exo.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    teen_exo.append(0)

                if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    teen_art.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    teen_art.append(0)

                if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    teen_seal.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    teen_seal.append(0)

                if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    teen_sdf.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    teen_sdf.append(0)
                teen_fv.append(Visualization.objects.filter(fv=True,age__range=(12,18)).filter(created_at__range=[start_date,end_date]).count())


                if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    adult_exo.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    adult_exo.append(0)

                if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    adult_art.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    adult_art.append(0)

                if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    adult_seal.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    adult_seal.append(0)

                if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    adult_sdf.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    adult_sdf.append(0)
                adult_fv.append(Visualization.objects.filter(fv=True,age__range=(19,60)).filter(created_at__range=[start_date,end_date]).count())

                if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                    old_adult_exo.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                else:
                    old_adult_exo.append(0)

                if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                    old_adult_art.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                else:
                    old_adult_art.append(0)

                if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                    old_adult_seal.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                else:
                    old_adult_seal.append(0)

                if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                    old_adult_sdf.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                else:
                    old_adult_sdf.append(0)
                old_adult_fv.append(Visualization.objects.filter(fv=True,age__gt=60).filter(created_at__range=[start_date,end_date]).count())

            else:
                for location in location_list:
                    if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        health_post_exo.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        health_post_exo.append(0)

                    if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        health_post_art.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        health_post_art.append(0)

                    if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        health_post_seal.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        health_post_seal.append(0)

                    if Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        health_post_sdf.append(Visualization.objects.filter(activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        health_post_sdf.append(0)
                    health_post_fv.append(Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        seminar_exo.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        seminar_exo.append(0)

                    if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        seminar_art.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        seminar_art.append(0)

                    if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        seminar_seal.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        seminar_seal.append(0)

                    if Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        seminar_sdf.append(Visualization.objects.filter(activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        seminar_sdf.append(0)
                    seminar_fv.append(Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    if Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        outreach_exo.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        outreach_exo.append(0)

                    if Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        outreach_art.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        outreach_art.append(0)

                    if Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        outreach_seal.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        outreach_seal.append(0)

                    if Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        outreach_sdf.append(Visualization.objects.filter(activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        outreach_sdf.append(0)
                    outreach_fv.append(Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    if Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        training_exo.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        training_exo.append(0)

                    if Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        training_art.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        training_art.append(0)

                    if Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        training_seal.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        training_seal.append(0)

                    if Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        training_sdf.append(Visualization.objects.filter(activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        training_sdf.append(0)
                    training_fv.append(Visualization.objects.filter(fv=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    district1=['Kids','Teen','Adult', 'Old Adult']
                    
                    if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        kid_exo.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        kid_exo.append(0)

                    if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        kid_art.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        kid_art.append(0)

                    if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        kid_seal.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        kid_seal.append(0)

                    if Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        kid_sdf.append(Visualization.objects.filter(age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        kid_sdf.append(0)
                    kid_fv.append(Visualization.objects.filter(fv=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        teen_exo.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        teen_exo.append(0)

                    if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        teen_art.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        teen_art.append(0)

                    if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        teen_seal.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        teen_seal.append(0)

                    if Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        teen_sdf.append(Visualization.objects.filter(age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        teen_sdf.append(0)
                    teen_fv.append(Visualization.objects.filter(fv=True,age__range=(12,18)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        adult_exo.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        adult_exo.append(0)

                    if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        adult_art.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        adult_art.append(0)

                    if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        adult_seal.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        adult_seal.append(0)

                    if Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        adult_sdf.append(Visualization.objects.filter(age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        adult_sdf.append(0)
                    adult_fv.append(Visualization.objects.filter(fv=True,age__range=(19,60)).filter(created_at__range=[start_date,end_date],geography_id=location.id).count())

                    if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                        old_adult_exo.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        old_adult_exo.append(0)

                    if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                        old_adult_art.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                    else:
                        old_adult_art.append(0)

                    if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                        old_adult_seal.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        old_adult_seal.append(0)

                    if Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        old_adult_sdf.append(Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        old_adult_sdf.append(0)
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
            if Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                a.append(Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('exo'))['exo__sum'])
            else:
                a.append(0)

            if Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('art'))['art__sum'] is not None:
                a.append(Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('art'))['art__sum'])
            else:
                a.append(0)

            if Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                a.append(Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('seal'))['seal__sum'])
            else:
                a.append(0)

            if Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                a.append(Visualization.objects.filter(created_at__range=[last_30_days_obj,today_date_obj],activities_id=activities_obj.id).aggregate(Sum('sdf'))['sdf__sum'])
            else:
                a.append(0)
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
                        if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                            a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('exo'))['exo__sum'])
                        else:
                            a.append(0)

                        if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('art'))['art__sum'] is not None:
                            a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('art'))['art__sum'])
                        else:
                            a.append(0)
                        
                        if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                            a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('seal'))['seal__sum'])
                        else:
                            a.append(0)

                        if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                            a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('sdf'))['sdf__sum'])
                        else:
                            a.append(0)
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
                    if Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                        health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        health_post_count.append(0)

                    if Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                        school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        school_seminar_count.append(0)

                    if Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                        community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        community_outreach_count.append(0)

                    if Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                        training_count.append(Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                    else:
                        training_count.append(0)
                        
                if(age_group=='art'):
                    if Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                        health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                    else:
                        health_post_count.append(0)

                    if Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                        school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                    else:
                        school_seminar_count.append(0)

                    if Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                        community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                    else:
                        community_outreach_count.append(0)

                    if Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                        training_count.append(Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                    else:
                        training_count.append(0)
                if(age_group=='seal'):
                    if Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                        health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        health_post_count.append(0)

                    if Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                        school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        school_seminar_count.append(0)

                    if Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                        community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        community_outreach_count.append(0)

                    if Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                        training_count.append(Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                    else:
                        training_count.append(0)
                if(age_group=='sdf'):
                    if Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        health_post_count.append(0)

                    if Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        school_seminar_count.append(0)

                    if Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        community_outreach_count.append(0)

                    if Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                        training_count.append(Visualization.objects.filter(activities_id=training_obj.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                    else:
                        training_count.append(0)
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
                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('exo'))['exo__sum'])
                            else:
                                a.append(0)

                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                            else:
                                a.append(0)

                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                            else:
                                a.append(0)

                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                            else:
                                a.append(0)
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
                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id).aggregate(Sum('exo'))['exo__sum'])
                            else:
                                a.append(0)
                            
                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('art'))['art__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('art'))['art__sum'])
                            else:
                                a.append(0)

                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('seal'))['seal__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('seal'))['seal__sum'])
                            else:
                                a.append(0)

                            if Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                                a.append(Visualization.objects.filter(created_at__range=[start_date,end_date],activities_id=activities_obj.id,geography_id=location.id).aggregate(Sum('sdf'))['sdf__sum'])
                            else:
                                a.append(0)

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
                        if Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                            health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                        else:
                            health_post_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                            school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                        else:
                            school_seminar_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                            community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                        else:
                            community_outreach_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'] is not None:
                            training_count.append(Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('exo'))['exo__sum'])
                        else:
                            training_count.append(0)

                    if(age_group=='art'):
                        if Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                            health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                        else:
                            health_post_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                            school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                        else:
                            school_seminar_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                            community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                        else:
                            community_outreach_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'] is not None:
                            training_count.append(Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('art'))['art__sum'])
                        else:
                            training_count.append(0)

                    if(age_group=='seal'):
                        if Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                            health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                        else:
                            health_post_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                            school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                        else:
                            school_seminar_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                            community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                        else:
                            community_outreach_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'] is not None:
                            training_count.append(Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('seal'))['seal__sum'])
                        else:
                            training_count.append(0)

                    if(age_group=='sdf'):
                        if Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                            health_post_count.append(Visualization.objects.filter(activities_id=health_post_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                        else:
                            health_post_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                            school_seminar_count.append(Visualization.objects.filter(activities_id=school_seminar_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                        else:
                            school_seminar_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                            community_outreach_count.append(Visualization.objects.filter(activities_id=community_outreach_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                        else:
                            community_outreach_count.append(0)
                            
                        if Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                            training_count.append(Visualization.objects.filter(activities_id=training_obj.id,geography_id=location.id,created_at__range=[start_date,end_date]).aggregate(Sum('sdf'))['sdf__sum'])
                        else:
                            training_count.append(0)
                        
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
