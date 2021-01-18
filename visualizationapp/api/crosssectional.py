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
import statistics

from visualizationapp.serializers.visualization import SectionalVisualizationSerializer,\
OverViewVisualization


# from datetime import datetime
# from datetime import timedelta
import logging
# Get an instance of a logger
from django.db.models import Count

logger = logging.getLogger(__name__)


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class SectionalVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = SectionalVisualizationSerializer

    def get(self, request,format=None):
        if User.objects.filter(id=request.user.id).exists():
            carries_risk=["Carries Risk"]
            carries_risk_low=['<span class="ml-4">Low</span>']
            carries_risk_medium=['<span class="ml-4">Medium</span>']
            carries_risk_high=['<span class="ml-4">High</span>']
            decayed_permanent_teeth = ["Number of decayed permanent teeth"]
            decayed_primary_teeth = ["Number of decayed primary teeth"]
            cavity_permanent_molar= ["Cavity permanent molar or premolar"]
            cavity_permanent_anterior = ["Cavity permanent anterior"]

            total_active_infection=Visualization.objects.filter(active_infection=True).count()
            total_active_infection_6=Visualization.objects.filter(age=6,active_infection=True).count()
            total_active_infection_12=Visualization.objects.filter(age=12,active_infection=True).count()
            total_active_infection_15=Visualization.objects.filter(age=15,active_infection=True).count()
            total_active_infection_child=Visualization.objects.filter(age__lt=18,active_infection=True).count()
            total_active_infection_adult=Visualization.objects.filter(age__range=(18,60),active_infection=True).count()
            total_active_infection_old=Visualization.objects.filter(age__gt=60,active_infection=True).count()

            carries_risk_low.append(Visualization.objects.filter(age=6,carries_risk="Low").count())
            carries_risk_low.append(Visualization.objects.filter(age=12,carries_risk="Low").count())
            carries_risk_low.append(Visualization.objects.filter(age=15,carries_risk="Low").count())
            carries_risk_low.append(Visualization.objects.filter(age__lt=18,carries_risk="Low").count())
            carries_risk_low.append(Visualization.objects.filter(age__range=(18,60),carries_risk="Low").count())
            carries_risk_low.append(Visualization.objects.filter(age__gt=60,carries_risk="Low").count())
            carries_risk_low.append('secondary')

            carries_risk_medium.append(Visualization.objects.filter(age=6,carries_risk="Medium").count())
            carries_risk_medium.append(Visualization.objects.filter(age=12,carries_risk="Medium").count())
            carries_risk_medium.append(Visualization.objects.filter(age=15,carries_risk="Medium").count())
            carries_risk_medium.append(Visualization.objects.filter(age__lt=18,carries_risk="Medium").count())
            carries_risk_medium.append(Visualization.objects.filter(age__range=(18,60),carries_risk="Medium").count())
            carries_risk_medium.append(Visualization.objects.filter(age__gt=60,carries_risk="Medium").count())
            carries_risk_medium.append('secondary')

            carries_risk_high.append(Visualization.objects.filter(age=6,carries_risk="High").count())
            carries_risk_high.append(Visualization.objects.filter(age=12,carries_risk="High").count())
            carries_risk_high.append(Visualization.objects.filter(age=15,carries_risk="High").count())
            carries_risk_high.append(Visualization.objects.filter(age__lt=18,carries_risk="High").count())
            carries_risk_high.append(Visualization.objects.filter(age__range=(18,60),carries_risk="High").count())
            carries_risk_high.append(Visualization.objects.filter(age__gt=60,carries_risk="High").count())
            carries_risk_high.append('secondary')

            decayed_primary_teeth_6=[]
            permanent_molar_teeth_6=[]
            for i in Visualization.objects.filter(age=6):
                decayed_primary_teeth_6.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth_6.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_6),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_6),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            decayed_primary_teeth_12=[]
            permanent_molar_teeth_12=[]
            for i in Visualization.objects.filter(age=12):
                decayed_primary_teeth_12.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth_12.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_12),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_12),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            decayed_primary_teeth_15=[]
            permanent_molar_teeth_15=[]
            for i in Visualization.objects.filter(age=15):
                decayed_primary_teeth_15.append(i.decayed_primary_teeth_number)
                decayed_primary_teeth_15.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_15),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_15),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            decayed_primary_teeth_child=[]
            permanent_molar_teeth_child=[]
            for i in Visualization.objects.filter(age__lt=18):
                decayed_primary_teeth_child.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth_child.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_child),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_child),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            decayed_primary_teeth_adult=[]
            permanent_molar_teeth_adult=[]
            for i in Visualization.objects.filter(age__range=(18,60)):
                decayed_primary_teeth_adult.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth_adult.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_adult),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_adult),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            decayed_primary_teeth_old=[]
            permanent_molar_teeth_old=[]
            for i in Visualization.objects.filter(age__gt=60):
                decayed_primary_teeth_old.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth_old.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_old),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_old),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)

            total_cavity_permanent_posterior=Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
            total_cavity_permanent_posterior_teeth_6=Visualization.objects.filter(age=6,cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_6/total_cavity_permanent_posterior)*100,2))
            except:
                cavity_permanent_molar.append(0)

            total_cavity_permanent_posterior_teeth_12=Visualization.objects.filter(age=12,cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_12/total_cavity_permanent_posterior)*100,2))
            except:
                cavity_permanent_molar.append(0)

            total_cavity_permanent_posterior_teeth_15=Visualization.objects.filter(age=15,cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_15/total_cavity_permanent_posterior)*100,2))
            except:
                cavity_permanent_molar.append(0)


            total_cavity_permanent_posterior_teeth_child=Visualization.objects.filter(age__lt=18,cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_child/total_cavity_permanent_posterior)*100,2))
            except:
                cavity_permanent_molar.append(0)


            total_cavity_permanent_posterior_teeth_adult=Visualization.objects.filter(age__range=(18,60),cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_adult/total_cavity_permanent_posterior)*100,2))
            except:
                cavity_permanent_molar.append(0)


            total_cavity_permanent_posterior_teeth_old=Visualization.objects.filter(age__gt=60,cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_old/total_cavity_permanent_posterior)*100,2))
            except:
                cavity_permanent_molar.append(0)

            total_cavity_permanent_anterior=Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
            total_cavity_permanent_anterior_teeth_6=Visualization.objects.filter(age=6,cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_6/total_cavity_permanent_anterior)*100,2))
            except:
                cavity_permanent_anterior.append(0)


            total_cavity_permanent_anterior_teeth_12=Visualization.objects.filter(age=12,cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_12/total_cavity_permanent_anterior)*100,2))
            except:
                cavity_permanent_anterior.append(0)


            total_cavity_permanent_anterior_teeth_15=Visualization.objects.filter(age=15,cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_15/total_cavity_permanent_anterior)*100,2))
            except:
                cavity_permanent_anterior.append(0)


            total_cavity_permanent_anterior_teeth_child=Visualization.objects.filter(age__lt=18,cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_child/total_cavity_permanent_anterior)*100,2))
            except:
                cavity_permanent_anterior.append(0)


            total_cavity_permanent_anterior_teeth_adult=Visualization.objects.filter(age__range=(18,60),cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_adult/total_cavity_permanent_anterior)*100,2))
            except:
                cavity_permanent_anterior.append(0)


            total_cavity_permanent_anterior_teeth_old=Visualization.objects.filter(age__gt=60,cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_old/total_cavity_permanent_anterior)*100,2))
            except:
                cavity_permanent_anterior.append(0)



            total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True).count()
            total_reversible_pulpitis_6=Visualization.objects.filter(age=6,reversible_pulpitis=True).count()
            total_reversible_pulpitis_12=Visualization.objects.filter(age=12,reversible_pulpitis=True).count()
            total_reversible_pulpitis_15=Visualization.objects.filter(age=15,reversible_pulpitis=True).count()
            total_reversible_pulpitis_child=Visualization.objects.filter(age__lt=18,reversible_pulpitis=True).count()
            total_reversible_pulpitis_adult=Visualization.objects.filter(age__range=(18,60),reversible_pulpitis=True).count()
            total_reversible_pulpitis_old=Visualization.objects.filter(age__gt=60,reversible_pulpitis=True).count()


            total_need_art_filling_6=Visualization.objects.filter(age=6,need_art_filling=True).count()
            total_need_art_filling_12=Visualization.objects.filter(age=12,need_art_filling=True).count()
            total_need_art_filling_15=Visualization.objects.filter(age=15,need_art_filling=True).count()
            total_need_art_filling_child=Visualization.objects.filter(age__lt=18,need_art_filling=True).count()
            total_need_art_filling_adult=Visualization.objects.filter(age__range=(18,60),need_art_filling=True).count()
            total_need_art_filling_old=Visualization.objects.filter(age__gt=60,need_art_filling=True).count()

            total_need_sdf=Visualization.objects.filter(need_sdf=True).count()
            total_need_sdf_6=Visualization.objects.filter(age=6,need_sdf=True).count()
            total_need_sdf_12=Visualization.objects.filter(age=12,need_sdf=True).count()
            total_need_sdf_15=Visualization.objects.filter(age=15,need_sdf=True).count()
            total_need_sdf_child=Visualization.objects.filter(age__lt=18,need_sdf=True).count()
            total_need_sdf_adult=Visualization.objects.filter(age__range=(18,60),need_sdf=True).count()
            total_need_sdf_old=Visualization.objects.filter(age__gt=60,need_sdf=True).count()

            total_need_extraction=Visualization.objects.filter(need_extraction=True).count()
            total_need_extraction_6=Visualization.objects.filter(age=6,need_extraction=True).count()
            total_need_extraction_12=Visualization.objects.filter(age=12,need_extraction=True).count()
            total_need_extraction_15=Visualization.objects.filter(age=15,need_extraction=True).count()
            total_need_extraction_child=Visualization.objects.filter(age__lt=18,need_extraction=True).count()
            total_need_extraction_adult=Visualization.objects.filter(age__range=(18,60),need_extraction=True).count()
            total_need_extraction_old=Visualization.objects.filter(age__gt=60,need_extraction=True).count()


            return Response([carries_risk,carries_risk_low,carries_risk_medium,carries_risk_high,decayed_primary_teeth,decayed_permanent_teeth,\
            cavity_permanent_molar,cavity_permanent_anterior,\
            ["Active Infection",total_active_infection_6,total_active_infection_12, total_active_infection_15,total_active_infection_child,total_active_infection_adult,total_active_infection_old],\
            ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis_6,total_reversible_pulpitis_12,total_reversible_pulpitis_15,total_reversible_pulpitis_child,total_reversible_pulpitis_adult,total_reversible_pulpitis_old],\
            ["Need ART filling",total_need_art_filling_6,total_need_art_filling_12,total_need_art_filling_15,total_need_art_filling_child,total_need_art_filling_adult,total_need_art_filling_old],\
            ["Need SDF",total_need_sdf_6,total_need_sdf_12,total_need_sdf_15,total_need_sdf_child,total_need_sdf_adult,total_need_sdf_old],\
            ["Need Extraction",total_need_extraction_6,total_need_extraction_12,total_need_extraction_15,total_need_extraction_child,total_need_extraction_adult,total_need_extraction_old]])

    def post(self, request, format=None):
        serializer = SectionalVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            reason_for_visit  = serializer.validated_data['reason_for_visit']
            referral_type  = serializer.validated_data['referral_type']
            health_post = serializer.validated_data['health_post']
            seminar = serializer.validated_data['seminar']
            outreach = serializer.validated_data['outreach']
            training = serializer.validated_data['training']

            carries_risk=["Carries Risk"]
            carries_risk_low=['<span class="ml-4">Low</span>']
            carries_risk_medium=['<span class="ml-4">Medium</span>']
            carries_risk_high=['<span class="ml-4">High</span>']
            decayed_permanent_teeth = ["Number of decayed permanent teeth"]
            decayed_primary_teeth = ["Number of decayed primary teeth"]
            cavity_permanent_molar= ["Cavity permanent molar or premolar"]
            cavity_permanent_anterior = ["Cavity permanent anterior"]

            if(end_date > start_date):
                total_active_infection_6=Visualization.objects.filter(age=6,active_infection=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_active_infection_12=Visualization.objects.filter(age=12,active_infection=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_active_infection_15=Visualization.objects.filter(age=15,active_infection=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_active_infection_child=Visualization.objects.filter(age__lt=18,active_infection=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_active_infection_adult=Visualization.objects.filter(age__range=(18,60),active_infection=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_active_infection_old=Visualization.objects.filter(age__gt=60,active_infection=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()

                carries_risk_low.append(Visualization.objects.filter(age=6,carries_risk="Low",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_low.append(Visualization.objects.filter(age=12,carries_risk="Low",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_low.append(Visualization.objects.filter(age=15,carries_risk="Low",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_low.append(Visualization.objects.filter(age__lt=18,carries_risk="Low",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_low.append(Visualization.objects.filter(age__range=(18,60),carries_risk="Low",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_low.append(Visualization.objects.filter(age__gt=60,carries_risk="Low",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_low.append('secondary')

                carries_risk_medium.append(Visualization.objects.filter(age=6,carries_risk="Medium",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_medium.append(Visualization.objects.filter(age=12,carries_risk="Medium",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_medium.append(Visualization.objects.filter(age=15,carries_risk="Medium",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_medium.append(Visualization.objects.filter(age__lt=18,carries_risk="Medium",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_medium.append(Visualization.objects.filter(age__range=(18,60),carries_risk="Medium",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_medium.append(Visualization.objects.filter(age__gt=60,carries_risk="Medium",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_medium.append('secondary')

                carries_risk_high.append(Visualization.objects.filter(age=6,carries_risk="High",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_high.append(Visualization.objects.filter(age=12,carries_risk="High",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_high.append(Visualization.objects.filter(age=15,carries_risk="High",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_high.append(Visualization.objects.filter(age__lt=18,carries_risk="High",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_high.append(Visualization.objects.filter(age__range=(18,60),carries_risk="High",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_high.append(Visualization.objects.filter(age__gt=60,carries_risk="High",created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                carries_risk_high.append('secondary')

                decayed_primary_teeth_6=[]
                permanent_molar_teeth_6=[]
                for i in Visualization.objects.filter(age=6,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type):
                    decayed_primary_teeth_6.append(i.decayed_primary_teeth_number)
                    permanent_molar_teeth_6.append(i.decayed_permanent_teeth_number)

                try:
                    decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_6),2))
                    decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_6),2))
                except:
                    decayed_primary_teeth.append(0)
                    decayed_permanent_teeth.append(0)


                decayed_primary_teeth_12=[]
                permanent_molar_teeth_12=[]
                for i in Visualization.objects.filter(age=12,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type):
                    decayed_primary_teeth_12.append(i.decayed_primary_teeth_number)
                    permanent_molar_teeth_12.append(i.decayed_permanent_teeth_number)

                try:
                    decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_12),2))
                    decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_12),2))
                except:
                    decayed_primary_teeth.append(0)
                    decayed_permanent_teeth.append(0)


                decayed_primary_teeth_15=[]
                permanent_molar_teeth_15=[]
                for i in Visualization.objects.filter(age=15,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type):
                    decayed_primary_teeth_15.append(i.decayed_primary_teeth_number)
                    decayed_primary_teeth_15.append(i.decayed_permanent_teeth_number)

                try:
                    decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_15),2))
                    decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_15),2))
                except:
                    decayed_primary_teeth.append(0)
                    decayed_permanent_teeth.append(0)


                decayed_primary_teeth_child=[]
                permanent_molar_teeth_child=[]
                for i in Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type):
                    decayed_primary_teeth_child.append(i.decayed_primary_teeth_number)
                    permanent_molar_teeth_child.append(i.decayed_permanent_teeth_number)

                try:
                    decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_child),2))
                    decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_child),2))
                except:
                    decayed_primary_teeth.append(0)
                    decayed_permanent_teeth.append(0)


                decayed_primary_teeth_adult=[]
                permanent_molar_teeth_adult=[]
                for i in Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type):
                    decayed_primary_teeth_adult.append(i.decayed_primary_teeth_number)
                    permanent_molar_teeth_adult.append(i.decayed_permanent_teeth_number)

                try:
                    decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_adult),2))
                    decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_adult),2))
                except:
                    decayed_primary_teeth.append(0)
                    decayed_permanent_teeth.append(0)


                decayed_primary_teeth_old=[]
                permanent_molar_teeth_old=[]
                for i in Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type):
                    decayed_primary_teeth_old.append(i.decayed_primary_teeth_number)
                    permanent_molar_teeth_old.append(i.decayed_permanent_teeth_number)

                try:
                    decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth_old),2))
                    decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth_old),2))
                except:
                    decayed_primary_teeth.append(0)
                    decayed_permanent_teeth.append(0)

                total_cavity_permanent_posterior=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_cavity_permanent_posterior_teeth_6=Visualization.objects.filter(age=6,cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_6/total_cavity_permanent_posterior)*100,2))
                except:
                    cavity_permanent_molar.append(0)

                total_cavity_permanent_posterior_teeth_12=Visualization.objects.filter(age=12,cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_12/total_cavity_permanent_posterior)*100,2))
                except:
                    cavity_permanent_molar.append(0)

                total_cavity_permanent_posterior_teeth_15=Visualization.objects.filter(age=15,cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_15/total_cavity_permanent_posterior)*100,2))
                except:
                    cavity_permanent_molar.append(0)


                total_cavity_permanent_posterior_teeth_child=Visualization.objects.filter(age__lt=18,cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_child/total_cavity_permanent_posterior)*100,2))
                except:
                    cavity_permanent_molar.append(0)


                total_cavity_permanent_posterior_teeth_adult=Visualization.objects.filter(age__range=(18,60),cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_adult/total_cavity_permanent_posterior)*100,2))
                except:
                    cavity_permanent_molar.append(0)


                total_cavity_permanent_posterior_teeth_old=Visualization.objects.filter(age__gt=60,cavity_permanent_posterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth_old/total_cavity_permanent_posterior)*100,2))
                except:
                    cavity_permanent_molar.append(0)



                total_cavity_permanent_anterior=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_cavity_permanent_anterior_teeth_6=Visualization.objects.filter(age=6,cavity_permanent_anterior_teeth=True,reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_6/total_cavity_permanent_anterior)*100,2))
                except:
                    cavity_permanent_anterior.append(0)


                total_cavity_permanent_anterior_teeth_12=Visualization.objects.filter(age=12,cavity_permanent_anterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_12/total_cavity_permanent_anterior)*100,2))
                except:
                    cavity_permanent_anterior.append(0)


                total_cavity_permanent_anterior_teeth_15=Visualization.objects.filter(age=15,cavity_permanent_anterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_15/total_cavity_permanent_anterior)*100,2))
                except:
                    cavity_permanent_anterior.append(0)


                total_cavity_permanent_anterior_teeth_child=Visualization.objects.filter(age__lt=18,cavity_permanent_anterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_child/total_cavity_permanent_anterior)*100,2))
                except:
                    cavity_permanent_anterior.append(0)


                total_cavity_permanent_anterior_teeth_adult=Visualization.objects.filter(age__range=(18,60),cavity_permanent_anterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_adult/total_cavity_permanent_anterior)*100,2))
                except:
                    cavity_permanent_anterior.append(0)


                total_cavity_permanent_anterior_teeth_old=Visualization.objects.filter(age__gt=60,cavity_permanent_anterior_teeth=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                try:
                    cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth_old/total_cavity_permanent_anterior)*100,2))
                except:
                    cavity_permanent_anterior.append(0)



                total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_reversible_pulpitis_6=Visualization.objects.filter(age=6,reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_reversible_pulpitis_12=Visualization.objects.filter(age=12,reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_reversible_pulpitis_15=Visualization.objects.filter(age=15,reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_reversible_pulpitis_child=Visualization.objects.filter(age__lt=18,reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_reversible_pulpitis_adult=Visualization.objects.filter(age__range=(18,60),reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_reversible_pulpitis_old=Visualization.objects.filter(age__gt=60,reversible_pulpitis=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()


                total_need_art_filling_6=Visualization.objects.filter(age=6,need_art_filling=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_art_filling_12=Visualization.objects.filter(age=12,need_art_filling=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_art_filling_15=Visualization.objects.filter(age=15,need_art_filling=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_art_filling_child=Visualization.objects.filter(age__lt=18,need_art_filling=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_art_filling_adult=Visualization.objects.filter(age__range=(18,60),need_art_filling=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_art_filling_old=Visualization.objects.filter(age__gt=60,need_art_filling=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()

                total_need_sdf=Visualization.objects.filter(need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_sdf_6=Visualization.objects.filter(age=6,need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_sdf_12=Visualization.objects.filter(age=12,need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_sdf_15=Visualization.objects.filter(age=15,need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_sdf_child=Visualization.objects.filter(age__lt=18,need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_sdf_adult=Visualization.objects.filter(age__range=(18,60),need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_sdf_old=Visualization.objects.filter(age__gt=60,need_sdf=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()

                total_need_extraction=Visualization.objects.filter(need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_extraction_6=Visualization.objects.filter(age=6,need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_extraction_12=Visualization.objects.filter(age=12,need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_extraction_15=Visualization.objects.filter(age=15,need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_extraction_child=Visualization.objects.filter(age__lt=18,need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_extraction_adult=Visualization.objects.filter(age__range=(18,60),need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()
                total_need_extraction_old=Visualization.objects.filter(age__gt=60,need_extraction=True,created_at__range=[start_date,end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).count()


                return Response([carries_risk,carries_risk_low,carries_risk_medium,carries_risk_high,decayed_primary_teeth,decayed_permanent_teeth,\
                cavity_permanent_molar,cavity_permanent_anterior,\
                ["Active Infection",total_active_infection_6,total_active_infection_12, total_active_infection_15,total_active_infection_child,total_active_infection_adult,total_active_infection_old],\
                ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis_6,total_reversible_pulpitis_12,total_reversible_pulpitis_15,total_reversible_pulpitis_child,total_reversible_pulpitis_adult,total_reversible_pulpitis_old],\
                ["Need ART filling",total_need_art_filling_6,total_need_art_filling_12,total_need_art_filling_15,total_need_art_filling_child,total_need_art_filling_adult,total_need_art_filling_old],\
                ["Need SDF",total_need_sdf_6,total_need_sdf_12,total_need_sdf_15,total_need_sdf_child,total_need_sdf_adult,total_need_sdf_old],\
                ["Need Extraction",total_need_extraction_6,total_need_extraction_12,total_need_extraction_15,total_need_extraction_child,total_need_extraction_adult,total_need_extraction_old]])
            return Response({"message":"End date must be greated then Start Date"},status=400)
        return Response({"message":serializer.errors},status=400)
