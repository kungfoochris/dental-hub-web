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
OverViewVisualization,LongitudinalVisualizationSerializer


from scipy.stats import mannwhitneyu

from scipy.stats import kruskal

from scipy.stats import chisquare

from scipy.stats import wilcoxon


# from datetime import datetime
# from datetime import timedelta
import logging
# Get an instance of a logger
from django.db.models import Count

logger = logging.getLogger(__name__)


import scipy.stats


def mcnemar_p(b, c):
    n = b + c
    x = min(b, c)
    dist = scipy.stats.binom(n, .5)
    print(dist)
    print(dir(dist))
    return (2. * dist.cdf(x)- dist.pmf(x))


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

# testing
class TestLongitudinalVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = LongitudinalVisualizationSerializer

    def get(self, request,format=None):
        if User.objects.filter(id=request.user.id).exists():
            carries_risk=["Carries Risk"]
            total_carries_risk_low = ['<span class="ml-4">Low</span>']
            total_carries_risk_medium = ['<span class="ml-4">Medium</span>']
            total_carries_risk_high = ['<span class="ml-4">High</span>']
            total_decayed_permanent_teeth = ["Number of decayed permanent teeth"]
            total_decayed_primary_teeth = ["Number of decayed primary teeth"]
            total_cavity_permanent_molar = ["Cavity permanent molar or premolar"]
            total_cavity_permanent_anterior = ["Cavity permanent anterior"]
            total_active_infection = Visualization.objects.filter(active_infection=True).count()

            total_carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
            total_carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
            try:
                total_carries_risk_low.append(round(carries_risk_low[1]/carries_risk_low[2],2))
            except:
                total_carries_risk_low.append(0)
            try:
                total_carries_risk_low.append(round(carries_risk_low[3]/carries_risk_low[1],2))
            except:
                total_carries_risk_low.append(0)
            
            if(total_carries_risk_low[1] or total_carries_risk_low[2] !=0):
                carries_risk_low_pvalue = chisquare([total_carries_risk_low[2],total_carries_risk_low[3]])
                total_carries_risk_low.append(round(carries_risk_low_pvalue[2],2))
            else:
                total_carries_risk_low.append(0)

            
            total_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Low").count())
            total_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Low").count())
            try:
                total_carries_risk_medium.append(round(carries_risk_low[1]/carries_risk_low[2],2))
            except:
                total_carries_risk_medium.append(0)
            try:
                total_carries_risk_medium.append(round(carries_risk_low[3]/carries_risk_low[1],2))
            except:
                total_carries_risk_medium.append(0)
            
            if(total_carries_risk_medium[1] or total_carries_risk_medium[2] !=0):
                carries_risk_low_pvalue = chisquare([total_carries_risk_medium[2],total_carries_risk_medium[3]])
                total_carries_risk_medium.append(round(carries_risk_low_pvalue[2],2))
            else:
                total_carries_risk_medium.append(0)

            
            total_carries_risk_high.append(Visualization.objects.filter(carries_risk="Low").count())
            total_carries_risk_high.append(Visualization.objects.filter(carries_risk="Low").count())
            try:
                total_carries_risk_high.append(round(carries_risk_low[1]/carries_risk_low[2],2))
            except:
                total_carries_risk_high.append(0)
            try:
                total_carries_risk_high.append(round(carries_risk_low[3]/carries_risk_low[1],2))
            except:
                total_carries_risk_high.append(0)
            
            if(total_carries_risk_high[1] or total_carries_risk_high[2] !=0):
                carries_risk_low_pvalue = chisquare([total_carries_risk_high[2],total_carries_risk_high[3]])
                total_carries_risk_high.append(round(carries_risk_low_pvalue[2],2))
            else:
                total_carries_risk_high.append(0)
            

            # Number of decayed primary teeth
            decayed_primary_teeth1=[]
            for i in Visualization.objects.all():
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1=[]
            for i in Visualization.objects.all():
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
            except:
                total_decayed_primary_teeth.append(0)
            
            try:
                total_decayed_primary_teeth.append(round(total_decayed_primary_teeth[1]/total_decayed_primary_teeth[2],2))
            except:
                total_decayed_primary_teeth.append(0)
            
            try:
                total_decayed_primary_teeth.append(round(total_decayed_primary_teeth[3]/total_decayed_primary_teeth[1],2))
            except:
                total_decayed_primary_teeth.append(0)
            
            try:
                stat5, decayed_permanent_teeth_pvalue = kruskal([total_decayed_primary_teeth[1]], [total_decayed_primary_teeth[2]])
                total_decayed_primary_teeth.append(round(decayed_permanent_teeth_pvalue,2))
            except:
                total_decayed_primary_teeth.append(0.0)



            # Number of decayed permanent teeth
            decayed_permanent_teeth1=[]
            for i in Visualization.objects.all():
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1=[]
            for i in Visualization.objects.all():
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            try:
                total_decayed_permanent_teeth.append(round(total_decayed_permanent_teeth[1]/total_decayed_permanent_teeth[2],2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            try:
                total_decayed_permanent_teeth.append(round(total_decayed_permanent_teeth[3]/total_decayed_permanent_teeth[1],2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            try:
                stat5, decayed_permanent_teeth_pvalue = kruskal([total_decayed_permanent_teeth[1]], [total_decayed_permanent_teeth[2]])
                total_decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
            except:
                total_decayed_permanent_teeth.append(0.0)

            
            # Cavity permanent molar or premolar
            total_patients = Visualization.objects.all().count()
            cavity_permanent_posterior_teeth = Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
            try:
                total_cavity_permanent_molar.append(round((cavity_permanent_posterior_teeth/total_patients)*100,2))
            except:
                total_cavity_permanent_molar.append(0)
            

            total_patients = Visualization.objects.all().count()
            cavity_permanent_posterior_teeth = Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
            try:
                total_cavity_permanent_molar.append(round((cavity_permanent_posterior_teeth/total_patients)*100,2))
            except:
                total_cavity_permanent_molar.append(0)
            
            try:
                total_cavity_permanent_molar.append(round(total_cavity_permanent_molar[1]/total_cavity_permanent_molar[2],2))
            except:
                total_cavity_permanent_molar.append(0)
            
            try:
                total_cavity_permanent_molar.append(round(total_cavity_permanent_molar[3]/total_cavity_permanent_molar[1],2))
            except:
                total_cavity_permanent_molar.append(0)
            
            if(total_cavity_permanent_molar[1] or total_cavity_permanent_molar[2] !=0):
                cavity_permanent_molar_pvalue = chisquare([total_cavity_permanent_molar[1],total_cavity_permanent_molar[2]])
                total_cavity_permanent_molar.append(round(total_cavity_permanent_molar_pvalue[1],2))
            else:
                total_cavity_permanent_molar.append(0)
            

            # Cavity permanent anterior
            total_patients = Visualization.objects.all().count()
            cavity_permanent_anterior = Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
            try:
                total_cavity_permanent_anterior.append(round((cavity_permanent_anterior/total_patients)*100,2))
            except:
                total_cavity_permanent_anterior.append(0)
        

            total_patients = Visualization.objects.all().count()
            cavity_permanent_anterior = Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
            try:
                total_cavity_permanent_anterior.append(round((cavity_permanent_anterior/total_patients)*100,2))
            except:
                total_cavity_permanent_anterior.append(0)
            
            try:
                total_cavity_permanent_anterior.append(round(total_cavity_permanent_anterior[1]/total_cavity_permanent_anterior[2],2))
            except:
                total_cavity_permanent_anterior.append(0)
            
            try:
                total_cavity_permanent_anterior.append(round(total_cavity_permanent_anterior[3]/total_cavity_permanent_anterior[1],2))
            except:
                total_cavity_permanent_anterior.append(0)
            
            if(total_cavity_permanent_anterior[1] or total_cavity_permanent_anterior[2] !=0):
                cavity_permanent_molar_pvalue = chisquare([total_cavity_permanent_anterior[1],total_cavity_permanent_anterior[2]])
                total_cavity_permanent_anterior.append(round(total_cavity_permanent_molar_pvalue[1],2))
            else:
                total_cavity_permanent_anterior.append(0)
            
            # Active Infection
            active_infection = Visualization.objects.filter(active_infection=True).count()
            active_infection = Visualization.objects.filter(active_infection=True).count()
            try:
                active_real_difference = round(active_infection/active_infection1,2)
            except:
                active_real_difference = 0
            
            try:
                 active_proportional = round(active_real_difference/active_infection,2)
            except:
                active_proportional = 0
            
            if(active_infection or active_infection != 0):
                active_infection_pvalue = round(chisquare([active_infection,active_infection])[1],2)
            else:
                active_infection_pvalue = 0
            
            # Mouth pain due to reversible pulpitis
            total_reversible_pulpitis1 = Visualization.objects.filter(reversible_pulpitis=True).count()
            total_reversible_pulpitis1 = Visualization.objects.filter(reversible_pulpitis=True).count()
            try:
                reversible_pulpitis_real_difference = round(total_reversible_pulpitis/total_reversible_pulpitis1,2)
            except:
                reversible_pulpitis_real_difference = 0
            
            try:
                reversible_pulpitis_proportional = round(reversible_pulpitis_real_difference/total_reversible_pulpitis,2)
            except:
                reversible_pulpitis_proportional = 0
            
            if(total_reversible_pulpitis or total_reversible_pulpitis1 != 0):
                reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis,total_reversible_pulpitis1])[1],2)
            else:
                reversible_pulpitis_pvalue = 0


            # Need ART filling
            total_need_art_filling1=Visualization.objects.filter(need_art_filling=True).count()
            try:
                art_real_difference = round(total_need_art_filling/total_need_art_filling1,2)
            except:
                art_real_difference = 0
            if(total_need_art_filling or total_need_art_filling1 != 0):
                need_art_filling_pvalue = round(chisquare([total_need_art_filling,total_need_art_filling1])[1],2)
            else:
                need_art_filling_pvalue = 0





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

            #fourth
            if(carries_risk_low[1] or carries_risk_low[2] !=0):
                carries_risk_low_pvalue = chisquare([carries_risk_low[1],carries_risk_low[2]])
                carries_risk_low.append(round(carries_risk_low_pvalue[1],2))
            else:
                carries_risk_low.append(0)

            if(carries_risk_medium[1] or carries_risk_medium[2] != 0):
                carries_risk_medium_pvalue = chisquare([carries_risk_medium[1],carries_risk_medium[2]])
                carries_risk_medium.append(round(carries_risk_medium_pvalue[1],2))
            else:
                carries_risk_medium.append(0)

            if(carries_risk_high[1] or carries_risk_high[2] != 0):
                carries_risk_high_pvalue = chisquare([carries_risk_high[1],carries_risk_high[2]])
                carries_risk_high.append(round(carries_risk_high_pvalue[1],2))
            else:
                carries_risk_high.append(0)


            try:
                stat4, decayed_primary_teeth_pvalue = kruskal([decayed_primary_teeth[1]], [decayed_primary_teeth[2]])
                decayed_primary_teeth.append(round(decayed_primary_teeth_pvalue,2))
            except:
                decayed_primary_teeth.append(0)

            try:
                stat5, decayed_permanent_teeth_pvalue = kruskal([decayed_permanent_teeth[1]], [decayed_permanent_teeth[2]])
                decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
            except:
                decayed_permanent_teeth.append(0.0)

            if(cavity_permanent_molar[1] or cavity_permanent_molar[2] !=0):
                cavity_permanent_molar_pvalue = chisquare([cavity_permanent_molar[1],cavity_permanent_molar[2]])
                cavity_permanent_molar.append(round(cavity_permanent_molar_pvalue[1],2))
            else:
                cavity_permanent_molar.append(0)


            if(cavity_permanent_anterior[1] or cavity_permanent_anterior[2] != 0):
                cavity_permanent_anterior_pvalue = chisquare([cavity_permanent_anterior[1],cavity_permanent_anterior[2]])
                cavity_permanent_anterior.append(round(cavity_permanent_anterior_pvalue[1],2))
            else:
                cavity_permanent_anterior.append(0)

            if(total_active_infection or total_active_infection != 0):
                active_infection_pvalue = round(chisquare([total_active_infection,total_active_infection])[1],2)
            else:
                active_infection_pvalue = 0

            if(total_reversible_pulpitis or total_reversible_pulpitis1 != 0):
                reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis,total_reversible_pulpitis1])[1],2)
            else:
                reversible_pulpitis_pvalue = 0

            if(total_need_art_filling or total_need_art_filling1 != 0):
                need_art_filling_pvalue = round(chisquare([total_need_art_filling,total_need_art_filling1])[1],2)
            else:
                need_art_filling_pvalue = 0

            if(total_need_sdf or total_need_sdf1 != 0):
                need_sdf_pvalue = round(chisquare([total_need_sdf,total_need_sdf1])[1],2)
            else:
                need_sdf_pvalue = 0

            if(total_need_extraction or total_need_extraction1 != 0):
                need_extraction_pvalue = round(chisquare([total_need_extraction,total_need_extraction1])[1],2)
            else:
                need_extraction_pvalue = 0
            


            return Response([carries_risk,carries_risk_low,\
            carries_risk_medium,carries_risk_high,\
            decayed_primary_teeth,decayed_permanent_teeth,\
            cavity_permanent_molar,cavity_permanent_anterior,\
            ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional,active_infection_pvalue],\
            ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional,reversible_pulpitis_pvalue],\
            ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional,
            ],\
            ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional,need_sdf_pvalue],\
            ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional,need_extraction_pvalue]])

    def post(self, request, format=None):
        serializer = LongitudinalVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            frame1_start_date = str(NepaliDate.from_date(serializer.validated_data['frame1_start_date']))
            frame1_end_date = str(NepaliDate.from_date(serializer.validated_data['frame1_end_date']))
            frame2_start_date = str(NepaliDate.from_date(serializer.validated_data['frame2_start_date']))
            frame2_end_date = str(NepaliDate.from_date(serializer.validated_data['frame2_end_date']))
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

            if(frame1_end_date > frame1_start_date):
                if(frame2_end_date > frame2_start_date):
                    total_active_infection=Visualization.objects.filter(active_infection=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    decayed_primary_teeth1=[]
                    permanent_molar_teeth=[]
                    for i in Visualization.objects.filter(created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)):
                        decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                        permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

                    try:
                        decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                        decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
                    except:
                        decayed_primary_teeth.append(0)
                        decayed_permanent_teeth.append(0)


                    total_patients = Visualization.objects.filter(created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                    total_cavity_permanent_posterior_teeth=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth/total_patients)*100,2))
                    except:
                        cavity_permanent_molar.append(0)


                    total_cavity_permanent_anterior_teeth=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth/total_patients)*100,2))
                    except:
                        cavity_permanent_anterior.append(0)

                    total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    total_need_art_filling=Visualization.objects.filter(need_art_filling=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_sdf=Visualization.objects.filter(need_sdf=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_extraction=Visualization.objects.filter(need_extraction=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    #second
                    total_active_infection1=Visualization.objects.filter(active_infection=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    decayed_primary_teeth1=[]
                    permanent_molar_teeth=[]
                    for i in Visualization.objects.filter(created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)):
                        decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                        permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

                    try:
                        decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                        decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
                    except:
                        decayed_primary_teeth.append(0)
                        decayed_permanent_teeth.append(0)


                    total_patients1 = Visualization.objects.filter(created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                    total_cavity_permanent_posterior_teeth1=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth1/total_patients1)*100,2))
                    except:
                        cavity_permanent_molar.append(0)


                    total_cavity_permanent_anterior_teeth1=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth1/total_patients1)*100,2))
                    except:
                        cavity_permanent_anterior.append(0)

                    total_reversible_pulpitis1=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    total_need_art_filling1=Visualization.objects.filter(need_art_filling=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_sdf1=Visualization.objects.filter(need_sdf=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_extraction1=Visualization.objects.filter(need_extraction=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
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

                    #fourth

                    if(carries_risk_low[1] or carries_risk_low[2] !=0):
                        carries_risk_low_pvalue = chisquare([carries_risk_low[1],carries_risk_low[2]])
                        carries_risk_low.append(round(carries_risk_low_pvalue[1],2))
                    else:
                        carries_risk_low.append(0)

                    if(carries_risk_medium[1] or carries_risk_medium[2] != 0):
                        carries_risk_medium_pvalue = chisquare([carries_risk_medium[1],carries_risk_medium[2]])
                        carries_risk_medium.append(round(carries_risk_medium_pvalue[1],2))
                    else:
                        carries_risk_medium.append(0)

                    if(carries_risk_high[1] or carries_risk_high[2] != 0):
                        carries_risk_high_pvalue = chisquare([carries_risk_high[1],carries_risk_high[2]])
                        carries_risk_high.append(round(carries_risk_high_pvalue[1],2))
                    else:
                        carries_risk_high.append(0)


                    try:
                        stat4, decayed_primary_teeth_pvalue = kruskal([decayed_primary_teeth[1]], [decayed_primary_teeth[2]])
                        decayed_primary_teeth.append(round(decayed_primary_teeth_pvalue,2))
                    except:
                        decayed_primary_teeth.append(0)

                    try:
                        stat5, decayed_permanent_teeth_pvalue = kruskal([decayed_permanent_teeth[1]], [decayed_permanent_teeth[2]])
                        decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
                    except:
                        decayed_permanent_teeth.append(0.0)

                    if(cavity_permanent_molar[1] or cavity_permanent_molar[2] !=0):
                        cavity_permanent_molar_pvalue = chisquare([cavity_permanent_molar[1],cavity_permanent_molar[2]])
                        cavity_permanent_molar.append(round(cavity_permanent_molar_pvalue[1],2))
                    else:
                        cavity_permanent_molar.append(0)


                    if(cavity_permanent_anterior[1] or cavity_permanent_anterior[2] != 0):
                        cavity_permanent_anterior_pvalue = chisquare([cavity_permanent_anterior[1],cavity_permanent_anterior[2]])
                        cavity_permanent_anterior.append(round(cavity_permanent_anterior_pvalue[1],2))
                    else:
                        cavity_permanent_anterior.append(0)

                    if(total_active_infection or total_active_infection != 0):
                        active_infection_pvalue = round(chisquare([total_active_infection,total_active_infection])[1],2)
                    else:
                        active_infection_pvalue = 0

                    if(total_reversible_pulpitis or total_reversible_pulpitis1 != 0):
                        reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis,total_reversible_pulpitis1])[1],2)
                    else:
                        reversible_pulpitis_pvalue = 0

                    if(total_need_art_filling or total_need_art_filling1 != 0):
                        need_art_filling_pvalue = round(chisquare([total_need_art_filling,total_need_art_filling1])[1],2)
                    else:
                        need_art_filling_pvalue = 0

                    if(total_need_sdf or total_need_sdf1 != 0):
                        need_sdf_pvalue = round(chisquare([total_need_sdf,total_need_sdf1])[1],2)
                    else:
                        need_sdf_pvalue = 0

                    if(total_need_extraction or total_need_extraction1 != 0):
                        need_extraction_pvalue = round(chisquare([total_need_extraction,total_need_extraction1])[1],2)
                    else:
                        need_extraction_pvalue = 0

                    return Response([carries_risk,carries_risk_low,\
                    carries_risk_medium,carries_risk_high,\
                    decayed_primary_teeth,decayed_permanent_teeth,\
                    cavity_permanent_molar,cavity_permanent_anterior,\
                    ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional,active_infection_pvalue],\
                    ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional,reversible_pulpitis_pvalue],\
                    ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional,need_art_filling_pvalue],\
                    ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional,need_sdf_pvalue],\
                    ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional,need_extraction_pvalue]])
                return Response({"message":"Frame 2 End date must be greated then Frame 2 Start Date"},status=400)
            return Response({"message":"Frame 1 End date must be greated then Frame 1 Start Date"},status=400)
        return Response({"message":serializer.errors},status=400)

class LongitudinalVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = LongitudinalVisualizationSerializer

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

            #fourth
            if(carries_risk_low[1] or carries_risk_low[2] !=0):
                carries_risk_low_pvalue = chisquare([carries_risk_low[1],carries_risk_low[2]])
                carries_risk_low.append(round(carries_risk_low_pvalue[1],2))
            else:
                carries_risk_low.append(0)

            if(carries_risk_medium[1] or carries_risk_medium[2] != 0):
                carries_risk_medium_pvalue = chisquare([carries_risk_medium[1],carries_risk_medium[2]])
                carries_risk_medium.append(round(carries_risk_medium_pvalue[1],2))
            else:
                carries_risk_medium.append(0)

            if(carries_risk_high[1] or carries_risk_high[2] != 0):
                carries_risk_high_pvalue = chisquare([carries_risk_high[1],carries_risk_high[2]])
                carries_risk_high.append(round(carries_risk_high_pvalue[1],2))
            else:
                carries_risk_high.append(0)


            try:
                stat4, decayed_primary_teeth_pvalue = kruskal([decayed_primary_teeth[1]], [decayed_primary_teeth[2]])
                decayed_primary_teeth.append(round(decayed_primary_teeth_pvalue,2))
            except:
                decayed_primary_teeth.append(0)

            try:
                stat5, decayed_permanent_teeth_pvalue = kruskal([decayed_permanent_teeth[1]], [decayed_permanent_teeth[2]])
                decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
            except:
                decayed_permanent_teeth.append(0.0)

            if(cavity_permanent_molar[1] or cavity_permanent_molar[2] !=0):
                cavity_permanent_molar_pvalue = chisquare([cavity_permanent_molar[1],cavity_permanent_molar[2]])
                cavity_permanent_molar.append(round(cavity_permanent_molar_pvalue[1],2))
            else:
                cavity_permanent_molar.append(0)


            if(cavity_permanent_anterior[1] or cavity_permanent_anterior[2] != 0):
                cavity_permanent_anterior_pvalue = chisquare([cavity_permanent_anterior[1],cavity_permanent_anterior[2]])
                cavity_permanent_anterior.append(round(cavity_permanent_anterior_pvalue[1],2))
            else:
                cavity_permanent_anterior.append(0)

            if(total_active_infection or total_active_infection != 0):
                active_infection_pvalue = round(chisquare([total_active_infection,total_active_infection])[1],2)
            else:
                active_infection_pvalue = 0

            if(total_reversible_pulpitis or total_reversible_pulpitis1 != 0):
                reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis,total_reversible_pulpitis1])[1],2)
            else:
                reversible_pulpitis_pvalue = 0

            if(total_need_art_filling or total_need_art_filling1 != 0):
                need_art_filling_pvalue = round(chisquare([total_need_art_filling,total_need_art_filling1])[1],2)
            else:
                need_art_filling_pvalue = 0

            if(total_need_sdf or total_need_sdf1 != 0):
                need_sdf_pvalue = round(chisquare([total_need_sdf,total_need_sdf1])[1],2)
            else:
                need_sdf_pvalue = 0

            if(total_need_extraction or total_need_extraction1 != 0):
                need_extraction_pvalue = round(chisquare([total_need_extraction,total_need_extraction1])[1],2)
            else:
                need_extraction_pvalue = 0

            return Response([carries_risk,carries_risk_low,\
            carries_risk_medium,carries_risk_high,\
            decayed_primary_teeth,decayed_permanent_teeth,\
            cavity_permanent_molar,cavity_permanent_anterior,\
            ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional,active_infection_pvalue],\
            ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional,reversible_pulpitis_pvalue],\
            ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional,
            ],\
            ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional,need_sdf_pvalue],\
            ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional,need_extraction_pvalue]])

    def post(self, request, format=None):
        serializer = LongitudinalVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            frame1_start_date = str(NepaliDate.from_date(serializer.validated_data['frame1_start_date']))
            frame1_end_date = str(NepaliDate.from_date(serializer.validated_data['frame1_end_date']))
            frame2_start_date = str(NepaliDate.from_date(serializer.validated_data['frame2_start_date']))
            frame2_end_date = str(NepaliDate.from_date(serializer.validated_data['frame2_end_date']))
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

            if(frame1_end_date > frame1_start_date):
                if(frame2_end_date > frame2_start_date):
                    total_active_infection=Visualization.objects.filter(active_infection=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    decayed_primary_teeth1=[]
                    permanent_molar_teeth=[]
                    for i in Visualization.objects.filter(created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)):
                        decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                        permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

                    try:
                        decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                        decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
                    except:
                        decayed_primary_teeth.append(0)
                        decayed_permanent_teeth.append(0)


                    total_patients = Visualization.objects.filter(created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                    total_cavity_permanent_posterior_teeth=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth/total_patients)*100,2))
                    except:
                        cavity_permanent_molar.append(0)


                    total_cavity_permanent_anterior_teeth=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth/total_patients)*100,2))
                    except:
                        cavity_permanent_anterior.append(0)

                    total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    total_need_art_filling=Visualization.objects.filter(need_art_filling=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_sdf=Visualization.objects.filter(need_sdf=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_extraction=Visualization.objects.filter(need_extraction=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    #second
                    total_active_infection1=Visualization.objects.filter(active_infection=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    decayed_primary_teeth1=[]
                    permanent_molar_teeth=[]
                    for i in Visualization.objects.filter(created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)):
                        decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                        permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

                    try:
                        decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                        decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
                    except:
                        decayed_primary_teeth.append(0)
                        decayed_permanent_teeth.append(0)


                    total_patients1 = Visualization.objects.filter(created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                    total_cavity_permanent_posterior_teeth1=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth1/total_patients1)*100,2))
                    except:
                        cavity_permanent_molar.append(0)


                    total_cavity_permanent_anterior_teeth1=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth1/total_patients1)*100,2))
                    except:
                        cavity_permanent_anterior.append(0)

                    total_reversible_pulpitis1=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    total_need_art_filling1=Visualization.objects.filter(need_art_filling=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_sdf1=Visualization.objects.filter(need_sdf=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_extraction1=Visualization.objects.filter(need_extraction=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
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

                    #fourth

                    if(carries_risk_low[1] or carries_risk_low[2] !=0):
                        carries_risk_low_pvalue = chisquare([carries_risk_low[1],carries_risk_low[2]])
                        carries_risk_low.append(round(carries_risk_low_pvalue[1],2))
                    else:
                        carries_risk_low.append(0)

                    if(carries_risk_medium[1] or carries_risk_medium[2] != 0):
                        carries_risk_medium_pvalue = chisquare([carries_risk_medium[1],carries_risk_medium[2]])
                        carries_risk_medium.append(round(carries_risk_medium_pvalue[1],2))
                    else:
                        carries_risk_medium.append(0)

                    if(carries_risk_high[1] or carries_risk_high[2] != 0):
                        carries_risk_high_pvalue = chisquare([carries_risk_high[1],carries_risk_high[2]])
                        carries_risk_high.append(round(carries_risk_high_pvalue[1],2))
                    else:
                        carries_risk_high.append(0)


                    try:
                        stat4, decayed_primary_teeth_pvalue = kruskal([decayed_primary_teeth[1]], [decayed_primary_teeth[2]])
                        decayed_primary_teeth.append(round(decayed_primary_teeth_pvalue,2))
                    except:
                        decayed_primary_teeth.append(0)

                    try:
                        stat5, decayed_permanent_teeth_pvalue = kruskal([decayed_permanent_teeth[1]], [decayed_permanent_teeth[2]])
                        decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
                    except:
                        decayed_permanent_teeth.append(0.0)

                    if(cavity_permanent_molar[1] or cavity_permanent_molar[2] !=0):
                        cavity_permanent_molar_pvalue = chisquare([cavity_permanent_molar[1],cavity_permanent_molar[2]])
                        cavity_permanent_molar.append(round(cavity_permanent_molar_pvalue[1],2))
                    else:
                        cavity_permanent_molar.append(0)


                    if(cavity_permanent_anterior[1] or cavity_permanent_anterior[2] != 0):
                        cavity_permanent_anterior_pvalue = chisquare([cavity_permanent_anterior[1],cavity_permanent_anterior[2]])
                        cavity_permanent_anterior.append(round(cavity_permanent_anterior_pvalue[1],2))
                    else:
                        cavity_permanent_anterior.append(0)

                    if(total_active_infection or total_active_infection != 0):
                        active_infection_pvalue = round(chisquare([total_active_infection,total_active_infection])[1],2)
                    else:
                        active_infection_pvalue = 0

                    if(total_reversible_pulpitis or total_reversible_pulpitis1 != 0):
                        reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis,total_reversible_pulpitis1])[1],2)
                    else:
                        reversible_pulpitis_pvalue = 0

                    if(total_need_art_filling or total_need_art_filling1 != 0):
                        need_art_filling_pvalue = round(chisquare([total_need_art_filling,total_need_art_filling1])[1],2)
                    else:
                        need_art_filling_pvalue = 0

                    if(total_need_sdf or total_need_sdf1 != 0):
                        need_sdf_pvalue = round(chisquare([total_need_sdf,total_need_sdf1])[1],2)
                    else:
                        need_sdf_pvalue = 0

                    if(total_need_extraction or total_need_extraction1 != 0):
                        need_extraction_pvalue = round(chisquare([total_need_extraction,total_need_extraction1])[1],2)
                    else:
                        need_extraction_pvalue = 0

                    return Response([carries_risk,carries_risk_low,\
                    carries_risk_medium,carries_risk_high,\
                    decayed_primary_teeth,decayed_permanent_teeth,\
                    cavity_permanent_molar,cavity_permanent_anterior,\
                    ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional,active_infection_pvalue],\
                    ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional,reversible_pulpitis_pvalue],\
                    ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional,need_art_filling_pvalue],\
                    ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional,need_sdf_pvalue],\
                    ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional,need_extraction_pvalue]])
                return Response({"message":"Frame 2 End date must be greated then Frame 2 Start Date"},status=400)
            return Response({"message":"Frame 1 End date must be greated then Frame 1 Start Date"},status=400)
        return Response({"message":serializer.errors},status=400)



