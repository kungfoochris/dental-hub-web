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

from visualizationapp.serializers.visualization import SectionalVisualizationSerializer,TestCrosssectionVisualizationSerializer,\
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



# testing
class TestCrossSectionalVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TestCrosssectionVisualizationSerializer

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


            # carries risk low
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(carries_risk="Low",age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)

            numerator = Visualization.objects.filter(carries_risk="Low",age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="Low",age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(carries_risk="Low",age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="Low",age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="Low",age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)
            numerator = Visualization.objects.filter(carries_risk="Low",age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_carries_risk_low.append((numerator/denominator)*100)
            except:
                total_carries_risk_low.append(0)

            total_carries_risk_low.append(sum(total_carries_risk_low[1:]))


            # carries risk medium
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(carries_risk="Medium",age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)

            numerator = Visualization.objects.filter(carries_risk="Medium",age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="Medium",age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(carries_risk="Medium",age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="Medium",age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="Medium",age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)
            numerator = Visualization.objects.filter(carries_risk="Medium",age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_carries_risk_medium.append((numerator/denominator)*100)
            except:
                total_carries_risk_medium.append(0)

            total_carries_risk_medium.append(sum(total_carries_risk_medium[1:]))


            # carries risk high
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(carries_risk="High",age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)

            numerator = Visualization.objects.filter(carries_risk="High",age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="High",age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(carries_risk="High",age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="High",age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)
            
            numerator = Visualization.objects.filter(carries_risk="High",age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)
            numerator = Visualization.objects.filter(carries_risk="High",age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_carries_risk_high.append((numerator/denominator)*100)
            except:
                total_carries_risk_high.append(0)

            total_carries_risk_high.append(sum(total_carries_risk_high[1:]))



            # Any untreated caries present
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)

            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)
            
            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)
            
            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)
            
            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)
            numerator = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_untreated_caries_present.append((numerator/denominator)*100)
            except:
                total_untreated_caries_present.append(0)

            total_untreated_caries_present.append(sum(total_untreated_caries_present[1:]))


            # Number of decayed primary teeth
            # WHO indicator age-groups
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age=6):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age=12):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age=15):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            

            # Jevaia's indicator age groups
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age__lt=13):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age__range=[13,18]):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age__range=[19,60]):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(age__gt=60):
                decayed_primary_teeth1.append(i.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
            
            # Number of decayed permanent teeth
            # WHO indicator age-groups
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age=6):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age=12):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age=15):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
            

            # Jevaia's indicator age groups
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age__lt=13):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age__range=[13,18]):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age__range=[19,60]):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(age__gt=60):
                decayed_permanent_teeth1.append(i.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)


            # Cavity permanent molar or premolar
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)

            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)
            
            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)
            
            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)
            
            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)
            numerator = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_cavity_permanent_molar.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_molar.append(0)

            total_cavity_permanent_molar.append(sum(total_cavity_permanent_molar[1:]))


            # Cavity permanent anterior
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)

            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)
            
            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)
            
            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)
            
            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)
            numerator = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_cavity_permanent_anterior.append((numerator/denominator)*100)
            except:
                total_cavity_permanent_anterior.append(0)

            total_cavity_permanent_anterior.append(sum(total_cavity_permanent_anterior[1:]))


            # Active Infection
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(active_infection=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)

            numerator = Visualization.objects.filter(active_infection=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)
            
            numerator = Visualization.objects.filter(active_infection=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(active_infection=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)
            
            numerator = Visualization.objects.filter(active_infection=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)
            
            numerator = Visualization.objects.filter(active_infection=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)
            numerator = Visualization.objects.filter(active_infection=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_active_infection.append((numerator/denominator)*100)
            except:
                total_active_infection.append(0)

            total_active_infection.append(sum(total_active_infection[1:]))


            # Mouth pain due to reversible pulpitis
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(reversible_pulpitis=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)

            numerator = Visualization.objects.filter(reversible_pulpitis=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)
            
            numerator = Visualization.objects.filter(reversible_pulpitis=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(reversible_pulpitis=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)
            
            numerator = Visualization.objects.filter(reversible_pulpitis=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)
            
            numerator = Visualization.objects.filter(reversible_pulpitis=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)
            numerator = Visualization.objects.filter(reversible_pulpitis=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_reversible_pulpitis.append((numerator/denominator)*100)
            except:
                total_reversible_pulpitis.append(0)

            total_reversible_pulpitis.append(sum(total_reversible_pulpitis[1:]))


            # Need ART filling
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(need_art_filling=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)

            numerator = Visualization.objects.filter(need_art_filling=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)
            
            numerator = Visualization.objects.filter(need_art_filling=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(need_art_filling=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)
            
            numerator = Visualization.objects.filter(need_art_filling=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)
            
            numerator = Visualization.objects.filter(need_art_filling=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)
            numerator = Visualization.objects.filter(need_art_filling=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_need_art_filling.append((numerator/denominator)*100)
            except:
                total_need_art_filling.append(0)

            total_need_art_filling.append(sum(total_need_art_filling[1:]))



            # Need SDF
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(need_sdf=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)

            numerator = Visualization.objects.filter(need_sdf=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)
            
            numerator = Visualization.objects.filter(need_sdf=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(need_sdf=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)
            
            numerator = Visualization.objects.filter(need_sdf=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)
            
            numerator = Visualization.objects.filter(need_sdf=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)
            numerator = Visualization.objects.filter(need_sdf=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_need_sdf.append((numerator/denominator)*100)
            except:
                total_need_sdf.append(0)

            total_need_sdf.append(sum(total_need_sdf[1:]))


            # Need Extraction
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(need_extraction=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)

            numerator = Visualization.objects.filter(need_extraction=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)
            
            numerator = Visualization.objects.filter(need_extraction=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(need_extraction=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)
            
            numerator = Visualization.objects.filter(need_extraction=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)
            
            numerator = Visualization.objects.filter(need_extraction=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)
            numerator = Visualization.objects.filter(need_extraction=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_need_extraction.append((numerator/denominator)*100)
            except:
                total_need_extraction.append(0)

            total_need_extraction.append(sum(total_need_extraction[1:]))


            # Need FV
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(need_fv=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)

            numerator = Visualization.objects.filter(need_fv=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)
            
            numerator = Visualization.objects.filter(need_fv=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(need_fv=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)
            
            numerator = Visualization.objects.filter(need_fv=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)
            
            numerator = Visualization.objects.filter(need_fv=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)
            numerator = Visualization.objects.filter(need_fv=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_need_fv.append((numerator/denominator)*100)
            except:
                total_need_fv.append(0)

            total_need_fv.append(sum(total_need_fv[1:]))


            # Need Dentist or Hygenist
            # WHO indicator age-groups
            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age=6).count()
            denominator = Visualization.objects.filter(age=6).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)

            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age=12).count()
            denominator = Visualization.objects.filter(age=12).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)
            
            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age=15).count()
            denominator = Visualization.objects.filter(age=15).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)
            
            # Jevaia's indicator age groups
            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age__lt=13).count()
            denominator = Visualization.objects.filter(age__lt=13).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)
            
            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age__range=[13,18]).count()
            denominator = Visualization.objects.filter(age__range=[13,18]).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)
            
            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age__range=[19,60]).count()
            denominator = Visualization.objects.filter(age__range=[19,60]).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)
            numerator = Visualization.objects.filter(need_dentist_or_hygienist=True,age__gt=60).count()
            denominator = Visualization.objects.filter(age__gt=60).count()
            try:
                total_need_dentist_or_hygienist.append((numerator/denominator)*100)
            except:
                total_need_dentist_or_hygienist.append(0)

            total_need_dentist_or_hygienist.append(sum(total_need_dentist_or_hygienist[1:]))

            
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



    def post(self, request, format=None):
        serializer = TestCrosssectionVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))

            if start_date > end_date:
                return Response({"message":"Start date cannot be later than end date."},status=400)
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
                


                
                numerator_list_6 = []
                denominator_list_6 = []
                numerator_list_12 = []
                denominator_list_12 = []
                numerator_list_15 = []
                denominator_list_15 = []
                numerator_list_lte12  = []
                denominator_list_lte12  = []
                numerator_list_13_18 = []
                denominator_list_13_18 = []
                numerator_list_19_60 = []
                denominator_list_19_60 = []
                numerator_list_gte61  = []
                denominator_list_gte61  = []

                # carries risk low
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_carries_risk_low.append((numerator/denominator)*100)
                except:
                    total_carries_risk_low.append(0)

                total_carries_risk_low.append(sum(total_carries_risk_low[1:]))


                # carries risk medium
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_carries_risk_medium.append((numerator/denominator)*100)
                except:
                    total_carries_risk_medium.append(0)

                total_carries_risk_medium.append(sum(total_carries_risk_medium[1:]))


                # carries risk high
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_carries_risk_high.append((numerator/denominator)*100)
                except:
                    total_carries_risk_high.append(0)

                total_carries_risk_high.append(sum(total_carries_risk_high[1:]))


                # untreated caries present
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_untreated_caries_present.append((numerator/denominator)*100)
                except:
                    total_untreated_caries_present.append(0)

                total_untreated_caries_present.append(sum(total_untreated_caries_present[1:]))


                # Number of decayed primary teeth
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6):
                            numerator_list_6.append(x.decayed_primary_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12):
                            numerator_list_12.append(x.decayed_primary_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15):
                            numerator_list_15.append(x.decayed_primary_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13):
                            numerator_list_lte12.append(x.decayed_primary_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]):
                            numerator_list_13_18.append(x.decayed_primary_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]):
                            numerator_list_19_60.append(x.decayed_primary_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60):
                            numerator_list_gte61.append(x.decayed_primary_teeth_number)
    
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_6),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_12),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_15),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_lte12),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_13_18),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_19_60),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_list_gte61),1))
                except:
                    total_decayed_primary_teeth.append(0)
                
                total_decayed_primary_teeth.append(sum(total_decayed_primary_teeth[1:]))
                

                # Number of decayed permanent teeth
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6):
                            numerator_list_6.append(x.decayed_permanent_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12):
                            numerator_list_12.append(x.decayed_permanent_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15):
                            numerator_list_15.append(x.decayed_permanent_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13):
                            numerator_list_lte12.append(x.decayed_permanent_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]):
                            numerator_list_13_18.append(x.decayed_permanent_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]):
                            numerator_list_19_60.append(x.decayed_permanent_teeth_number)
                        for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60):
                            numerator_list_gte61.append(x.decayed_permanent_teeth_number)
    
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_6),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_12),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_15),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_lte12),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_13_18),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_19_60),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_list_gte61),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                
                total_decayed_permanent_teeth.append(sum(total_decayed_permanent_teeth[1:]))
                

                # Cavity permanent molar or premolar
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_cavity_permanent_molar.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_molar.append(0)

                total_cavity_permanent_molar.append(sum(total_cavity_permanent_molar[1:]))


                # Cavity permanent anterior
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_cavity_permanent_anterior.append((numerator/denominator)*100)
                except:
                    total_cavity_permanent_anterior.append(0)

                total_cavity_permanent_anterior.append(sum(total_cavity_permanent_anterior[1:]))


                # Active Infection
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_active_infection.append((numerator/denominator)*100)
                except:
                    total_active_infection.append(0)

                total_active_infection.append(sum(total_active_infection[1:]))

                
                # Mouth pain due to reversible pulpitis
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_reversible_pulpitis.append((numerator/denominator)*100)
                except:
                    total_reversible_pulpitis.append(0)

                total_reversible_pulpitis.append(sum(total_reversible_pulpitis[1:]))



                # Need ART filling
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_need_art_filling.append((numerator/denominator)*100)
                except:
                    total_need_art_filling.append(0)

                total_need_art_filling.append(sum(total_need_art_filling[1:]))


                # Need SDF
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_need_sdf.append((numerator/denominator)*100)
                except:
                    total_need_sdf.append(0)

                total_need_sdf.append(sum(total_need_sdf[1:]))


                # Need Extraction
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_need_extraction.append((numerator/denominator)*100)
                except:
                    total_need_extraction.append(0)

                total_need_extraction.append(sum(total_need_extraction[1:]))


                # Need fv
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_need_fv.append((numerator/denominator)*100)
                except:
                    total_need_fv.append(0)

                total_need_fv.append(sum(total_need_fv[1:]))


                # Need dentist or hygienist
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        numerator_list_6.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        denominator_list_6.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).count())
                        numerator_list_12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        denominator_list_12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).count())
                        numerator_list_15.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())
                        denominator_list_15.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).count())

                        numerator_list_lte12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        denominator_list_lte12.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).count())
                        numerator_list_13_18.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        denominator_list_13_18.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).count())
                        numerator_list_19_60.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        denominator_list_19_60.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).count())
                        numerator_list_gte61.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                        denominator_list_gte61.append(Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).count())
                
                numerator = sum(numerator_list_6)
                denominator = sum(denominator_list_6)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator = sum(numerator_list_12)
                denominator = sum(denominator_list_12)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator = sum(numerator_list_15)
                denominator = sum(denominator_list_15)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator = sum(numerator_list_lte12)
                denominator = sum(denominator_list_lte12)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator = sum(numerator_list_13_18)
                denominator = sum(denominator_list_13_18)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator = sum(numerator_list_19_60)
                denominator = sum(denominator_list_19_60)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator = sum(numerator_list_gte61)
                denominator = sum(denominator_list_gte61)
                try:
                    total_need_dentist_or_hygienist.append((numerator/denominator)*100)
                except:
                    total_need_dentist_or_hygienist.append(0)

                total_need_dentist_or_hygienist.append(sum(total_need_dentist_or_hygienist[1:]))

                
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

            total_cavity_permanent_posterior = Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
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
