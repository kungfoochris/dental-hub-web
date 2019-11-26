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


class LongitudinalVisualization(APIView):
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
            carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
            carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
            carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
            decayed_primary_teeth1=[]
            permanent_molar_teeth=[]
            for i in Visualization.objects.all():
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            total_patients = Visualization.objects.all().count()

            total_cavity_permanent_posterior_teeth=Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth/total_patients)*100,2))
            except:
                cavity_permanent_molar.append(0)


            total_cavity_permanent_anterior_teeth=Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth/total_patients)*100,2))
            except:
                cavity_permanent_anterior.append(0)

            total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True).count()


            total_need_art_filling=Visualization.objects.filter(need_art_filling=True).count()
            total_need_sdf=Visualization.objects.filter(need_sdf=True).count()
            total_need_extraction=Visualization.objects.filter(need_extraction=True).count()


            #second
            total_active_infection1=Visualization.objects.filter(active_infection=True).count()
            carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
            carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
            carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
            decayed_primary_teeth1=[]
            permanent_molar_teeth=[]
            for i in Visualization.objects.all():
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

            try:
                decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
            except:
                decayed_primary_teeth.append(0)
                decayed_permanent_teeth.append(0)


            total_patients1 = Visualization.objects.all().count()

            total_cavity_permanent_posterior_teeth1=Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
            try:
                cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth1/total_patients1)*100,2))
            except:
                cavity_permanent_molar.append(0)


            total_cavity_permanent_anterior_teeth1=Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
            try:
                cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth1/total_patients1)*100,2))
            except:
                cavity_permanent_anterior.append(0)

            total_reversible_pulpitis1=Visualization.objects.filter(reversible_pulpitis=True).count()


            total_need_art_filling1=Visualization.objects.filter(need_art_filling=True).count()
            total_need_sdf1=Visualization.objects.filter(need_sdf=True).count()
            total_need_extraction1=Visualization.objects.filter(need_extraction=True).count()
            try:
                carries_risk_low.append(round(carries_risk_low[1]/carries_risk_low[2],2))
            except:
                carries_risk_low.append(0)
            try:
                carries_risk_medium.append(round(carries_risk_medium[1]/carries_risk_medium[2],2))
            except:
                carries_risk_medium.append(0)

            try:
                carries_risk_high.append(round(carries_risk_high[1]/carries_risk_high[2],2))
            except:
                carries_risk_high.append(0)

            try:
                decayed_permanent_teeth.append(round(decayed_permanent_teeth[1]/decayed_permanent_teeth[2],2))
            except:
                decayed_permanent_teeth.append(0)

            try:
                decayed_primary_teeth.append(round(decayed_primary_teeth[1]/decayed_primary_teeth[2],2))
            except:
                decayed_primary_teeth.append(0)

            try:
                cavity_permanent_molar.append(round(cavity_permanent_molar[1]/cavity_permanent_molar[2],2))
            except:
                cavity_permanent_molar.append(0)

            try:
                cavity_permanent_anterior.append(round(cavity_permanent_anterior[1]/cavity_permanent_anterior[2],2))
            except:
                cavity_permanent_anterior.append(0)

            try:
                active_real_difference = round(total_active_infection/total_active_infection1,2)
            except:
                active_real_difference = 0

            try:
                reversible_pulpitis_real_difference = round(total_reversible_pulpitis/total_reversible_pulpitis1,2)
            except:
                reversible_pulpitis_real_difference = 0

            try:
                art_real_difference = round(total_need_art_filling/total_need_art_filling1,2)
            except:
                art_real_difference = 0

            try:
                sdf_real_difference = round(total_need_sdf/total_need_sdf1,2)
            except:
                sdf_real_difference = 0

            try:
                extraction_real_difference = round(total_need_extraction/total_need_extraction1,2)
            except:
                extraction_real_difference = 0


            #third
            try:
                carries_risk_low.append(round(carries_risk_low[3]/carries_risk_low[1],2))
            except:
                carries_risk_low.append(0)
            try:
                carries_risk_medium.append(round(carries_risk_medium[3]/carries_risk_medium[1],2))
            except:
                carries_risk_medium.append(0)

            try:
                carries_risk_high.append(round(carries_risk_high[3]/carries_risk_high[1],2))
            except:
                carries_risk_high.append(0)

            try:
                decayed_permanent_teeth.append(round(decayed_permanent_teeth[3]/decayed_permanent_teeth[1],2))
            except:
                decayed_permanent_teeth.append(0)

            try:
                decayed_primary_teeth.append(round(decayed_primary_teeth[3]/decayed_primary_teeth[1],2))
            except:
                decayed_primary_teeth.append(0)

            try:
                cavity_permanent_molar.append(round(cavity_permanent_molar[3]/cavity_permanent_molar[1],2))
            except:
                cavity_permanent_molar.append(0)

            try:
                cavity_permanent_anterior.append(round(cavity_permanent_anterior[3]/cavity_permanent_anterior[1],2))
            except:
                cavity_permanent_anterior.append(0)

            try:
                 active_proportional = round(active_real_difference/total_active_infection,2)
            except:
                active_proportional = 0

            try:
                reversible_pulpitis_proportional = round(reversible_pulpitis_real_difference/total_reversible_pulpitis,2)
            except:
                reversible_pulpitis_proportional = 0

            try:
                art_proportional = round(art_real_difference/total_need_art_filling,2)
            except:
                art_proportional = 0

            try:
                sdf_proportional = round(sdf_real_difference/total_need_sdf,2)
            except:
                sdf_proportional = 0

            try:
                extraction_proportional = round(extraction_real_difference/total_need_extraction,2)
            except:
                extraction_proportional = 0

            return Response([carries_risk,carries_risk_low,\
            carries_risk_medium,carries_risk_high,\
            decayed_primary_teeth,decayed_permanent_teeth,\
            cavity_permanent_molar,cavity_permanent_anterior,\
            ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional],\
            ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional],\
            ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional],\
            ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional],\
            ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional]])

    # def post(self, request, format=None):
    #     serializer = SectionalVisualizationSerializer(data=request.data,context={'request': request})
    #     if serializer.is_valid():
    #         start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
    #         end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
    #         location = serializer.validated_data['location']
    #         carries_risk=["Carries Risk"]
    #         carries_risk_low=['<span class="ml-4">Low</span>']
    #         carries_risk_medium=['<span class="ml-4">Medium</span>']
    #         carries_risk_high=['<span class="ml-4">High</span>']
    #         decayed_permanent_teeth = ["Number of decayed permanent teeth"]
    #         decayed_primary_teeth = ["Number of decayed primary teeth"]
    #         cavity_permanent_molar= ["Cavity permanent molar or premolar"]
    #         cavity_permanent_anterior = ["Cavity permanent anterior"]
    #
    #         total_active_infection=Visualization.objects.filter(active_infection=True).count()
    #         carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
    #         carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
    #         carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
    #         decayed_primary_teeth=[]
    #         permanent_molar_teeth=[]
    #         for i in Visualization.objects.all():
    #             decayed_primary_teeth.append(i.decayed_primary_teeth_number)
    #             permanent_molar_teeth.append(i.decayed_permanent_teeth_number)
    #
    #         try:
    #             decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth),2))
    #             decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
    #         except:
    #             decayed_primary_teeth.append(0)
    #             decayed_permanent_teeth.append(0)
    #
    #
    #         total_patients = Visualization.objects.all().count()
    #
    #         total_cavity_permanent_posterior_teeth=Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
    #         try:
    #             cavity_permanent_molar.append((total_cavity_permanent_posterior_teeth/total_patients)*100)
    #         except:
    #             cavity_permanent_molar.append(0)
    #
    #
    #         total_cavity_permanent_anterior_teeth=Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
    #         try:
    #             cavity_permanent_anterior.append((total_cavity_permanent_anterior_teeth/total_patients)*100)
    #         except:
    #             cavity_permanent_anterior.append(0)
    #
    #         total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True).count()
    #
    #
    #         total_need_art_filling=Visualization.objects.filter(need_art_filling=True).count()
    #         total_need_sdf=Visualization.objects.filter(need_sdf=True).count()
    #         total_need_extraction=Visualization.objects.filter(need_extraction=True).count()
    #
    #         return Response([carries_risk,carries_risk_low,carries_risk_medium,carries_risk_high,decayed_primary_teeth,decayed_permanent_teeth,\
    #         cavity_permanent_molar,cavity_permanent_anterior,\
    #         ["Active Infection",total_active_infection],\
    #         ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis],\
    #         ["Need ART filling",total_need_art_filling],\
    #         ["Need SDF",total_need_sdf],\
    #         ["Need Extraction",total_need_extraction]])
    #     return Response({"message":serializer.errors},status=400)