class LongitudinalVisualization1(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = LongitudinalVisualizationSerializer

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

            #fourth
            if(carries_risk_low[1] or carries_risk_low[2] !=0):
                carries_risk_low_pvalue = chisquare([carries_risk_low[1],carries_risk_low[2]])
                carries_risk_low.append(carries_risk_low_pvalue[1])
            else:
                carries_risk_low.append(0)

            if(carries_risk_medium[1] or carries_risk_medium[2] != 0):
                carries_risk_medium_pvalue = chisquare([carries_risk_medium[1],carries_risk_medium[2]])
                carries_risk_medium.append(carries_risk_medium_pvalue[1])
            else:
                carries_risk_medium.append(0)

            if(carries_risk_high[1] or carries_risk_high[2] != 0):
                carries_risk_high_pvalue = chisquare([carries_risk_high[1],carries_risk_high[2]])
                carries_risk_high.append(carries_risk_high_pvalue[1])
            else:
                carries_risk_high.append(0)


            try:
                stat4, decayed_primary_teeth_pvalue = kruskal([decayed_primary_teeth[1]], [decayed_primary_teeth[2]])
                decayed_primary_teeth.append(decayed_primary_teeth_pvalue)
            except:
                decayed_primary_teeth.append(0)

            try:
                stat5, decayed_permanent_teeth_pvalue = kruskal([decayed_permanent_teeth[1]], [decayed_permanent_teeth[2]])
                decayed_permanent_teeth.append(decayed_permanent_teeth_pvalue)
            except:
                decayed_permanent_teeth.append(0.0)

            if(cavity_permanent_molar[1] or cavity_permanent_molar[2] !=0):
                cavity_permanent_molar_pvalue = chisquare([cavity_permanent_molar[1],cavity_permanent_molar[2]])
                cavity_permanent_molar.append(cavity_permanent_molar_pvalue[1])
            else:
                cavity_permanent_molar.append(0)


            if(cavity_permanent_anterior[1] or cavity_permanent_anterior[2] != 0):
                cavity_permanent_anterior_pvalue = chisquare([cavity_permanent_anterior[1],cavity_permanent_anterior[2]])
                cavity_permanent_anterior.append(cavity_permanent_anterior_pvalue[1])
            else:
                cavity_permanent_anterior.append(0)

            if(total_active_infection or total_active_infection != 0):
                active_infection_pvalue = chisquare([total_active_infection,total_active_infection])[1]
            else:
                active_infection_pvalue = 0

            if(total_reversible_pulpitis or total_reversible_pulpitis1 != 0):
                reversible_pulpitis_pvalue = chisquare([total_reversible_pulpitis,total_reversible_pulpitis1])[1]
            else:
                reversible_pulpitis_pvalue = 0

            if(total_need_art_filling or total_need_art_filling1 != 0):
                need_art_filling_pvalue = chisquare([total_need_art_filling,total_need_art_filling1])[1]
            else:
                need_art_filling_pvalue = 0

            if(total_need_sdf or total_need_sdf1 != 0):
                need_sdf_pvalue = chisquare([total_need_sdf,total_need_sdf1])[1]
            else:
                need_sdf_pvalue = 0

            if(total_need_extraction or total_need_extraction1 != 0):
                need_extraction_pvalue = chisquare([total_need_extraction,total_need_extraction1])[1]
            else:
                need_extraction_pvalue = 0

            return Response([carries_risk,carries_risk_low,\
            carries_risk_medium,carries_risk_high,\
            decayed_primary_teeth,decayed_permanent_teeth,\
            cavity_permanent_molar,cavity_permanent_anterior,\
            ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional,active_infection_pvalue],\
            ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional,reversible_pulpitis_pvalue],\
            ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional,
            ],\
            ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional,need_sdf_pvalue],\
            ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional,need_extraction_pvalue]])

    def post(self, request, format=None):
        serializer = LongitudinalVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            frame1_start_date = str(NepaliDate.from_date(serializer.validated_data['frame1_start_date']))
            frame1_end_date = str(NepaliDate.from_date(serializer.validated_data['frame1_end_date']))
            frame2_start_date = str(NepaliDate.from_date(serializer.validated_data['frame2_start_date']))
            frame2_end_date = str(NepaliDate.from_date(serializer.validated_data['frame2_end_date']))
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


            if(frame1_end_date > frame1_start_date):
                if(frame2_end_date > frame2_start_date):
                    total_active_infection=Visualization.objects.filter(active_infection=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    decayed_primary_teeth1=[]
                    permanent_molar_teeth=[]
                    for i in Visualization.objects.filter(created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)):
                        decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                        permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

                    try:
                        decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                        decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
                    except:
                        decayed_primary_teeth.append(0)
                        decayed_permanent_teeth.append(0)


                    total_patients = Visualization.objects.filter(created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                    total_cavity_permanent_posterior_teeth=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth/total_patients)*100,2))
                    except:
                        cavity_permanent_molar.append(0)


                    total_cavity_permanent_anterior_teeth=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth/total_patients)*100,2))
                    except:
                        cavity_permanent_anterior.append(0)

                    total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    total_need_art_filling=Visualization.objects.filter(need_art_filling=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_sdf=Visualization.objects.filter(need_sdf=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_extraction=Visualization.objects.filter(need_extraction=True,created_at__range=[frame1_start_date,frame1_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    #second
                    total_active_infection1=Visualization.objects.filter(active_infection=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count())
                    decayed_primary_teeth1=[]
                    permanent_molar_teeth=[]
                    for i in Visualization.objects.filter(created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)):
                        decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
                        permanent_molar_teeth.append(i.decayed_permanent_teeth_number)

                    try:
                        decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
                        decayed_permanent_teeth.append(round(statistics.stdev(permanent_molar_teeth),2))
                    except:
                        decayed_primary_teeth.append(0)
                        decayed_permanent_teeth.append(0)


                    total_patients1 = Visualization.objects.filter(created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

                    total_cavity_permanent_posterior_teeth1=Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_molar.append(round((total_cavity_permanent_posterior_teeth1/total_patients1)*100,2))
                    except:
                        cavity_permanent_molar.append(0)


                    total_cavity_permanent_anterior_teeth1=Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    try:
                        cavity_permanent_anterior.append(round((total_cavity_permanent_anterior_teeth1/total_patients1)*100,2))
                    except:
                        cavity_permanent_anterior.append(0)

                    total_reversible_pulpitis1=Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


                    total_need_art_filling1=Visualization.objects.filter(need_art_filling=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_sdf1=Visualization.objects.filter(need_sdf=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
                    total_need_extraction1=Visualization.objects.filter(need_extraction=True,created_at__range=[frame2_start_date,frame2_end_date],reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
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

                    #fourth
                    carries_risk_low_pvalue = mcnemar_p(carries_risk_low[1],carries_risk_low[2])
                    carries_risk_low.append(round(carries_risk_low_pvalue,2))

                    carries_risk_medium_pvalue = mcnemar_p(carries_risk_medium[1],carries_risk_medium[2])
                    carries_risk_medium.append(round(carries_risk_medium_pvalue,2))


                    carries_risk_high_pvalue =  mcnemar_p(carries_risk_high[1],carries_risk_high[2])
                    carries_risk_high.append(round(carries_risk_high_pvalue,2))



                    try:
                        stat4, decayed_primary_teeth_pvalue = wilcoxon([decayed_primary_teeth[1]], [decayed_primary_teeth[2]])
                        decayed_primary_teeth.append(round(decayed_primary_teeth_pvalue,2))
                    except:
                        decayed_primary_teeth.append(0)

                    try:
                        stat5, decayed_permanent_teeth_pvalue = wilcoxon([decayed_permanent_teeth[1]], [decayed_permanent_teeth[2]])
                        decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
                    except:
                        decayed_permanent_teeth.append(0.0)

                    cavity_permanent_molar_pvalue = mcnemar_p(cavity_permanent_molar[1],cavity_permanent_molar[2])
                    cavity_permanent_molar.append(round(cavity_permanent_molar_pvalue,2))

                    cavity_permanent_anterior_pvalue =  mcnemar_p(cavity_permanent_anterior[1],cavity_permanent_anterior[2])
                    cavity_permanent_anterior.append(round(cavity_permanent_anterior_pvalue,2))

                    active_infection_pvalue = round(mcnemar_p(total_active_infection,total_active_infection),2)

                    reversible_pulpitis_pvalue = round(mcnemar_p(total_reversible_pulpitis,total_reversible_pulpitis1),2)

                    need_art_filling_pvalue = round(mcnemar_p(total_need_art_filling,total_need_art_filling1),2)

                    need_sdf_pvalue = round(mcnemar_p(total_need_sdf,total_need_sdf1),2)

                    need_extraction_pvalue = round(mcnemar_p(total_need_extraction,total_need_extraction1),2)

                    return Response([carries_risk,carries_risk_low,\
                    carries_risk_medium,carries_risk_high,\
                    decayed_primary_teeth,decayed_permanent_teeth,\
                    cavity_permanent_molar,cavity_permanent_anterior,\
                    ["Active Infection",total_active_infection,total_active_infection1,active_real_difference,active_proportional,active_infection_pvalue],\
                    ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis,total_reversible_pulpitis1,reversible_pulpitis_real_difference,reversible_pulpitis_proportional,reversible_pulpitis_pvalue],\
                    ["Need ART filling",total_need_art_filling,total_need_art_filling1,art_real_difference,art_proportional,need_art_filling_pvalue],\
                    ["Need SDF",total_need_sdf,total_need_sdf1,sdf_real_difference,sdf_proportional,need_sdf_pvalue],\
                    ["Need Extraction",total_need_extraction,total_need_extraction1,extraction_real_difference,extraction_proportional,need_extraction_pvalue]])
                return Response({"message":"Frame 2 End date must be greated then Frame 2 Start Date"},status=400)
            return Response({"message":"Frame 1 End date must be greated then Frame 1 Start Date"},status=400)
        return Response({"message":serializer.errors},status=400)
