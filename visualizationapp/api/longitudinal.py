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
OverViewVisualization,LongitudinalVisualizationSerializer,TestLongitudinalVisualizationSerializer


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
    serializer_class = TestLongitudinalVisualizationSerializer

    def get(self, request,format=None):
        if User.objects.filter(id=request.user.id).exists():
            carries_risk = ["Carries Risk"]
            total_carries_risk_low = ['<span class="ml-4">Low</span>']
            total_carries_risk_medium = ['<span class="ml-4">Medium</span>']
            total_carries_risk_high = ['<span class="ml-4">High</span>']
            total_untreated_caries_present=["Any untreated caries present"]
            total_decayed_permanent_teeth = ["Number of decayed permanent teeth"]
            total_decayed_primary_teeth = ["Number of decayed primary teeth"]
            total_cavity_permanent_molar = ["Cavity permanent molar or premolar"]
            total_cavity_permanent_anterior = ["Cavity permanent anterior"]
            total_active_infection = ["Active Infection"]
            total_reversible_pulpitis = ["Mouth pain due to reversible pulpitis"]
            total_need_art_filling = ["Need ART filling"]
            total_need_sdf = ["Need SDF"]
            total_need_extraction = ["Need Extraction"]
            total_need_fv = ["Need FV"]
            total_need_dentist_or_hygienist = ["Need Dentist or Hygenist"]
            total = []


            # carries risk low
            total_carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
            total_carries_risk_low.append(Visualization.objects.filter(carries_risk="Low").count())
            try:
                total_carries_risk_low.append(abs(round(total_carries_risk_low[1] - total_carries_risk_low[2],2)))
            except:
                total_carries_risk_low.append(0)
            try:
                total_carries_risk_low.append(round(total_carries_risk_low[3]/total_carries_risk_low[1],2))
            except:
                total_carries_risk_low.append(0)
            
            if total_carries_risk_low[4] < 0.2:
                total_carries_risk_low.append("small")
            elif total_carries_risk_low[4] >= 0.2 and total_carries_risk_low[4] <= 0.6:
                total_carries_risk_low.append("medium")
            else:
                total_carries_risk_low.append("large")
            
            if(total_carries_risk_low[1] or total_carries_risk_low[2] !=0):
                carries_risk_low_pvalue = chisquare([total_carries_risk_low[2],total_carries_risk_low[3]])
                total_carries_risk_low.append(round(carries_risk_low_pvalue[2],2))
            else:
                total_carries_risk_low.append(0)
            

            
            # carries risk medium
            total_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
            total_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
            try:
                total_carries_risk_medium.append(abs(round(total_carries_risk_medium[1] - total_carries_risk_medium[2],2)))
            except:
                total_carries_risk_medium.append(0)
            try:
                total_carries_risk_medium.append(round(total_carries_risk_medium[3]/total_carries_risk_medium[1],2))
            except:
                total_carries_risk_medium.append(0)
            
            if total_carries_risk_medium[4] < 0.2:
                total_carries_risk_medium.append("small")
            elif total_carries_risk_medium[4] >= 0.2 and total_carries_risk_medium[4] <= 0.6:
                total_carries_risk_medium.append("medium")
            else:
                total_carries_risk_medium.append("large")
            
            if(total_carries_risk_medium[1] or total_carries_risk_medium[2] !=0):
                carries_risk_low_pvalue = chisquare([total_carries_risk_medium[2],total_carries_risk_medium[3]])
                total_carries_risk_medium.append(round(carries_risk_low_pvalue[2],2))
            else:
                total_carries_risk_medium.append(0)

            
            # carries risk high
            total_carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
            total_carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
            try:
                total_carries_risk_high.append(abs(round(total_carries_risk_high[1] - total_carries_risk_high[2],2)))
            except:
                total_carries_risk_high.append(0)
            try:
                total_carries_risk_high.append(round(total_carries_risk_high[3]/total_carries_risk_high[1],2))
            except:
                total_carries_risk_high.append(0)
            
            if total_carries_risk_high[4] < 0.2:
                total_carries_risk_high.append("small")
            elif total_carries_risk_high[4] >= 0.2 and total_carries_risk_high[4] <= 0.6:
                total_carries_risk_high.append("medium")
            else:
                total_carries_risk_high.append("large")
            
            if(total_carries_risk_high[1] or total_carries_risk_high[2] !=0):
                carries_risk_low_pvalue = chisquare([total_carries_risk_high[2],total_carries_risk_high[3]])
                total_carries_risk_high.append(round(carries_risk_low_pvalue[2],2))
            else:
                total_carries_risk_high.append(0)

            # Any untreated caries present
            total_untreated_caries_present.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).count())
            total_untreated_caries_present.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).count())
            try:
                total_untreated_caries_present.append(abs(round(total_untreated_caries_present[1] - total_untreated_caries_present[2],2)))
            except:
                total_untreated_caries_present.append(0)
            try:
                total_untreated_caries_present.append(round(total_untreated_caries_present[3]/total_untreated_caries_present[1],2))
            except:
                total_untreated_caries_present.append(0)
            
            if total_untreated_caries_present[4] < 0.2:
                total_untreated_caries_present.append("small")
            elif total_untreated_caries_present[4] >= 0.2 and total_untreated_caries_present[4] <= 0.6:
                total_untreated_caries_present.append("medium")
            else:
                total_untreated_caries_present.append("large")
            
            
            if(total_untreated_caries_present[1] or total_untreated_caries_present[2] !=0):
                untreated_caries_present_pvalue = chisquare([total_untreated_caries_present[2],total_untreated_caries_present[3]])
                total_untreated_caries_present.append(round(untreated_caries_present_pvalue[2],2))
            else:
                total_untreated_caries_present.append(0)
            

            # Number of decayed primary teeth
            decayed_primary_teeth1 = []
            for i in Visualization.objects.all():
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.all():
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),2))
            except:
                total_decayed_primary_teeth.append(0)
            
            try:
                total_decayed_primary_teeth.append(abs(round(total_decayed_primary_teeth[1] - total_decayed_primary_teeth[2],2)))
            except:
                total_decayed_primary_teeth.append(0)
            
            try:
                total_decayed_primary_teeth.append(round(total_decayed_primary_teeth[3]/total_decayed_primary_teeth[1],2))
            except:
                total_decayed_primary_teeth.append(0)
            
            if total_decayed_primary_teeth[4] < 0.2:
                total_decayed_primary_teeth.append("small")
            elif total_decayed_primary_teeth[4] >= 0.2 and total_decayed_primary_teeth[4] <= 0.6:
                total_decayed_primary_teeth.append("medium")
            else:
                total_decayed_primary_teeth.append("large")
            
            try:
                stat5, decayed_permanent_teeth_pvalue = kruskal([total_decayed_primary_teeth[1]], [total_decayed_primary_teeth[2]])
                total_decayed_primary_teeth.append(round(decayed_permanent_teeth_pvalue,2))
            except:
                total_decayed_primary_teeth.append(0.0)



            # Number of decayed permanent teeth
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.all():
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.all():
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            try:
                total_decayed_permanent_teeth.append(abs(round(total_decayed_permanent_teeth[1] - total_decayed_permanent_teeth[2],2)))
            except:
                total_decayed_permanent_teeth.append(0)
            
            try:
                total_decayed_permanent_teeth.append(round(total_decayed_permanent_teeth[3]/total_decayed_permanent_teeth[1],2))
            except:
                total_decayed_permanent_teeth.append(0)
            
            if total_decayed_permanent_teeth[4] < 0.2:
                total_decayed_permanent_teeth.append("small")
            elif total_decayed_permanent_teeth[4] >= 0.2 and total_decayed_permanent_teeth[4] <= 0.6:
                total_decayed_permanent_teeth.append("medium")
            else:
                total_decayed_permanent_teeth.append("large")
            
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
                total_cavity_permanent_molar.append(abs(round(total_cavity_permanent_molar[1] - total_cavity_permanent_molar[2],2)))
            except:
                total_cavity_permanent_molar.append(0)
            
            try:
                total_cavity_permanent_molar.append(round(total_cavity_permanent_molar[3]/total_cavity_permanent_molar[1],2))
            except:
                total_cavity_permanent_molar.append(0)
            
            if total_cavity_permanent_molar[4] < 0.2:
                total_cavity_permanent_molar.append("small")
            elif total_cavity_permanent_molar[4] >= 0.2 and total_cavity_permanent_molar[4] <= 0.6:
                total_cavity_permanent_molar.append("medium")
            else:
                total_cavity_permanent_molar.append("large")
            
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
                total_cavity_permanent_anterior.append(abs(round(total_cavity_permanent_anterior[1] - total_cavity_permanent_anterior[2],2)))
            except:
                total_cavity_permanent_anterior.append(0)
            
            try:
                total_cavity_permanent_anterior.append(round(total_cavity_permanent_anterior[3]/total_cavity_permanent_anterior[1],2))
            except:
                total_cavity_permanent_anterior.append(0)
            
            if total_cavity_permanent_anterior[4] < 0.2:
                total_cavity_permanent_anterior.append("small")
            elif total_cavity_permanent_anterior[4] >= 0.2 and total_cavity_permanent_anterior[4] <= 0.6:
                total_cavity_permanent_anterior.append("medium")
            else:
                total_cavity_permanent_anterior.append("large")
            
            if(total_cavity_permanent_anterior[1] or total_cavity_permanent_anterior[2] !=0):
                cavity_permanent_molar_pvalue = chisquare([total_cavity_permanent_anterior[1],total_cavity_permanent_anterior[2]])
                total_cavity_permanent_anterior.append(round(total_cavity_permanent_molar_pvalue[1],2))
            else:
                total_cavity_permanent_anterior.append(0)
            
            # Active Infection
            total_active_infection.append(Visualization.objects.filter(active_infection=True).count())
            total_active_infection.append(Visualization.objects.filter(active_infection=True).count())
            total_active_infection.append(abs(round(total_active_infection[1]  - total_active_infection[2],2)))
            try:
                active_proportional = round(total_active_infection[3]/total_active_infection[1],2)
            except:
                active_proportional = 0
            total_active_infection.append(active_proportional)

            if total_active_infection[4] < 0.2:
                total_active_infection.append("small")
            elif total_active_infection[4] >= 0.2 and total_active_infection[4] <= 0.6:
                total_active_infection.append("medium")
            else:
                total_active_infection.append("large")
            
            if(total_active_infection[1] or total_active_infection[2] != 0):
                active_infection_pvalue = round(chisquare([active_infection,active_infection])[1],2)
            else:
                active_infection_pvalue = 0
            total_active_infection.append(active_infection_pvalue)
            
            # Mouth pain due to reversible pulpitis
            total_reversible_pulpitis.append(Visualization.objects.filter(reversible_pulpitis=True).count())
            total_reversible_pulpitis.append(Visualization.objects.filter(reversible_pulpitis=True).count())
            total_reversible_pulpitis.append(abs(round(total_reversible_pulpitis[1] - total_reversible_pulpitis[2],2)))
            try:
                reversible_pulpitis_proportional = round(reversible_pulpitis_real_difference[3]/total_reversible_pulpitis[1],2)
            except:
                reversible_pulpitis_proportional = 0
            total_reversible_pulpitis.append(reversible_pulpitis_proportional)
            
            if total_reversible_pulpitis[4] < 0.2:
                total_reversible_pulpitis.append("small")
            elif total_reversible_pulpitis[4] >= 0.2 and total_reversible_pulpitis[4] <= 0.6:
                total_reversible_pulpitis.append("medium")
            else:
                total_reversible_pulpitis.append("large")

            if(total_reversible_pulpitis[1] or total_reversible_pulpitis[2] != 0):
                reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis[1],total_reversible_pulpitis[2]])[1],2)
            else:
                reversible_pulpitis_pvalue = 0
            total_reversible_pulpitis.append(reversible_pulpitis_pvalue)


            # Need ART filling
            total_need_art_filling.append(Visualization.objects.filter(need_art_filling=True).count())
            total_need_art_filling.append(Visualization.objects.filter(need_art_filling=True).count())
            total_need_art_filling.append(abs(round(total_need_art_filling[1] - total_need_art_filling[2],2)))
            try:
                art_proportional = round(total_need_art_filling[3]/total_need_art_filling[1],2)
            except:
                art_proportional = 0
            total_need_art_filling.append(art_proportional)

            if total_need_art_filling[4] < 0.2:
                total_need_art_filling.append("small")
            elif total_need_art_filling[4] >= 0.2 and total_need_art_filling[4] <= 0.6:
                total_need_art_filling.append("medium")
            else:
                total_need_art_filling.append("large")

            if(total_need_art_filling[1] or total_need_art_filling[2] != 0):
                need_art_filling_pvalue = round(chisquare([total_need_art_filling[1],total_need_art_filling[2]])[1],2)
            else:
                need_art_filling_pvalue = 0
            total_need_art_filling.append(need_art_filling_pvalue)


            # Need SDF
            total_need_sdf.append(Visualization.objects.filter(need_sdf=True).count())
            total_need_sdf.append(Visualization.objects.filter(need_sdf=True).count())
            total_need_sdf.append(abs(round(total_need_sdf[1] - total_need_sdf[2],2)))
   
            try:
                sdf_proportional = round(sdf_real_difference/total_need_sdf[1],2)
            except:
                sdf_proportional = 0
            total_need_sdf.append(sdf_proportional)

            if total_need_sdf[4] < 0.2:
                total_need_sdf.append("small")
            elif total_need_sdf[4] >= 0.2 and total_need_sdf[4] <= 0.6:
                total_need_sdf.append("medium")
            else:
                total_need_sdf.append("large")

            if(total_need_sdf[1] or total_need_sdf[2] != 0):
                need_sdf_pvalue = round(chisquare([total_need_sdf[1],total_need_sdf[2]])[1],2)
            else:
                need_sdf_pvalue = 0
            total_need_sdf.append(need_sdf_pvalue)

            
            # Need Extraction
            total_need_extraction.append(Visualization.objects.filter(need_extraction=True).count())
            total_need_extraction.append(Visualization.objects.filter(need_extraction=True).count())
            total_need_extraction.append(abs(round(total_need_extraction[1] - total_need_extraction[2],2)))
            try:
                extraction_proportional = round(total_need_extraction[3]/total_need_extraction[1],2)
            except:
                extraction_proportional = 0
            total_need_extraction.append(extraction_proportional)

            if total_need_extraction[4] < 0.2:
                total_need_extraction.append("small")
            elif total_need_extraction[4] >= 0.2 and total_need_extraction[4] <= 0.6:
                total_need_extraction.append("medium")
            else:
                total_need_extraction.append("large")

            if(total_need_extraction[1] or total_need_extraction[2] != 0):
                need_extraction_pvalue = round(chisquare([total_need_extraction[1],total_need_extraction[2]])[1],2)
            else:
                need_extraction_pvalue = 0
            total_need_extraction.append(need_extraction_pvalue)


            # Need FV
            total_need_fv.append(Visualization.objects.filter(need_fv=True).count())
            total_need_fv.append(Visualization.objects.filter(need_fv=True).count())
            total_need_fv.append(abs(round(total_need_fv[1] - total_need_fv[2],2)))
            try:
                fv_proportional = round(total_need_fv[3]/total_need_fv[1],2)
            except:
                fv_proportional = 0
            total_need_fv.append(fv_proportional)

            if total_need_extraction[4] < 0.2:
                total_need_extraction.append("small")
            elif total_need_extraction[4] >= 0.2 and total_need_extraction[4] <= 0.6:
                total_need_extraction.append("medium")
            else:
                total_need_extraction.append("large")

            if(total_need_fv[1] or total_need_fv[2] != 0):
                need_fv_pvalue = round(chisquare([total_need_fv[1],total_need_fv[2]])[1],2)
            else:
                need_fv_pvalue = 0
            total_need_fv.append(need_fv_pvalue)

            # Need Dentist or Hygenist
            total_need_dentist_or_hygienist.append(Visualization.objects.filter(need_dentist_or_hygienist=True).count())
            total_need_dentist_or_hygienist.append(Visualization.objects.filter(need_dentist_or_hygienist=True).count())
            total_need_dentist_or_hygienist.append(abs(round(total_need_dentist_or_hygienist[1] - total_need_dentist_or_hygienist[2],2)))
            try:
                dentist_or_hygienist_proportional = round(total_need_dentist_or_hygienist[3]/total_need_dentist_or_hygienist[1],2)
            except:
                dentist_or_hygienist_proportional = 0
            total_need_dentist_or_hygienist.append(dentist_or_hygienist_proportional)

            if total_need_dentist_or_hygienist[4] < 0.2:
                total_need_dentist_or_hygienist.append("small")
            elif total_need_dentist_or_hygienist[4] >= 0.2 and total_need_dentist_or_hygienist[4] <= 0.6:
                total_need_dentist_or_hygienist.append("medium")
            else:
                total_need_dentist_or_hygienist.append("large")

            if(total_need_dentist_or_hygienist[1] or total_need_dentist_or_hygienist[2] != 0):
                need_dentist_or_hygienist_pvalue = round(chisquare([total_need_dentist_or_hygienist[1],total_need_dentist_or_hygienist[2]])[1],2)
            else:
                need_dentist_or_hygienist_pvalue = 0
            total_need_dentist_or_hygienist.append(need_dentist_or_hygienist_pvalue)

            
            data = [
                carries_risk,
                total_carries_risk_low ,
                total_carries_risk_medium ,
                total_carries_risk_high ,
                total_untreated_caries_present,
                total_decayed_permanent_teeth ,
                total_decayed_primary_teeth ,
                total_cavity_permanent_molar ,
                total_cavity_permanent_anterior ,
                total_active_infection,
                total_reversible_pulpitis ,
                total_need_art_filling ,
                total_need_sdf,
                total_need_extraction,
                total_need_fv,
                total_need_dentist_or_hygienist
                ]
            
            return Response(data)



    def post(self, request, format=None):
        serializer = TestLongitudinalVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date1 = str(NepaliDate.from_date(serializer.validated_data['frame1_start_date']))
            end_date1 = str(NepaliDate.from_date(serializer.validated_data['frame1_end_date']))
            start_date2 = str(NepaliDate.from_date(serializer.validated_data['frame2_start_date']))
            end_date2 = str(NepaliDate.from_date(serializer.validated_data['frame2_end_date']))
            reason_for_visit  = serializer.validated_data['reason_for_visit']

            if start_date1 > end_date1:
                return Response({"message":"Frame1 start date cannot be later than end date."},status=400)
            if start_date2 > end_date2:
                return Response({"message":"Frame2 start date cannot be later than end date."},status=400)
            if User.objects.filter(id=request.user.id).exists():
                carries_risk=["Carries Risk"]
                total_carries_risk_low = ['<span class="ml-4">Low</span>']
                total_carries_risk_medium = ['<span class="ml-4">Medium</span>']
                total_carries_risk_high = ['<span class="ml-4">High</span>']
                total_untreated_caries_present=["Any untreated caries present"]
                total_decayed_permanent_teeth = ["Number of decayed permanent teeth"]
                total_decayed_primary_teeth = ["Number of decayed primary teeth"]
                total_cavity_permanent_molar = ["Cavity permanent molar or premolar"]
                total_cavity_permanent_anterior = ["Cavity permanent anterior"]
                total_active_infection = ["Active Infection"]
                total_reversible_pulpitis = ["Mouth pain due to reversible pulpitis"]
                total_need_art_filling = ["Need ART filling"]
                total_need_sdf = ["Need SDF"]
                total_need_extraction = ["Need Extraction"]
                total_need_fv = ["Need FV"]
                total_need_dentist_or_hygienist = ["Need Dentist or Hygenist"]


                reason_for_visit = serializer.validated_data['reason_for_visit']
                referral_type = serializer.validated_data['referral_type']
                
                if serializer.validated_data['age_group'] == "Child ≤12 Y":
                    start_age = 0
                    end_age = 12
                if serializer.validated_data['age_group'] == "Teen 13-18 Y":
                    start_age = 13
                    end_age = 18
                if serializer.validated_data['age_group'] == "Adult 19-60 Y":
                    start_age = 19
                    end_age = 60
                if serializer.validated_data['age_group'] == "Older Adult ≥61 Y":
                    start_age = 60
                    end_age = 200
                if serializer.validated_data['age_group'] == "6 Y":
                    start_age = 6
                    end_age = 7
                if serializer.validated_data['age_group'] == "12 Y":
                    start_age = 12
                    end_age = 13
                if serializer.validated_data['age_group'] == "15 Y":
                    start_age = 15
                    end_age = 16
                


                # carries risk low
                frame1_carries_risk_low = []
                frame2_carries_risk_low = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_carries_risk_low.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_carries_risk_low.append(sum(frame1_carries_risk_low))
                total_carries_risk_low.append(sum(frame2_carries_risk_low))
                try:
                    total_carries_risk_low.append(abs(round(carries_risk_low[1] - carries_risk_low[2],2)))
                except:
                    total_carries_risk_low.append(0)
                try:
                    total_carries_risk_low.append(round(carries_risk_low[3]/carries_risk_low[1],2))
                except:
                    total_carries_risk_low.append(0)
                
                if total_carries_risk_low[4] < 0.2:
                    total_carries_risk_low.append("small")
                elif total_carries_risk_low[4] >= 0.2 and total_carries_risk_low[4] <= 0.6:
                    total_carries_risk_low.append("medium")
                else:
                    total_carries_risk_low.append("large")
                
                if(total_carries_risk_low[1] or total_carries_risk_low[2] !=0):
                    carries_risk_low_pvalue = chisquare([total_carries_risk_low[2],total_carries_risk_low[3]])
                    total_carries_risk_low.append(round(carries_risk_low_pvalue[2],2))
                else:
                    total_carries_risk_low.append(0)

                
                # carries risk medium
                frame1_carries_risk_medium = []
                frame2_carries_risk_medium = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
                total_carries_risk_medium.append(Visualization.objects.filter(carries_risk="Medium").count())
                try:
                    total_carries_risk_medium.append(abs(round(total_carries_risk_medium[1] - total_carries_risk_medium[2],2)))
                except:
                    total_carries_risk_medium.append(0)
                try:
                    total_carries_risk_medium.append(round(total_carries_risk_medium[3]/total_carries_risk_medium[1],2))
                except:
                    total_carries_risk_medium.append(0)
                
                if total_carries_risk_medium[4] < 0.2:
                    total_carries_risk_medium.append("small")
                elif total_carries_risk_medium[4] >= 0.2 and total_carries_risk_medium[4] <= 0.6:
                    total_carries_risk_medium.append("medium")
                else:
                    total_carries_risk_medium.append("large")
                
                if(total_carries_risk_medium[1] or total_carries_risk_medium[2] !=0):
                    carries_risk_medium_pvalue = chisquare([total_carries_risk_medium[2],total_carries_risk_medium[3]])
                    total_carries_risk_medium.append(round(carries_risk_medium_pvalue[2],2))
                else:
                    total_carries_risk_medium.append(0)

                
                # carries risk high
                frame1_carries_risk_high = []
                frame2_carries_risk_high = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_carries_risk_high.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
                total_carries_risk_high.append(Visualization.objects.filter(carries_risk="High").count())
                try:
                    total_carries_risk_high.append(abs(round(total_carries_risk_high[1]/total_carries_risk_high[2],2)))
                except:
                    total_carries_risk_high.append(0)
                try:
                    total_carries_risk_high.append(round(total_carries_risk_high[3]/total_carries_risk_high[1],2))
                except:
                    total_carries_risk_high.append(0)
                
                if total_carries_risk_high[4] < 0.2:
                    total_carries_risk_high.append("small")
                elif total_carries_risk_high[4] >= 0.2 and total_carries_risk_high[4] <= 0.6:
                    total_carries_risk_high.append("medium")
                else:
                    total_carries_risk_high.append("large")
                
                if(total_carries_risk_high[1] or total_carries_risk_high[2] !=0):
                    carries_risk_high_pvalue = chisquare([total_carries_risk_high[2],total_carries_risk_high[3]])
                    total_carries_risk_high.append(round(carries_risk_high_pvalue[2],2))
                else:
                    total_carries_risk_high.append(0)
                

                # untreated caries present
                frame1_untreated_caries_present = []
                frame2_untreated_caries_present = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_untreated_caries_present.append(Visualization.objects.filter(created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).count())
                        frame2_untreated_caries_present.append(Visualization.objects.filter(created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).count())
                
                total_untreated_caries_present.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).count())
                total_untreated_caries_present.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).count())
                try:
                    total_untreated_caries_present.append(abs(round(total_untreated_caries_present[1]/total_untreated_caries_present[2],2)))
                except:
                    total_untreated_caries_present.append(0)
                try:
                    total_untreated_caries_present.append(round(total_untreated_caries_present[3]/total_untreated_caries_present[1],2))
                except:
                    total_untreated_caries_present.append(0)
                
                if total_untreated_caries_present[4] < 0.2:
                    total_untreated_caries_present.append("small")
                elif total_untreated_caries_present[4] >= 0.2 and total_untreated_caries_present[4] <= 0.6:
                    total_untreated_caries_present.append("medium")
                else:
                    total_untreated_caries_present.append("large")
                
                if(total_untreated_caries_present[1] or total_untreated_caries_present[2] !=0):
                    untreated_caries_present_pvalue = chisquare([total_untreated_caries_present[2],total_untreated_caries_present[3]])
                    total_untreated_caries_present.append(round(untreated_caries_present_pvalue[2],2))
                else:
                    total_untreated_caries_present.append(0)
                

                # Number of decayed primary teeth
                frame1_total_decayed_primary_teeth = []
                frame2_total_decayed_primary_teeth = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        for x in Visualization.objects.filter(created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type):
                            frame1_total_decayed_primary_teeth.append(x.decayed_primary_teeth_number)
                        for y in Visualization.objects.filter(created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type):
                            frame2_total_decayed_primary_teeth.append(y.decayed_primary_teeth_number)                

                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(frame1_decayed_primary_teeth),2))
                except:
                    total_decayed_primary_teeth.append(0)
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(frame2_decayed_primary_teeth),2))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(abs(round(total_decayed_primary_teeth[1] - total_decayed_primary_teeth[2],2)))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(total_decayed_primary_teeth[3]/total_decayed_primary_teeth[1],2))
                except:
                    total_decayed_primary_teeth.append(0)
                
                if total_decayed_primary_teeth[4] < 0.2:
                    total_decayed_primary_teeth.append("small")
                elif total_decayed_primary_teeth[4] >= 0.2 and total_decayed_primary_teeth[4] <= 0.6:
                    total_decayed_primary_teeth.append("medium")
                else:
                    total_decayed_primary_teeth.append("large")
                
                try:
                    stat5, decayed_permanent_teeth_pvalue = kruskal([total_decayed_primary_teeth[1]], [total_decayed_primary_teeth[2]])
                    total_decayed_primary_teeth.append(round(decayed_permanent_teeth_pvalue,2))
                except:
                    total_decayed_primary_teeth.append(0.0)



                # Number of decayed permanent teeth
                frame1_total_decayed_permanent_teeth = []
                frame2_total_decayed_permanent_teeth = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        for x in Visualization.objects.filter(created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type):
                            frame1_total_decayed_permanent_teeth.append(x.decayed_permanent_teeth_number)
                        for y in Visualization.objects.filter(created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type):
                            frame2_total_decayed_permanent_teeth.append(y.decayed_permanent_teeth_number)                

                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(frame1_total_decayed_permanent_teeth),2))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(frame2_total_decayed_permanent_teeth),2))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(abs(round(total_decayed_permanent_teeth[1] - total_decayed_permanent_teeth[2],2)))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(total_decayed_permanent_teeth[3]/total_decayed_permanent_teeth[1],2))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                if total_decayed_permanent_teeth[4] < 0.2:
                    total_decayed_permanent_teeth.append("small")
                elif total_decayed_permanent_teeth[4] >= 0.2 and total_decayed_permanent_teeth[4] <= 0.6:
                    total_decayed_permanent_teeth.append("medium")
                else:
                    total_decayed_permanent_teeth.append("large")
                
                try:
                    stat5, decayed_permanent_teeth_pvalue = kruskal([total_decayed_permanent_teeth[1]], [total_decayed_permanent_teeth[2]])
                    total_decayed_permanent_teeth.append(round(decayed_permanent_teeth_pvalue,2))
                except:
                    total_decayed_permanent_teeth.append(0.0)

                
                # Cavity permanent molar or premolar
                frame1_cavity_permanent_molar = []
                frame2_cavity_permanent_molar = []
                frame1_total_patient = []
                frame2_total_patient = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_cavity_permanent_molar.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_cavity_permanent_molar.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame1_total_patient.append(Visualization.objects.filter(created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_total_patient.append(Visualization.objects.filter(created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())

                try:
                    total_cavity_permanent_molar.append(round((sum(frame1_cavity_permanent_molar)/sum(frame1_total_patient))*100,2))
                except:
                    total_cavity_permanent_molar.append(0)
                
                try:
                    total_cavity_permanent_molar.append(round((sum(frame2_cavity_permanent_molar)/sum(frame2_total_patient))*100,2))
                except:
                    total_cavity_permanent_molar.append(0)
                
                try:
                    total_cavity_permanent_molar.append(abs(round(total_cavity_permanent_molar[1] - total_cavity_permanent_molar[2],2)))
                except:
                    total_cavity_permanent_molar.append(0)
                
                try:
                    total_cavity_permanent_molar.append(round(total_cavity_permanent_molar[3]/total_cavity_permanent_molar[1],2))
                except:
                    total_cavity_permanent_molar.append(0)
                
                if total_cavity_permanent_molar[4] < 0.2:
                    total_cavity_permanent_molar.append("small")
                elif total_cavity_permanent_molar[4] >= 0.2 and total_cavity_permanent_molar[4] <= 0.6:
                    total_cavity_permanent_molar.append("medium")
                else:
                    total_cavity_permanent_molar.append("large")
                
                if(total_cavity_permanent_molar[1] or total_cavity_permanent_molar[2] !=0):
                    cavity_permanent_molar_pvalue = chisquare([total_cavity_permanent_molar[1],total_cavity_permanent_molar[2]])
                    total_cavity_permanent_molar.append(round(total_cavity_permanent_molar_pvalue[1],2))
                else:
                    total_cavity_permanent_molar.append(0)
                

                # Cavity permanent anterior
                frame1_total_cavity_permanent_anterior = []
                frame2_total_cavity_permanent_anterior = []
                frame1_total_patient = []
                frame2_total_patient = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_total_cavity_permanent_anterior.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_total_cavity_permanent_anterior.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame1_total_patient.append(Visualization.objects.filter(created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_total_patient.append(Visualization.objects.filter(created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())

                try:
                    total_cavity_permanent_anterior.append(round((sum(frame1_total_cavity_permanent_anterior)/sum(frame1_total_patient))*100,2))
                except:
                    total_cavity_permanent_anterior.append(0)
            
                try:
                    total_cavity_permanent_anterior.append(round((sum(frame2_total_cavity_permanent_anterior)/sum(frame2_total_patient))*100,2))
                except:
                    total_cavity_permanent_anterior.append(0)
                
                try:
                    total_cavity_permanent_anterior.append(abs(round(total_cavity_permanent_anterior[1] - total_cavity_permanent_anterior[2],2)))
                except:
                    total_cavity_permanent_anterior.append(0)
                
                try:
                    total_cavity_permanent_anterior.append(round(total_cavity_permanent_anterior[3]/total_cavity_permanent_anterior[1],2))
                except:
                    total_cavity_permanent_anterior.append(0)
                
                if total_cavity_permanent_anterior[4] < 0.2:
                    total_cavity_permanent_anterior.append("small")
                elif total_cavity_permanent_anterior[4] >= 0.2 and total_cavity_permanent_anterior[4] <= 0.6:
                    total_cavity_permanent_anterior.append("medium")
                else:
                    total_cavity_permanent_anterior.append("large")
                
                if(total_cavity_permanent_anterior[1] or total_cavity_permanent_anterior[2] !=0):
                    cavity_permanent_molar_pvalue = chisquare([total_cavity_permanent_anterior[1],total_cavity_permanent_anterior[2]])
                    total_cavity_permanent_anterior.append(round(total_cavity_permanent_molar_pvalue[1],2))
                else:
                    total_cavity_permanent_anterior.append(0)
                
                # Active Infection
                frame1_active_infection = []
                frame2_active_infection = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_active_infection.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_active_infection.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_active_infection.append(sum(frame1_active_infection))
                total_active_infection.append(sum(frame2_active_infection))

                total_active_infection.append(abs(round(total_active_infection[1] - total_active_infection[2],2)))
                
                try:
                    active_proportional = round(total_active_infection[3]/total_active_infection[1],2)
                except:
                    active_proportional = 0
                total_active_infection.append(active_proportional)

                if total_active_infection[4] < 0.2:
                    total_active_infection.append("small")
                elif total_active_infection[4] >= 0.2 and total_active_infection[4] <= 0.6:
                    total_active_infection.append("medium")
                else:
                    total_active_infection.append("large")
                
                if(total_active_infection[1] or total_active_infection[2] != 0):
                    active_infection_pvalue = round(chisquare([active_infection,active_infection])[1],2)
                else:
                    active_infection_pvalue = 0
                total_active_infection.append(active_infection_pvalue)
                
                # Mouth pain due to reversible pulpitis
                frame1_reversible_pulpitis = []
                frame2_reversible_pulpitis = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_reversible_pulpitis.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_reversible_pulpitis.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_reversible_pulpitis.append(sum(frame1_reversible_pulpitis))
                total_reversible_pulpitis.append(sum(frame2_reversible_pulpitis))

                total_reversible_pulpitis.append(abs(round(total_reversible_pulpitis[1] - total_reversible_pulpitis[2],2)))
                try:
                    reversible_pulpitis_proportional = round(reversible_pulpitis_real_difference[1]/total_reversible_pulpitis[2],2)
                except:
                    reversible_pulpitis_proportional = 0
                total_reversible_pulpitis.append(reversible_pulpitis_proportional)

                if total_reversible_pulpitis[4] < 0.2:
                    total_reversible_pulpitis.append("small")
                elif total_reversible_pulpitis[4] >= 0.2 and total_reversible_pulpitis[4] <= 0.6:
                    total_reversible_pulpitis.append("medium")
                else:
                    total_reversible_pulpitis.append("large")
                
                if(total_reversible_pulpitis[1] or total_reversible_pulpitis[2] != 0):
                    reversible_pulpitis_pvalue = round(chisquare([total_reversible_pulpitis[1],total_reversible_pulpitis[2]])[1],2)
                else:
                    reversible_pulpitis_pvalue = 0
                total_reversible_pulpitis.append(reversible_pulpitis_pvalue)


                # Need ART filling
                frame1_need_art_filling = []
                frame2_need_art_filling = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_need_art_filling.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_need_art_filling.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_need_art_filling.append(sum(frame1_need_art_filling))
                total_need_art_filling.append(sum(frame2_need_art_filling))

                total_need_art_filling.append(abs(round(total_need_art_filling[1] - total_need_art_filling[2],2)))
                try:
                    art_proportional = round(total_need_art_filling[3]/total_need_art_filling[1],2)
                except:
                    art_proportional = 0
                total_need_art_filling.append(art_proportional)

                if total_need_art_filling[4] < 0.2:
                    total_need_art_filling.append("small")
                elif total_need_art_filling[4] >= 0.2 and total_need_art_filling[4] <= 0.6:
                    total_need_art_filling.append("medium")
                else:
                    total_need_art_filling.append("large")

                if(total_need_art_filling[1] or total_need_art_filling[2] != 0):
                    need_art_filling_pvalue = round(chisquare([total_need_art_filling[1],total_need_art_filling[2]])[1],2)
                else:
                    need_art_filling_pvalue = 0
                total_need_art_filling.append(need_art_filling_pvalue)


                # Need SDF
                frame1_need_sdf = []
                frame2_need_sdf = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_need_sdf.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_need_sdf.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_need_sdf.append(sum(frame1_need_sdf))
                total_need_sdf.append(sum(frame2_need_sdf))

                total_need_sdf(abs(round(total_need_sdf[1] - total_need_sdf[2],2)))
                
                try:
                    sdf_proportional = round(sdf_real_difference/total_need_sdf[1],2)
                except:
                    sdf_proportional = 0
                total_need_sdf.append(sdf_proportional)

                if total_need_sdf[4] < 0.2:
                    total_need_sdf.append("small")
                elif total_need_sdf[4] >= 0.2 and total_need_sdf[4] <= 0.6:
                    total_need_sdf.append("medium")
                else:
                    total_need_sdf.append("large")

                if(total_need_sdf[1] or total_need_sdf[2] != 0):
                    need_sdf_pvalue = round(chisquare([total_need_sdf[1],total_need_sdf[2]])[1],2)
                else:
                    need_sdf_pvalue = 0
                total_need_sdf.append(need_sdf_pvalue)

                
                # Need Extraction
                frame1_need_extraction = []
                frame2_need_extraction = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_need_extraction.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_need_extraction.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_need_extraction.append(sum(frame1_need_extraction))
                total_need_extraction.append(sum(frame2_need_extraction))

                total_need_extraction.append(abs(round(total_need_extraction[1]  - total_need_extraction[2],2)))

                try:
                    extraction_proportional = round(total_need_extraction[3]/total_need_extraction[1],2)
                except:
                    extraction_proportional = 0
                total_need_extraction.append(extraction_proportional)

                if total_need_extraction[4] < 0.2:
                    total_need_extraction.append("small")
                elif total_need_extraction[4] >= 0.2 and total_need_extraction[4] <= 0.6:
                    total_need_extraction.append("medium")
                else:
                    total_need_extraction.append("large")

                if(total_need_extraction[1] or total_need_extraction[2] != 0):
                    need_extraction_pvalue = round(chisquare([total_need_extraction[1],total_need_extraction[2]])[1],2)
                else:
                    need_extraction_pvalue = 0
                total_need_extraction.append(need_extraction_pvalue)


                # Need fv
                frame1_need_fv = []
                frame2_need_fv = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_need_fv.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_need_fv.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_need_fv.append(sum(frame1_need_fv))
                total_need_fv.append(sum(frame2_need_fv))

                total_need_fv.append(abs(round(total_need_fv[1] - total_need_fv[2],2)))
                try:
                    fv_proportional = round(total_need_fv[3]/total_need_fv[1],2)
                except:
                    fv_proportional = 0
                total_need_fv.append(fv_proportional)

                if total_need_fv[4] < 0.2:
                    total_need_fv.append("small")
                elif total_need_fv[4] >= 0.2 and total_need_fv[4] <= 0.6:
                    total_need_fv.append("medium")
                else:
                    total_need_fv.append("large")

                if(total_need_fv[1] or total_need_fv[2] != 0):
                    need_fv_pvalue = round(chisquare([total_need_fv[1],total_need_fv[2]])[1],2)
                else:
                    need_fv_pvalue = 0
                total_need_fv.append(need_fv_pvalue)


                # Need dentist or hygienist
                frame1_need_dentist_or_hygienist = []
                frame2_need_dentist_or_hygienist = []
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        frame1_need_dentist_or_hygienist.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date1, end_date1],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                        frame2_need_dentist_or_hygienist.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date2, end_date2],age__range=[start_age, end_age],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).count())
                
                total_need_dentist_or_hygienist.append(sum(frame1_need_dentist_or_hygienist))
                total_need_dentist_or_hygienist.append(sum(frame2_need_dentist_or_hygienist))

                total_need_dentist_or_hygienist.append(abs(round(total_need_dentist_or_hygienist[1] - total_need_dentist_or_hygienist[2],2)))
                
                try:
                    dentist_or_hygienist_proportional = round(total_need_dentist_or_hygienist[3]/total_need_dentist_or_hygienist[1],2)
                except:
                    dentist_or_hygienist_proportional = 0
                total_need_dentist_or_hygienist.append(dentist_or_hygienist_proportional)

                if total_need_dentist_or_hygienist[4] < 0.2:
                    total_need_dentist_or_hygienist.append("small")
                elif total_need_dentist_or_hygienist[4] >= 0.2 and total_need_dentist_or_hygienist[4] <= 0.6:
                    total_need_dentist_or_hygienist.append("medium")
                else:
                    total_need_dentist_or_hygienist.append("large")

                if(total_need_dentist_or_hygienist[1] or total_need_dentist_or_hygienist[2] != 0):
                    need_dentist_or_hygienist_pvalue = round(chisquare([total_need_dentist_or_hygienist[1],total_need_dentist_or_hygienist[2]])[1],2)
                else:
                    need_dentist_or_hygienist_pvalue = 0
                total_need_dentist_or_hygienist.append(need_dentist_or_hygienist_pvalue)
                
                data = [
                    carries_risk,
                    total_carries_risk_low ,
                    total_carries_risk_medium ,
                    total_carries_risk_high ,
                    total_untreated_caries_present,
                    total_decayed_primary_teeth ,
                    total_decayed_permanent_teeth ,
                    total_cavity_permanent_molar ,
                    total_cavity_permanent_anterior ,
                    total_active_infection,
                    total_reversible_pulpitis ,
                    total_need_art_filling ,
                    total_need_sdf,
                    total_need_extraction,
                    total_need_fv,
                    total_need_dentist_or_hygienist
                    ]
                
                return Response(data)



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
