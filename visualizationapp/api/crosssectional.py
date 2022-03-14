import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import filters
import os
from django.http import JsonResponse
from nepali.datetime import NepaliDate
from django.db.models import DurationField, F, ExpressionWrapper
import datetime
from django.db.models import Q
from visualizationapp.models import Visualization
import statistics
from scipy.stats import chi2_contingency
from scipy.stats import kruskal
from scipy.stats import chisquare
from scipy.stats import wilcoxon
import numpy

from patientapp.models import Patient
from userapp.models import User, CustomUser
from treatmentapp.models import Treatment
from encounterapp.models import Screeing,Encounter,Refer
from visualizationapp.serializers.visualization import SectionalVisualizationSerializer,TestCrosssectionVisualizationSerializer,\
OverViewVisualization

import logging
# Get an instance of a logger
from django.db.models import Count

logger = logging.getLogger(__name__)

today = NepaliDate()


today_date = datetime.date.today()
last_30_days = datetime.date.today() + datetime.timedelta(-30)

today_date_obj = str(NepaliDate.from_date(today_date))
last_30_days_obj = str(NepaliDate.from_date(last_30_days))



class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CrossSectionalVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TestCrosssectionVisualizationSerializer

    def get(self, request,format=None):
        if User.objects.filter(id=request.user.id).exists():
            carries_risk = ["Carries Risk"]
            total_carries_risk_low = []
            total_carries_risk_medium = []
            total_carries_risk_high = []
            total_untreated_caries_present = []
            total_decayed_permanent_teeth = []
            total_decayed_primary_teeth = []
            total_cavity_permanent_molar = []
            total_cavity_permanent_anterior = []
            total_active_infection = []
            total_reversible_pulpitis = []
            total_need_art_filling = []
            total_need_sdf = []
            total_need_extraction = []
            total_need_fv = []
            total_need_dentist_or_hygienist = []

            # carries risk low
            # WHO indicator age-groups
            # Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")
            numerator_carries_risk_low_A = Visualization.objects.filter(carries_risk="Low",age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_A/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)

            numerator_carries_risk_low_B = Visualization.objects.filter(carries_risk="Low",age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_B/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)
            
            numerator_carries_risk_low_C = Visualization.objects.filter(carries_risk="Low",age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_C/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)
            
            carries_risk_low_ABC = [numerator_carries_risk_low_A,numerator_carries_risk_low_B,numerator_carries_risk_low_C]
            
            # Jevaia's indicator age groups
            numerator_carries_risk_low_E = Visualization.objects.filter(carries_risk="Low",age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_E/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)
            
            numerator_carries_risk_low_F = Visualization.objects.filter(carries_risk="Low",age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_F/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)
            
            numerator_carries_risk_low_G = Visualization.objects.filter(carries_risk="Low",age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_G/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)

            numerator_carries_risk_low_H = Visualization.objects.filter(carries_risk="Low",age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_H/denominator)*100,1))
            except:
                total_carries_risk_low.append(0)

            carries_risk_low_EFGH = [numerator_carries_risk_low_E,numerator_carries_risk_low_F,numerator_carries_risk_low_G,numerator_carries_risk_low_H]
            
            # carries risk medium
            # WHO indicator age-groups
            numerator_carries_risk_medium_A = Visualization.objects.filter(carries_risk="Medium",age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_A/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)

            numerator_carries_risk_medium_B = Visualization.objects.filter(carries_risk="Medium",age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_B/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)
            
            numerator_carries_risk_medium_C = Visualization.objects.filter(carries_risk="Medium",age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_C/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)
            
            carries_risk_medium_ABC = [numerator_carries_risk_medium_A,numerator_carries_risk_medium_B,numerator_carries_risk_medium_C]
            
            # Jevaia's indicator age groups
            numerator_carries_risk_medium_E = Visualization.objects.filter(carries_risk="Medium",age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_E/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)
            
            numerator_carries_risk_medium_F = Visualization.objects.filter(carries_risk="Medium",age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_F/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)
            
            numerator_carries_risk_medium_G = Visualization.objects.filter(carries_risk="Medium",age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_G/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)

            numerator_carries_risk_medium_H = Visualization.objects.filter(carries_risk="Medium",age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_H/denominator)*100,1))
            except:
                total_carries_risk_medium.append(0)

            carries_risk_medium_EFGH = [numerator_carries_risk_medium_E,numerator_carries_risk_medium_F,numerator_carries_risk_medium_G,numerator_carries_risk_medium_H]

            # carries risk high
            # WHO indicator age-groups
            numerator_carries_risk_high_A = Visualization.objects.filter(carries_risk="High",age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_A/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)

            numerator_carries_risk_high_B = Visualization.objects.filter(carries_risk="High",age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_B/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)
            
            numerator_carries_risk_high_C = Visualization.objects.filter(carries_risk="High",age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_C/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)
            
            carries_risk_high_ABC = [numerator_carries_risk_high_A,numerator_carries_risk_high_B,numerator_carries_risk_high_C]
            
            # Jevaia's indicator age groups
            numerator_carries_risk_high_E = Visualization.objects.filter(carries_risk="High",age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_E/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)
            
            numerator_carries_risk_high_F = Visualization.objects.filter(carries_risk="High",age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_F/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)
            
            numerator_carries_risk_high_G = Visualization.objects.filter(carries_risk="High",age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_G/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)

            numerator_carries_risk_high_H = Visualization.objects.filter(carries_risk="High",age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_H/denominator)*100,1))
            except:
                total_carries_risk_high.append(0)

            carries_risk_high_EFGH = [numerator_carries_risk_high_E,numerator_carries_risk_high_F,numerator_carries_risk_high_G,numerator_carries_risk_high_H]

            # p-value calculation for ABC
            # WHO Indicator age-groups
            try:
                table_ABC1 = [carries_risk_low_ABC,carries_risk_medium_ABC,carries_risk_high_ABC]
                stat, p, dof, expected = chi2_contingency(table_ABC1)
                if numpy.isnan(p):
                    abc1_pvalue = "nan" 
                else:
                    abc1_pvalue = round(p,3)
            except:
                abc1_pvalue = 0
            total_carries_risk_low.insert(3, abc1_pvalue)
            total_carries_risk_medium.insert(3, abc1_pvalue)
            total_carries_risk_high.insert(3, abc1_pvalue)

            # p-value calculation for EFGH
            # Jevaia’s indicator age-groups
            try:
                table_EFGH1 = [carries_risk_low_EFGH,carries_risk_medium_EFGH,carries_risk_high_EFGH]
                stat, p, dof, expected = chi2_contingency(table_EFGH1)
                if numpy.isnan(p):
                    efgh1_pvalue = "nan" 
                else:
                    efgh1_pvalue = round(p,3)
            except:
                efgh1_pvalue = 0
                
            total_carries_risk_low.append(efgh1_pvalue)
            total_carries_risk_medium.append(efgh1_pvalue)
            total_carries_risk_high.append(efgh1_pvalue)

            denominator_total = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            numerator_carries_risk_low_total = Visualization.objects.filter(carries_risk="Low",created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_low.append(round((numerator_carries_risk_low_total/denominator_total)*100,1))
            except:
                total_carries_risk_low.append(0)

            numerator_carries_risk_medium_total = Visualization.objects.filter(carries_risk="Medium",created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_medium.append(round((numerator_carries_risk_medium_total/denominator_total)*100,1))
            except:
                total_carries_risk_medium.append(0)

            numerator_carries_risk_high_total = Visualization.objects.filter(carries_risk="High",created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_carries_risk_high.append(round((numerator_carries_risk_high_total/denominator_total)*100,1))
            except:
                total_carries_risk_high.append(0)

            final_total_carries_risk_low = [
                'Low',
                str(numerator_carries_risk_low_A ) + "(" + str(total_carries_risk_low[0]) + "%)",
                str(numerator_carries_risk_low_B) + "(" + str(total_carries_risk_low[1]) + "%)",
                str(numerator_carries_risk_low_C) + "(" + str(total_carries_risk_low[2]) + "%)",
                total_carries_risk_low[3],
                str(numerator_carries_risk_low_E) + "(" + str(total_carries_risk_low[4]) + "%)",
                str(numerator_carries_risk_low_F) + "(" + str(total_carries_risk_low[5]) + "%)",
                str(numerator_carries_risk_low_G) + "(" + str(total_carries_risk_low[6]) + "%)",
                str(numerator_carries_risk_low_H) + "(" + str(total_carries_risk_low[7]) + "%)",
                total_carries_risk_low[8],
                str(numerator_carries_risk_low_total) + "(" + str(total_carries_risk_low[9]) + "%)",
                ]
            
            final_total_carries_risk_medium = [
                'Medium',
                str(numerator_carries_risk_medium_A) + "(" + str(total_carries_risk_medium[0]) + "%)",
                str(numerator_carries_risk_medium_B) + "(" + str(total_carries_risk_medium[1]) + "%)",
                str(numerator_carries_risk_medium_C) + "(" + str(total_carries_risk_medium[2]) + "%)",
                total_carries_risk_medium[3],
                str(numerator_carries_risk_medium_E) + "(" + str(total_carries_risk_medium[4]) + "%)",
                str(numerator_carries_risk_medium_F) + "(" + str(total_carries_risk_medium[5]) + "%)",
                str(numerator_carries_risk_medium_G) + "(" + str(total_carries_risk_medium[6]) + "%)",
                str(numerator_carries_risk_medium_H) + "(" + str(total_carries_risk_medium[7]) + "%)",
                total_carries_risk_medium[8],
                str(numerator_carries_risk_medium_total) + "(" + str(total_carries_risk_medium[9]) + "%)",
                ]
            
            final_total_carries_risk_high = [
                'High' ,
                str(numerator_carries_risk_high_A) + "(" + str(total_carries_risk_high[0]) + "%)",
                str(numerator_carries_risk_high_B) + "(" + str(total_carries_risk_high[1]) + "%)",
                str(numerator_carries_risk_high_C) + "(" + str(total_carries_risk_high[2]) + "%)",
                total_carries_risk_high[3],
                str(numerator_carries_risk_high_E) + "(" + str(total_carries_risk_high[4]) + "%)",
                str(numerator_carries_risk_high_F) + "(" + str(total_carries_risk_high[5]) + "%)",
                str(numerator_carries_risk_high_G) + "(" + str(total_carries_risk_high[6]) + "%)",
                str(numerator_carries_risk_high_H) + "(" + str(total_carries_risk_high[7]) + "%)",
                total_carries_risk_high[8],
                str(numerator_carries_risk_high_total) + "(" + str(total_carries_risk_high[9]) + "%)",
                ]

            # Any untreated caries present
            # WHO indicator age-groups
            numerator_untreated_caries_present_A = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_A/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)

            numerator_untreated_caries_present_B = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_B/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)
            
            numerator_untreated_caries_present_C = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_C/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)
            
            untreated_caries_present_ABC = [numerator_untreated_caries_present_A,numerator_untreated_caries_present_B,numerator_untreated_caries_present_C]
            
            # Jevaia's indicator age groups
            numerator_untreated_caries_present_E = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_E/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)
            
            numerator_untreated_caries_present_F = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_F/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)
            
            numerator_untreated_caries_present_G = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_G/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)
            numerator_untreated_caries_present_H = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_H/denominator)*100,1))
            except:
                total_untreated_caries_present.append(0)

            untreated_caries_present_EFGH = [numerator_untreated_caries_present_E,numerator_untreated_caries_present_F,numerator_untreated_caries_present_G,numerator_untreated_caries_present_H]

            # Number of decayed primary teeth
            # WHO indicator age-groups
            decayed_primary_teeth_mean_list_ABC = []
            decayed_primary_teeth_mean_list_EFGH = []
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=6).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=6,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_ABC.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_ABC.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=12).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=12,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_ABC.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_ABC.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=15).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=15,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_ABC.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_ABC.append(0)
            
            # Jevaia's indicator age groups
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__lt=13).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__lt=13,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_EFGH.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[13,18]).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[13,18],patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_EFGH.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[19,60]).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[19,60],patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_EFGH.append(0)
            
            decayed_primary_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__gt=60).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__gt=60,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_primary_teeth1.append(a.decayed_primary_teeth_number)
            try:
                total_decayed_primary_teeth.append(round(statistics.stdev(decayed_primary_teeth1),1))
                decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_primary_teeth1),1))
            except:
                total_decayed_primary_teeth.append(0)
                decayed_primary_teeth_mean_list_EFGH.append(0)
            
            # Number of decayed permanent teeth
            # WHO indicator age-groups
            decayed_permanent_teeth_mean_list_ABC = []
            decayed_permanent_teeth_mean_list_EFGH = []
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=6).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=6,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_ABC.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_ABC.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=12).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=12,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_ABC.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_ABC.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=15).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age=15,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_ABC.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_ABC.append(0)
            
            # Jevaia's indicator age groups
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__lt=13).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__lt=13,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_EFGH.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[13,18]).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[13,18],patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_EFGH.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[19,60]).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__range=[19,60],patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_EFGH.append(0)
            
            decayed_permanent_teeth1 = []
            for i in Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__gt=60).values('patiend_id').distinct():
                a = Visualization.objects.filter(created_at__range=[last_30_days_obj, today_date_obj],age__gt=60,patiend_id=i["patiend_id"]).order_by('-created_at').first()
                decayed_permanent_teeth1.append(a.decayed_permanent_teeth_number)
            try:
                total_decayed_permanent_teeth.append(round(statistics.stdev(decayed_permanent_teeth1),1))
                decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(decayed_permanent_teeth1),1))
            except:
                total_decayed_permanent_teeth.append(0)
                decayed_permanent_teeth_mean_list_EFGH.append(0)

            # p-value calculation for ABC
            try:
                stat, p = wilcoxon(decayed_primary_teeth_mean_list_ABC,decayed_permanent_teeth_mean_list_ABC)
                abc_pvalue = round(p,3)
            except:
                abc_pvalue = 0
            
            total_decayed_primary_teeth.insert(3, abc_pvalue)
            total_decayed_permanent_teeth.insert(3, abc_pvalue)

            # p-value calculation for EFGH
            try:
                stat, p = wilcoxon(decayed_primary_teeth_mean_list_EFGH,decayed_permanent_teeth_mean_list_EFGH)
                efgh_pvalue = round(p,3)
            except:
                efgh_pvalue = 0
            
            total_decayed_primary_teeth.append(efgh_pvalue)
            total_decayed_permanent_teeth.append(efgh_pvalue)

            overall_decayed_primary_teeth = decayed_primary_teeth_mean_list_ABC[0] + decayed_primary_teeth_mean_list_ABC[1] 
            + decayed_primary_teeth_mean_list_ABC[2] + decayed_primary_teeth_mean_list_EFGH[0]
            + decayed_primary_teeth_mean_list_EFGH[1] + decayed_primary_teeth_mean_list_EFGH[2]
            + decayed_primary_teeth_mean_list_EFGH[3]

            mean_overall_decayed_primary_teeth = round(overall_decayed_primary_teeth / 7,2)

            overall_decayed_permanent_teeth = decayed_permanent_teeth_mean_list_ABC[0] + decayed_permanent_teeth_mean_list_ABC[1] 
            + decayed_permanent_teeth_mean_list_ABC[2] + decayed_permanent_teeth_mean_list_EFGH[0]
            + decayed_permanent_teeth_mean_list_EFGH[1] + decayed_permanent_teeth_mean_list_EFGH[2]
            + decayed_permanent_teeth_mean_list_EFGH[3]

            mean_overall_decayed_permanent_teeth = round(overall_decayed_permanent_teeth / 7,2)

            final_total_decayed_primary_teeth = [
                "Number of decayed primary teeth",
                str(decayed_primary_teeth_mean_list_ABC[0]) + "(" + "SD" + str(total_decayed_primary_teeth[0]) + ")",
                str(decayed_primary_teeth_mean_list_ABC[1]) + "(" + "SD" + str(total_decayed_primary_teeth[1]) + ")",
                str(decayed_primary_teeth_mean_list_ABC[2]) + "(" + "SD" + str(total_decayed_primary_teeth[2]) + ")",
                total_decayed_primary_teeth[3],
                str(decayed_primary_teeth_mean_list_EFGH[0]) + "(" + "SD" + str(total_decayed_primary_teeth[4]) + ")",
                str(decayed_primary_teeth_mean_list_EFGH[1]) + "(" + "SD" + str(total_decayed_primary_teeth[5]) + ")",
                str(decayed_primary_teeth_mean_list_EFGH[2]) + "(" + "SD" + str(total_decayed_primary_teeth[6]) + ")",
                str(decayed_primary_teeth_mean_list_EFGH[3]) + "(" + "SD" + str(total_decayed_primary_teeth[7]) + ")",
                total_decayed_primary_teeth[8],
                mean_overall_decayed_primary_teeth,
                ]
            
            final_total_decayed_permanent_teeth = [
                "Number of decayed permanent teeth",
                str(decayed_permanent_teeth_mean_list_ABC[0]) + "(" + "SD" + str(total_decayed_permanent_teeth[0]) + ")",
                str(decayed_permanent_teeth_mean_list_ABC[1]) + "(" + "SD" + str(total_decayed_permanent_teeth[1]) + ")",
                str(decayed_permanent_teeth_mean_list_ABC[2]) + "(" + "SD" + str(total_decayed_permanent_teeth[2]) + ")",
                total_decayed_permanent_teeth[3],
                str(decayed_permanent_teeth_mean_list_EFGH[0]) + "(" + "SD" + str(total_decayed_permanent_teeth[4]) + ")",
                str(decayed_permanent_teeth_mean_list_EFGH[1]) + "(" + "SD" + str(total_decayed_permanent_teeth[5]) + ")",
                str(decayed_permanent_teeth_mean_list_EFGH[2]) + "(" + "SD" + str(total_decayed_permanent_teeth[6]) + ")",
                str(decayed_permanent_teeth_mean_list_EFGH[3]) + "(" + "SD" + str(total_decayed_permanent_teeth[7]) + ")",
                total_decayed_permanent_teeth[8],
                mean_overall_decayed_permanent_teeth,
                ]
            
            # Cavity permanent molar or premolar
            # WHO indicator age-groups
            numerator_cavity_permanent_molar_A = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_A/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)

            numerator_cavity_permanent_molar_B = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_B/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)
            
            numerator_cavity_permanent_molar_C = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_C/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)
            
            cavity_permanent_molar_ABC = [numerator_cavity_permanent_molar_A,numerator_cavity_permanent_molar_B,numerator_cavity_permanent_molar_C]
            
            # Jevaia's indicator age groups
            numerator_cavity_permanent_molar_E = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_E/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)
            
            numerator_cavity_permanent_molar_F = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_F/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)
            
            numerator_cavity_permanent_molar_G = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_G/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)
            numerator_cavity_permanent_molar_H = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_H/denominator)*100,1))
            except:
                total_cavity_permanent_molar.append(0)

            cavity_permanent_molar_EFGH = [numerator_cavity_permanent_molar_E,numerator_cavity_permanent_molar_F,numerator_cavity_permanent_molar_G,numerator_cavity_permanent_molar_H]


            # Cavity permanent anterior
            # WHO indicator age-groups
            numerator_cavity_permanent_anterior_A = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_A/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)

            numerator_cavity_permanent_anterior_B = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_B/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)
            
            numerator_cavity_permanent_anterior_C = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_C/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)
            
            cavity_permanent_anterior_ABC = [numerator_cavity_permanent_anterior_A,numerator_cavity_permanent_anterior_B,numerator_cavity_permanent_anterior_C]
            
            # Jevaia's indicator age groups
            numerator_cavity_permanent_anterior_E = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_E/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)
            
            numerator_cavity_permanent_anterior_F = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_F/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)
            
            numerator_cavity_permanent_anterior_G = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_G/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)
            numerator_cavity_permanent_anterior_H = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_H/denominator)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)

            cavity_permanent_anterior_EFGH = [numerator_cavity_permanent_anterior_E,numerator_cavity_permanent_anterior_F,numerator_cavity_permanent_anterior_G,numerator_cavity_permanent_anterior_H]


            # Active Infection
            # WHO indicator age-groups
            numerator_active_infection_A = Visualization.objects.filter(active_infection=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_A/denominator)*100,1))
            except:
                total_active_infection.append(0)

            numerator_active_infection_B = Visualization.objects.filter(active_infection=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_B/denominator)*100,1))
            except:
                total_active_infection.append(0)
            
            numerator_active_infection_C = Visualization.objects.filter(active_infection=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_C/denominator)*100,1))
            except:
                total_active_infection.append(0)
            
            active_infection_ABC = [numerator_active_infection_A,numerator_active_infection_A,numerator_active_infection_A]
            
            # Jevaia's indicator age groups
            numerator_active_infection_E = Visualization.objects.filter(active_infection=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_E/denominator)*100,1))
            except:
                total_active_infection.append(0)
            
            numerator_active_infection_F = Visualization.objects.filter(active_infection=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_F/denominator)*100,1))
            except:
                total_active_infection.append(0)
            
            numerator_active_infection_G = Visualization.objects.filter(active_infection=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_G/denominator)*100,1))
            except:
                total_active_infection.append(0)
            numerator_active_infection_H = Visualization.objects.filter(active_infection=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_H/denominator)*100,1))
            except:
                total_active_infection.append(0)

            active_infection_EFGH = [numerator_active_infection_E,numerator_active_infection_F,numerator_active_infection_G,numerator_active_infection_H]

            # Mouth pain due to reversible pulpitis
            # WHO indicator age-groups
            numerator_reversible_pulpitis_A = Visualization.objects.filter(reversible_pulpitis=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_A/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)

            numerator_reversible_pulpitis_B = Visualization.objects.filter(reversible_pulpitis=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_B/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)
            
            numerator_reversible_pulpitis_C = Visualization.objects.filter(reversible_pulpitis=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_C/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)
            
            reversible_pulpitis_ABC = [numerator_reversible_pulpitis_A,numerator_reversible_pulpitis_B,numerator_reversible_pulpitis_C]
            
            # Jevaia's indicator age groups
            numerator_reversible_pulpitis_E = Visualization.objects.filter(reversible_pulpitis=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_E/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)
            
            numerator_reversible_pulpitis_F = Visualization.objects.filter(reversible_pulpitis=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_F/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)
            
            numerator_reversible_pulpitis_G = Visualization.objects.filter(reversible_pulpitis=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_G/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)
            numerator_reversible_pulpitis_H = Visualization.objects.filter(reversible_pulpitis=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_H/denominator)*100,1))
            except:
                total_reversible_pulpitis.append(0)

            reversible_pulpitis_EFGH = [numerator_reversible_pulpitis_E,numerator_reversible_pulpitis_F,numerator_reversible_pulpitis_G,numerator_reversible_pulpitis_H]

            # Need ART filling
            # WHO indicator age-groups
            numerator_need_art_filling_A = Visualization.objects.filter(need_art_filling=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_A/denominator)*100,1))
            except:
                total_need_art_filling.append(0)

            numerator_need_art_filling_B = Visualization.objects.filter(need_art_filling=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_B/denominator)*100,1))
            except:
                total_need_art_filling.append(0)
            
            numerator_need_art_filling_C = Visualization.objects.filter(need_art_filling=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_C/denominator)*100,1))
            except:
                total_need_art_filling.append(0)
            
            need_art_filling_ABC = [numerator_need_art_filling_A,numerator_need_art_filling_B,numerator_need_art_filling_C]
            
            # Jevaia's indicator age groups
            numerator_need_art_filling_E = Visualization.objects.filter(need_art_filling=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_E/denominator)*100,1))
            except:
                total_need_art_filling.append(0)
            
            numerator_need_art_filling_F = Visualization.objects.filter(need_art_filling=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_F/denominator)*100,1))
            except:
                total_need_art_filling.append(0)
            
            numerator_need_art_filling_G = Visualization.objects.filter(need_art_filling=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_G/denominator)*100,1))
            except:
                total_need_art_filling.append(0)
            numerator_need_art_filling_H = Visualization.objects.filter(need_art_filling=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_H/denominator)*100,1))
            except:
                total_need_art_filling.append(0)

            need_art_filling_EFGH = [numerator_need_art_filling_E,numerator_need_art_filling_F,numerator_need_art_filling_G,numerator_need_art_filling_H]

            # Need SDF
            # WHO indicator age-groups
            numerator_need_sdf_A = Visualization.objects.filter(need_sdf=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_A/denominator)*100,1))
            except:
                total_need_sdf.append(0)

            numerator_need_sdf_B = Visualization.objects.filter(need_sdf=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_B/denominator)*100,1))
            except:
                total_need_sdf.append(0)
            
            numerator_need_sdf_C = Visualization.objects.filter(need_sdf=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_C/denominator)*100,1))
            except:
                total_need_sdf.append(0)
            
            need_sdf_ABC = [numerator_need_sdf_A,numerator_need_sdf_B,numerator_need_sdf_C]
            
            # Jevaia's indicator age groups
            numerator_need_sdf_E = Visualization.objects.filter(need_sdf=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_E/denominator)*100,1))
            except:
                total_need_sdf.append(0)
            
            numerator_need_sdf_F = Visualization.objects.filter(need_sdf=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_F/denominator)*100,1))
            except:
                total_need_sdf.append(0)
            
            numerator_need_sdf_G = Visualization.objects.filter(need_sdf=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_G/denominator)*100,1))
            except:
                total_need_sdf.append(0)
            numerator_need_sdf_H = Visualization.objects.filter(need_sdf=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_H/denominator)*100,1))
            except:
                total_need_sdf.append(0)

            need_sdf_EFGH = [numerator_need_sdf_E,numerator_need_sdf_F,numerator_need_sdf_G,numerator_need_sdf_H]


            # Need Extraction
            # WHO indicator age-groups
            numerator_need_extraction_A = Visualization.objects.filter(need_extraction=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_A/denominator)*100,1))
            except:
                total_need_extraction.append(0)

            numerator_need_extraction_B = Visualization.objects.filter(need_extraction=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_B/denominator)*100,1))
            except:
                total_need_extraction.append(0)
            
            numerator_need_extraction_C = Visualization.objects.filter(need_extraction=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_C/denominator)*100,1))
            except:
                total_need_extraction.append(0)

            need_extraction_ABC = [numerator_need_extraction_A,numerator_need_extraction_B,numerator_need_extraction_C]

            
            # Jevaia's indicator age groups
            numerator_need_extraction_E = Visualization.objects.filter(need_extraction=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_E/denominator)*100,1))
            except:
                total_need_extraction.append(0)
            
            numerator_need_extraction_F = Visualization.objects.filter(need_extraction=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_F/denominator)*100,1))
            except:
                total_need_extraction.append(0)
            
            numerator_need_extraction_G = Visualization.objects.filter(need_extraction=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_G/denominator)*100,1))
            except:
                total_need_extraction.append(0)
            numerator_need_extraction_H = Visualization.objects.filter(need_extraction=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_H/denominator)*100,1))
            except:
                total_need_extraction.append(0)

            need_extraction_EFGH = [numerator_need_extraction_E,numerator_need_extraction_F,numerator_need_extraction_G,numerator_need_extraction_H]

            # Need FV
            # WHO indicator age-groups
            numerator_need_fv_A = Visualization.objects.filter(need_fv=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_A/denominator)*100,1))
            except:
                total_need_fv.append(0)

            numerator_need_fv_B = Visualization.objects.filter(need_fv=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_B/denominator)*100,1))
            except:
                total_need_fv.append(0)
            
            numerator_need_fv_C = Visualization.objects.filter(need_fv=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_C/denominator)*100,1))
            except:
                total_need_fv.append(0)
            
            need_fv_ABC = [numerator_need_fv_A,numerator_need_fv_B,numerator_need_fv_C]
            
            # Jevaia's indicator age groups
            numerator_need_fv_E = Visualization.objects.filter(need_fv=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_E/denominator)*100,1))
            except:
                total_need_fv.append(0)
            
            numerator_need_fv_F = Visualization.objects.filter(need_fv=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_F/denominator)*100,1))
            except:
                total_need_fv.append(0)
            
            numerator_need_fv_G = Visualization.objects.filter(need_fv=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_G/denominator)*100,1))
            except:
                total_need_fv.append(0)
            numerator_need_fv_H = Visualization.objects.filter(need_fv=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_H/denominator)*100,1))
            except:
                total_need_fv.append(0)

            need_fv_EFGH = [numerator_need_fv_E,numerator_need_fv_F,numerator_need_fv_G,numerator_need_fv_H]
            

            # Need Dentist or Hygenist
            # WHO indicator age-groups
            numerator_need_dentist_or_hygienist_A = Visualization.objects.filter(need_dentist_or_hygienist=True,age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=6,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_A/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)

            numerator_need_dentist_or_hygienist_B = Visualization.objects.filter(need_dentist_or_hygienist=True,age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=12,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_B/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)
            
            numerator_need_dentist_or_hygienist_C = Visualization.objects.filter(need_dentist_or_hygienist=True,age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age=15,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_C/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)
            
            need_dentist_or_hygienist_ABC = [numerator_need_dentist_or_hygienist_A,numerator_need_dentist_or_hygienist_B,numerator_need_dentist_or_hygienist_C]
            
            # Jevaia's indicator age groups
            numerator_need_dentist_or_hygienist_E = Visualization.objects.filter(need_dentist_or_hygienist=True,age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__lt=13,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_E/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)
            
            numerator_need_dentist_or_hygienist_F = Visualization.objects.filter(need_dentist_or_hygienist=True,age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[13,18],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_F/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)
            
            numerator_need_dentist_or_hygienist_G = Visualization.objects.filter(need_dentist_or_hygienist=True,age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__range=[19,60],created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_G/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)
            numerator_need_dentist_or_hygienist_H = Visualization.objects.filter(need_dentist_or_hygienist=True,age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            denominator = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(age__gt=60,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_H/denominator)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)

            need_dentist_or_hygienist_EFGH = [numerator_need_dentist_or_hygienist_E,numerator_need_dentist_or_hygienist_F,numerator_need_dentist_or_hygienist_G,numerator_need_dentist_or_hygienist_H]

            # p-value calculation for ABCD2
            # WHO Indicator age-groups
            try:
                table_ABC2 = [untreated_caries_present_ABC,cavity_permanent_molar_ABC,cavity_permanent_anterior_ABC,active_infection_ABC,reversible_pulpitis_ABC,need_art_filling_ABC,need_sdf_ABC,need_extraction_ABC,need_fv_ABC,need_dentist_or_hygienist_ABC]
                stat, p, dof, expected = chi2_contingency(table_ABC2)
                if numpy.isnan(p):
                    abc2_pvalue = "nan" 
                else:
                    abc2_pvalue = round(p,3)
            except:
                abc2_pvalue = 0

            total_untreated_caries_present.insert(3, abc2_pvalue)
            total_cavity_permanent_molar.insert(3, abc2_pvalue)
            total_cavity_permanent_anterior.insert(3, abc2_pvalue)
            total_active_infection.insert(3, abc2_pvalue)
            total_reversible_pulpitis.insert(3, abc2_pvalue)
            total_need_art_filling.insert(3, abc2_pvalue)
            total_need_sdf.insert(3, abc2_pvalue)
            total_need_extraction.insert(3, abc2_pvalue)
            total_need_fv.insert(3, abc2_pvalue)
            total_need_dentist_or_hygienist.insert(3, abc2_pvalue)

            # p-value calculation for EFGH2
            # Jevaia’s indicator age-groups
            try:
                table_EFGH2 = [untreated_caries_present_EFGH,cavity_permanent_molar_EFGH,cavity_permanent_anterior_EFGH,active_infection_EFGH,reversible_pulpitis_EFGH,need_art_filling_EFGH,need_sdf_EFGH,need_extraction_EFGH,need_fv_EFGH,need_dentist_or_hygienist_EFGH]
                stat, p, dof, expected = chi2_contingency(table_EFGH2)
                if numpy.isnan(p):
                    efgh2_pvalue = "nan" 
                else:
                    efgh2_pvalue = round(p,3)
            except:
                efgh2_pvalue = 0

            total_untreated_caries_present.append(efgh2_pvalue)
            total_cavity_permanent_molar.append(efgh2_pvalue)
            total_cavity_permanent_anterior.append(efgh2_pvalue)
            total_active_infection.append(efgh2_pvalue)
            total_reversible_pulpitis.append(efgh2_pvalue)
            total_need_art_filling.append(efgh2_pvalue)
            total_need_sdf.append(efgh2_pvalue)
            total_need_extraction.append(efgh2_pvalue)
            total_need_fv.append(efgh2_pvalue)
            total_need_dentist_or_hygienist.append(efgh2_pvalue)

            denominator_total = Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            numerator_untreated_caries_present_total = Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_untreated_caries_present.append(round((numerator_untreated_caries_present_total/denominator_total)*100,1))
            except:
                total_untreated_caries_present.append(0)

            numerator_cavity_permanent_molar_total = Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_total/denominator_total)*100,1))
            except:
                total_cavity_permanent_molar.append(0)

            numerator_cavity_permanent_anterior_total = Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_total/denominator_total)*100,1))
            except:
                total_cavity_permanent_anterior.append(0)

            numerator_active_infection_total = Visualization.objects.filter(active_infection=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_active_infection.append(round((numerator_active_infection_total/denominator_total)*100,1))
            except:
                total_active_infection.append(0)

            numerator_reversible_pulpitis_total = Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_total/denominator_total)*100,1))
            except:
                total_reversible_pulpitis.append(0)

            numerator_need_art_filling_total = Visualization.objects.filter(need_art_filling=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_art_filling.append(round((numerator_need_art_filling_total/denominator_total)*100,1))
            except:
                total_need_art_filling.append(0)

            numerator_need_sdf_total = Visualization.objects.filter(need_sdf=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_sdf.append(round((numerator_need_sdf_total/denominator_total)*100,1))
            except:
                total_need_sdf.append(0)

            numerator_need_extraction_total = Visualization.objects.filter(need_extraction=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_extraction.append(round((numerator_need_extraction_total/denominator_total)*100,1))
            except:
                total_need_extraction.append(0)

            numerator_need_fv_total = Visualization.objects.filter(need_fv=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_fv.append(round((numerator_need_fv_total/denominator_total)*100,1))
            except:
                total_need_fv.append(0)

            numerator_need_dentist_or_hygienist_total = Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[last_30_days_obj, today_date_obj]).values('patiend_id').distinct().count()
            try:
                total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_total/denominator_total)*100,1))
            except:
                total_need_dentist_or_hygienist.append(0)

            final_total_untreated_caries_present = [
                "Any untreated caries present" ,
                str(numerator_untreated_caries_present_A) + "(" + str(total_untreated_caries_present[0]) + "%)",
                str(numerator_untreated_caries_present_B) + "(" + str(total_untreated_caries_present[1]) + "%)",
                str(numerator_untreated_caries_present_C) + "(" + str(total_untreated_caries_present[2]) + "%)",
                total_untreated_caries_present[3],
                str(numerator_untreated_caries_present_E) + "(" + str(total_untreated_caries_present[4]) + "%)",
                str(numerator_untreated_caries_present_F) + "(" + str(total_untreated_caries_present[5]) + "%)",
                str(numerator_untreated_caries_present_G) + "(" + str(total_untreated_caries_present[6]) + "%)",
                str(numerator_untreated_caries_present_H) + "(" + str(total_untreated_caries_present[7]) + "%)",
                total_untreated_caries_present[8],
                str(numerator_untreated_caries_present_total) + "(" + str(total_untreated_caries_present[9]) + "%)",
                ]
            
            final_total_cavity_permanent_molar = [
                "Cavity permanent molar or premolar" ,
                str(numerator_cavity_permanent_molar_A) + "(" + str(total_cavity_permanent_molar[0]) + "%)",
                str(numerator_cavity_permanent_molar_B) + "(" + str(total_cavity_permanent_molar[1]) + "%)",
                str(numerator_cavity_permanent_molar_C) + "(" + str(total_cavity_permanent_molar[2]) + "%)",
                total_cavity_permanent_molar[3],
                str(numerator_cavity_permanent_molar_E) + "(" + str(total_cavity_permanent_molar[4]) + "%)",
                str(numerator_cavity_permanent_molar_F) + "(" + str(total_cavity_permanent_molar[5]) + "%)",
                str(numerator_cavity_permanent_molar_G) + "(" + str(total_cavity_permanent_molar[6]) + "%)",
                str(numerator_cavity_permanent_molar_H) + "(" + str(total_cavity_permanent_molar[7]) + "%)",
                total_cavity_permanent_molar[8],
                str(numerator_cavity_permanent_molar_total) + "(" + str(total_cavity_permanent_molar[9]) + "%)",
                ]
            
            final_total_cavity_permanent_anterior = [
                "Cavity permanent anterior",
                str(numerator_cavity_permanent_anterior_A) + "(" + str(total_cavity_permanent_anterior[0]) + "%)",
                str(numerator_cavity_permanent_anterior_B) + "(" + str(total_cavity_permanent_anterior[1]) + "%)",
                str(numerator_cavity_permanent_anterior_C) + "(" + str(total_cavity_permanent_anterior[2]) + "%)",
                total_cavity_permanent_anterior[3],
                str(numerator_cavity_permanent_anterior_E) + "(" + str(total_cavity_permanent_anterior[4]) + "%)",
                str(numerator_cavity_permanent_anterior_F) + "(" + str(total_cavity_permanent_anterior[5]) + "%)",
                str(numerator_cavity_permanent_anterior_G) + "(" + str(total_cavity_permanent_anterior[6]) + "%)",
                str(numerator_cavity_permanent_anterior_H) + "(" + str(total_cavity_permanent_anterior[7]) + "%)",
                total_cavity_permanent_anterior[8],
                str(numerator_cavity_permanent_anterior_total) + "(" + str(total_cavity_permanent_anterior[9]) + "%)",
                ]
            
            final_total_active_infection = [
                "Active Infection" ,
                str(numerator_active_infection_A) + "(" + str(total_active_infection[0]) + "%)",
                str(numerator_active_infection_B) + "(" + str(total_active_infection[1]) + "%)",
                str(numerator_active_infection_C) + "(" + str(total_active_infection[2]) + "%)",
                total_active_infection[3],
                str(numerator_active_infection_E) + "(" + str(total_active_infection[4]) + "%)",
                str(numerator_active_infection_F) + "(" + str(total_active_infection[5]) + "%)",
                str(numerator_active_infection_G) + "(" + str(total_active_infection[6]) + "%)",
                str(numerator_active_infection_H) + "(" + str(total_active_infection[7]) + "%)",
                total_active_infection[8],
                str(numerator_active_infection_total) + "(" + str(total_active_infection[9]) + "%)",
                ]
            
            final_total_reversible_pulpitis = [
                "Mouth pain due to reversible pulpitis" ,
                str(numerator_reversible_pulpitis_A) + "(" + str(total_reversible_pulpitis[0]) + "%)",
                str(numerator_reversible_pulpitis_B) + "(" + str(total_reversible_pulpitis[1]) + "%)",
                str(numerator_reversible_pulpitis_C) + "(" + str(total_reversible_pulpitis[2]) + "%)",
                total_reversible_pulpitis[3],
                str(numerator_reversible_pulpitis_E) + "(" + str(total_reversible_pulpitis[4]) + "%)",
                str(numerator_reversible_pulpitis_F) + "(" + str(total_reversible_pulpitis[5]) + "%)",
                str(numerator_reversible_pulpitis_G) + "(" + str(total_reversible_pulpitis[6]) + "%)",
                str(numerator_reversible_pulpitis_H) + "(" + str(total_reversible_pulpitis[7]) + "%)",
                total_reversible_pulpitis[8],
                str(numerator_reversible_pulpitis_total) + "(" + str(total_reversible_pulpitis[9]) + "%)",
                ]
            
            final_total_need_art_filling = [
                "Need ART filling" ,
                str(numerator_need_art_filling_A) + "(" + str(total_need_art_filling[0]) + "%)",
                str(numerator_need_art_filling_B) + "(" + str(total_need_art_filling[1]) + "%)",
                str(numerator_need_art_filling_C) + "(" + str(total_need_art_filling[2]) + "%)",
                total_need_art_filling[3],
                str(numerator_need_art_filling_E) + "(" + str(total_need_art_filling[4]) + "%)",
                str(numerator_need_art_filling_F) + "(" + str(total_need_art_filling[5]) + "%)",
                str(numerator_need_art_filling_G) + "(" + str(total_need_art_filling[6]) + "%)",
                str(numerator_need_art_filling_H) + "(" + str(total_need_art_filling[7]) + "%)",
                total_need_art_filling[8],
                str(numerator_need_art_filling_total) + "(" + str(total_need_art_filling[9]) + "%)",
                ]

            final_total_need_sdf = [
                "Need SDF",
                str(numerator_need_sdf_A) + "(" + str(total_need_sdf[0]) + "%)",
                str(numerator_need_sdf_B) + "(" + str(total_need_sdf[1]) + "%)",
                str(numerator_need_sdf_C) + "(" + str(total_need_sdf[2]) + "%)",
                total_need_sdf[3],
                str(numerator_need_sdf_E) + "(" + str(total_need_sdf[4]) + "%)",
                str(numerator_need_sdf_F) + "(" + str(total_need_sdf[5]) + "%)",
                str(numerator_need_sdf_G) + "(" + str(total_need_sdf[6]) + "%)",
                str(numerator_need_sdf_H) + "(" + str(total_need_sdf[7]) + "%)",
                total_need_sdf[8],
                str(numerator_need_sdf_total) + "(" + str(total_need_sdf[9]) + "%)",
                ]
            
            final_total_need_extraction = [
                "Need Extraction",
                str(numerator_need_extraction_A) + "(" + str(total_need_extraction[0]) + "%)",
                str(numerator_need_extraction_B) + "(" + str(total_need_extraction[1]) + "%)",
                str(numerator_need_extraction_C) + "(" + str(total_need_extraction[2]) + "%)",
                total_need_extraction[3],
                str(numerator_need_extraction_E) + "(" + str(total_need_extraction[4]) + "%)",
                str(numerator_need_extraction_F) + "(" + str(total_need_extraction[5]) + "%)",
                str(numerator_need_extraction_G) + "(" + str(total_need_extraction[6]) + "%)",
                str(numerator_need_extraction_H) + "(" + str(total_need_extraction[7]) + "%)",
                total_need_extraction[8],
                str(numerator_need_extraction_total) + "(" + str(total_need_extraction[9]) + "%)",
                ]
            
            final_total_need_fv = [
                "Need FV",
                str(numerator_need_fv_A) + "(" + str(total_need_fv[0]) + "%)",
                str(numerator_need_fv_B) + "(" + str(total_need_fv[1]) + "%)",
                str(numerator_need_fv_C) + "(" + str(total_need_fv[2]) + "%)",
                total_need_fv[3],
                str(numerator_need_fv_E) + "(" + str(total_need_fv[4]) + "%)",
                str(numerator_need_fv_F) + "(" + str(total_need_fv[5]) + "%)",
                str(numerator_need_fv_G) + "(" + str(total_need_fv[6]) + "%)",
                str(numerator_need_fv_H) + "(" + str(total_need_fv[7]) + "%)",
                total_need_fv[8],
                str(numerator_need_fv_total) + "(" + str(total_need_fv[9]) + "%)",
                ]
            
            final_total_need_dentist_or_hygienist = [
                "Need Dentist or Hygenist",
                str(numerator_need_dentist_or_hygienist_A) + "(" + str(total_need_dentist_or_hygienist[0]) + "%)",
                str(numerator_need_dentist_or_hygienist_B) + "(" + str(total_need_dentist_or_hygienist[1]) + "%)",
                str(numerator_need_dentist_or_hygienist_C) + "(" + str(total_need_dentist_or_hygienist[2]) + "%)",
                total_need_dentist_or_hygienist[3],
                str(numerator_need_dentist_or_hygienist_E) + "(" + str(total_need_dentist_or_hygienist[4]) + "%)",
                str(numerator_need_dentist_or_hygienist_F) + "(" + str(total_need_dentist_or_hygienist[5]) + "%)",
                str(numerator_need_dentist_or_hygienist_G) + "(" + str(total_need_dentist_or_hygienist[6]) + "%)",
                str(numerator_need_dentist_or_hygienist_H) + "(" + str(total_need_dentist_or_hygienist[7]) + "%)",
                total_need_dentist_or_hygienist[8],
                str(numerator_need_dentist_or_hygienist_total) + "(" + str(total_need_dentist_or_hygienist[9]) + "%)",
                ]

            rowA_total = numerator_carries_risk_low_A + numerator_carries_risk_medium_A + numerator_carries_risk_high_A 
            
            rowB_total = numerator_carries_risk_low_B + numerator_carries_risk_medium_B + numerator_carries_risk_high_B 
            
            rowC_total = numerator_carries_risk_low_C + numerator_carries_risk_medium_C + numerator_carries_risk_high_C 

            rowE_total = numerator_carries_risk_low_E + numerator_carries_risk_medium_E + numerator_carries_risk_high_E 
            
            rowF_total = numerator_carries_risk_low_F + numerator_carries_risk_medium_F + numerator_carries_risk_high_F 
            
            rowG_total = numerator_carries_risk_low_G + numerator_carries_risk_medium_G + numerator_carries_risk_high_G 
            
            rowH_total = numerator_carries_risk_low_H + numerator_carries_risk_medium_H + numerator_carries_risk_high_H 
            
            grand_total = rowE_total + rowF_total + rowG_total + rowH_total
            try:
                rowA_total_percent = round((rowA_total / grand_total) * 100,1)
            except:
                rowA_total_percent = 0

            try:
                rowB_total_percent = round((rowB_total / grand_total) * 100,1)
            except:
                rowB_total_percent = 0
            
            try:
                rowC_total_percent = round((rowC_total / grand_total) * 100,1)
            except:
                rowC_total_percent = 0
            
            try:
                rowE_total_percent = round((rowE_total / grand_total) * 100,1)
            except:
                rowE_total_percent = 0
            
            try:
                rowF_total_percent = round((rowF_total / grand_total) * 100,1)
            except:
                rowF_total_percent = 0

            try:
                rowG_total_percent = round((rowG_total / grand_total) * 100,1)
            except:
                rowG_total_percent = 0
            
            try:
                rowH_total_percent = round((rowH_total / grand_total) * 100,1)
            except:
                rowH_total_percent = 0

            try:
                grand_total_percent = round((grand_total / grand_total) * 100,1)
            except:
                grand_total_percent = 0

            row_total = [
                    "Totals",
                    str(rowA_total) + "(" + str(rowA_total_percent) + "%" + ")",
                    str(rowB_total) + "(" + str(rowB_total_percent) + "%" + ")",
                    str(rowC_total) + "(" + str(rowC_total_percent) + "%" + ")",
                    "",
                    str(rowE_total) + "(" + str(rowE_total_percent) + "%" + ")",
                    str(rowF_total) + "(" + str(rowF_total_percent) + "%" + ")",
                    str(rowG_total) + "(" + str(rowG_total_percent) + "%" + ")",
                    str(rowH_total) + "(" + str(rowH_total_percent) + "%" + ")",
                    "",
                    str(grand_total) + "(" + str(grand_total_percent) + "%" + ")",
                ]

            data = [
                carries_risk,
                final_total_carries_risk_low ,
                final_total_carries_risk_medium ,
                final_total_carries_risk_high ,
                final_total_untreated_caries_present,
                final_total_decayed_primary_teeth ,
                final_total_decayed_permanent_teeth ,
                final_total_cavity_permanent_molar ,
                final_total_cavity_permanent_anterior ,
                final_total_active_infection,
                final_total_reversible_pulpitis ,
                final_total_need_art_filling ,
                final_total_need_sdf,
                final_total_need_extraction,
                final_total_need_fv,
                final_total_need_dentist_or_hygienist,
                row_total
                ]
            
            return Response(data)
        return Response({"message":"Do not have permission."},status=401)


    def post(self, request, format=None):
        serializer = TestCrosssectionVisualizationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))


            if start_date > end_date:
                return Response({"message":"Start date cannot be later than end date."},status=400)
            if User.objects.filter(id=request.user.id).exists():
                carries_risk=["Carries Risk"]
                total_carries_risk_low = []
                total_carries_risk_medium = []
                total_carries_risk_high = []
                total_untreated_caries_present =[]
                total_decayed_permanent_teeth = []
                total_decayed_primary_teeth = []
                total_cavity_permanent_molar = []
                total_cavity_permanent_anterior = []
                total_active_infection = []
                total_reversible_pulpitis = []
                total_need_art_filling = []
                total_need_sdf = []
                total_need_extraction = []
                total_need_fv = []
                total_need_dentist_or_hygienist = []

                reason_for_visit = serializer.validated_data['reason_for_visit']
                referral_type = serializer.validated_data['referral_type']
                
                numerator_carries_risk_low_list_6 = []
                denominator_carries_risk_low_list_6 = []
                numerator_carries_risk_low_list_12 = []
                denominator_carries_risk_low_list_12 = []
                numerator_carries_risk_low_list_15 = []
                denominator_carries_risk_low_list_15 = []
                numerator_carries_risk_low_list_lte12  = []
                denominator_carries_risk_low_list_lte12  = []
                numerator_carries_risk_low_list_13_18 = []
                denominator_carries_risk_low_list_13_18 = []
                numerator_carries_risk_low_list_19_60 = []
                denominator_carries_risk_low_list_19_60 = []
                numerator_carries_risk_low_list_gte61  = []
                denominator_carries_risk_low_list_gte61  = []

                numerator_carries_risk_medium_list_6 = []
                denominator_carries_risk_medium_list_6 = []
                numerator_carries_risk_medium_list_12 = []
                denominator_carries_risk_medium_list_12 = []
                numerator_carries_risk_medium_list_15 = []
                denominator_carries_risk_medium_list_15 = []
                numerator_carries_risk_medium_list_lte12  = []
                denominator_carries_risk_medium_list_lte12  = []
                numerator_carries_risk_medium_list_13_18 = []
                denominator_carries_risk_medium_list_13_18 = []
                numerator_carries_risk_medium_list_19_60 = []
                denominator_carries_risk_medium_list_19_60 = []
                numerator_carries_risk_medium_list_gte61  = []
                denominator_carries_risk_medium_list_gte61  = []
                
                numerator_carries_risk_high_list_6 = []
                denominator_carries_risk_high_list_6 = []
                numerator_carries_risk_high_list_12 = []
                denominator_carries_risk_high_list_12 = []
                numerator_carries_risk_high_list_15 = []
                denominator_carries_risk_high_list_15 = []
                numerator_carries_risk_high_list_lte12  = []
                denominator_carries_risk_high_list_lte12  = []
                numerator_carries_risk_high_list_13_18 = []
                denominator_carries_risk_high_list_13_18 = []
                numerator_carries_risk_high_list_19_60 = []
                denominator_carries_risk_high_list_19_60 = []
                numerator_carries_risk_high_list_gte61  = []
                denominator_carries_risk_high_list_gte61  = []

                numerator_untreated_caries_present_list_6 = []
                denominator_untreated_caries_present_list_6 = []
                numerator_untreated_caries_present_list_12 = []
                denominator_untreated_caries_present_list_12 = []
                numerator_untreated_caries_present_list_15 = []
                denominator_untreated_caries_present_list_15 = []
                numerator_untreated_caries_present_list_lte12  = []
                denominator_untreated_caries_present_list_lte12  = []
                numerator_untreated_caries_present_list_13_18 = []
                denominator_untreated_caries_present_list_13_18 = []
                numerator_untreated_caries_present_list_19_60 = []
                denominator_untreated_caries_present_list_19_60 = []
                numerator_untreated_caries_present_list_gte61  = []
                denominator_untreated_caries_present_list_gte61  = []

                numerator_decayed_permanent_teeth_list_6 = []
                numerator_decayed_permanent_teeth_list_12 = []
                numerator_decayed_permanent_teeth_list_15 = []
                numerator_decayed_permanent_teeth_list_lte12  = []
                numerator_decayed_permanent_teeth_list_13_18 = []
                numerator_decayed_permanent_teeth_list_19_60 = []
                numerator_decayed_permanent_teeth_list_gte61  = []

                numerator_decayed_primary_teeth_list_6 = []
                numerator_decayed_primary_teeth_list_12 = []
                numerator_decayed_primary_teeth_list_15 = []
                numerator_decayed_primary_teeth_list_lte12  = []
                numerator_decayed_primary_teeth_list_13_18 = []
                numerator_decayed_primary_teeth_list_19_60 = []
                numerator_decayed_primary_teeth_list_gte61  = []

                numerator_cavity_permanent_molar_list_6 = []
                denominator_cavity_permanent_molar_list_6 = []
                numerator_cavity_permanent_molar_list_12 = []
                denominator_cavity_permanent_molar_list_12 = []
                numerator_cavity_permanent_molar_list_15 = []
                denominator_cavity_permanent_molar_list_15 = []
                numerator_cavity_permanent_molar_list_lte12  = []
                denominator_cavity_permanent_molar_list_lte12  = []
                numerator_cavity_permanent_molar_list_13_18 = []
                denominator_cavity_permanent_molar_list_13_18 = []
                numerator_cavity_permanent_molar_list_19_60 = []
                denominator_cavity_permanent_molar_list_19_60 = []
                numerator_cavity_permanent_molar_list_gte61  = []
                denominator_cavity_permanent_molar_list_gte61  = []

                numerator_cavity_permanent_anterior_list_6 = []
                denominator_cavity_permanent_anterior_list_6 = []
                numerator_cavity_permanent_anterior_list_12 = []
                denominator_cavity_permanent_anterior_list_12 = []
                numerator_cavity_permanent_anterior_list_15 = []
                denominator_cavity_permanent_anterior_list_15 = []
                numerator_cavity_permanent_anterior_list_lte12  = []
                denominator_cavity_permanent_anterior_list_lte12  = []
                numerator_cavity_permanent_anterior_list_13_18 = []
                denominator_cavity_permanent_anterior_list_13_18 = []
                numerator_cavity_permanent_anterior_list_19_60 = []
                denominator_cavity_permanent_anterior_list_19_60 = []
                numerator_cavity_permanent_anterior_list_gte61  = []
                denominator_cavity_permanent_anterior_list_gte61  = []

                numerator_active_infection_list_6 = []
                denominator_active_infection_list_6 = []
                numerator_active_infection_list_12 = []
                denominator_active_infection_list_12 = []
                numerator_active_infection_list_15 = []
                denominator_active_infection_list_15 = []
                numerator_active_infection_list_lte12  = []
                denominator_active_infection_list_lte12  = []
                numerator_active_infection_list_13_18 = []
                denominator_active_infection_list_13_18 = []
                numerator_active_infection_list_19_60 = []
                denominator_active_infection_list_19_60 = []
                numerator_active_infection_list_gte61  = []
                denominator_active_infection_list_gte61  = []

                numerator_reversible_pulpitis_list_6 = []
                denominator_reversible_pulpitis_list_6 = []
                numerator_reversible_pulpitis_list_12 = []
                denominator_reversible_pulpitis_list_12 = []
                numerator_reversible_pulpitis_list_15 = []
                denominator_reversible_pulpitis_list_15 = []
                numerator_reversible_pulpitis_list_lte12  = []
                denominator_reversible_pulpitis_list_lte12  = []
                numerator_reversible_pulpitis_list_13_18 = []
                denominator_reversible_pulpitis_list_13_18 = []
                numerator_reversible_pulpitis_list_19_60 = []
                denominator_reversible_pulpitis_list_19_60 = []
                numerator_reversible_pulpitis_list_gte61  = []
                denominator_reversible_pulpitis_list_gte61  = []

                numerator_need_art_filling_list_6 = []
                denominator_need_art_filling_list_6 = []
                numerator_need_art_filling_list_12 = []
                denominator_need_art_filling_list_12 = []
                numerator_need_art_filling_list_15 = []
                denominator_need_art_filling_list_15 = []
                numerator_need_art_filling_list_lte12  = []
                denominator_need_art_filling_list_lte12  = []
                numerator_need_art_filling_list_13_18 = []
                denominator_need_art_filling_list_13_18 = []
                numerator_need_art_filling_list_19_60 = []
                denominator_need_art_filling_list_19_60 = []
                numerator_need_art_filling_list_gte61  = []
                denominator_need_art_filling_list_gte61  = []

                numerator_need_sdf_list_6 = []
                denominator_need_sdf_list_6 = []
                numerator_need_sdf_list_12 = []
                denominator_need_sdf_list_12 = []
                numerator_need_sdf_list_15 = []
                denominator_need_sdf_list_15 = []
                numerator_need_sdf_list_lte12  = []
                denominator_need_sdf_list_lte12  = []
                numerator_need_sdf_list_13_18 = []
                denominator_need_sdf_list_13_18 = []
                numerator_need_sdf_list_19_60 = []
                denominator_need_sdf_list_19_60 = []
                numerator_need_sdf_list_gte61  = []
                denominator_need_sdf_list_gte61  = []

                numerator_need_extraction_list_6 = []
                denominator_need_extraction_list_6 = []
                numerator_need_extraction_list_12 = []
                denominator_need_extraction_list_12 = []
                numerator_need_extraction_list_15 = []
                denominator_need_extraction_list_15 = []
                numerator_need_extraction_list_lte12  = []
                denominator_need_extraction_list_lte12  = []
                numerator_need_extraction_list_13_18 = []
                denominator_need_extraction_list_13_18 = []
                numerator_need_extraction_list_19_60 = []
                denominator_need_extraction_list_19_60 = []
                numerator_need_extraction_list_gte61  = []
                denominator_need_extraction_list_gte61  = []

                numerator_need_fv_list_6 = []
                denominator_need_fv_list_6 = []
                numerator_need_fv_list_12 = []
                denominator_need_fv_list_12 = []
                numerator_need_fv_list_15 = []
                denominator_need_fv_list_15 = []
                numerator_need_fv_list_lte12  = []
                denominator_need_fv_list_lte12  = []
                numerator_need_fv_list_13_18 = []
                denominator_need_fv_list_13_18 = []
                numerator_need_fv_list_19_60 = []
                denominator_need_fv_list_19_60 = []
                numerator_need_fv_list_gte61  = []
                denominator_need_fv_list_gte61  = []

                numerator_need_dentist_or_hygienist_list_6 = []
                denominator_need_dentist_or_hygienist_list_6 = []
                numerator_need_dentist_or_hygienist_list_12 = []
                denominator_need_dentist_or_hygienist_list_12 = []
                numerator_need_dentist_or_hygienist_list_15 = []
                denominator_need_dentist_or_hygienist_list_15 = []
                numerator_need_dentist_or_hygienist_list_lte12  = []
                denominator_need_dentist_or_hygienist_list_lte12  = []
                numerator_need_dentist_or_hygienist_list_13_18 = []
                denominator_need_dentist_or_hygienist_list_13_18 = []
                numerator_need_dentist_or_hygienist_list_19_60 = []
                denominator_need_dentist_or_hygienist_list_19_60 = []
                numerator_need_dentist_or_hygienist_list_gte61  = []
                denominator_need_dentist_or_hygienist_list_gte61  = []

                numerator_carries_risk_low_total = []
                numerator_carries_risk_medium_total = []
                numerator_carries_risk_high_total = []
                numerator_untreated_caries_present_total = []
                numerator_cavity_permanent_molar_total = []
                numerator_cavity_permanent_anterior_total = []
                numerator_active_infection_total = []
                numerator_reversible_pulpitis_total = []
                numerator_need_art_filling_total = []
                numerator_need_sdf_total = []
                numerator_need_extraction_total = []
                numerator_need_fv_total = []
                numerator_need_dentist_or_hygienist_total = []

                denominator_all = []
                
                # carries risk low
                for l in serializer.validated_data['location']:
                    for a in serializer.validated_data['activity']:
                        if referral_type and reason_for_visit:
                            print("inside referral type and no reason for visit")
                            # carries risk low
                            numerator_carries_risk_low_total.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            denominator_all.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_6.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_15.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_low_list_lte12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_13_18.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_19_60.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_gte61.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk medium
                            numerator_carries_risk_medium_total.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_6.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_15.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk high
                            numerator_carries_risk_high_total.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_6.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_15.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_high_list_lte12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_13_18.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_19_60.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_gte61.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # untreated caries present
                            numerator_untreated_caries_present_total.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Number of decayed primary teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_6.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_15.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_lte12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_13_18.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_19_60.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_gte61.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_gte61.append(0)

                            # Number of decayed permanent teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_6.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_15.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_lte12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_13_18.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_19_60.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_gte61.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_gte61.append(0)

                            # Cavity permanent molar or premolar
                            numerator_cavity_permanent_molar_total.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Cavity permanent anterior
                            numerator_cavity_permanent_anterior_total.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Active Infection
                            numerator_active_infection_total.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_active_infection_list_6.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_active_infection_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_active_infection_list_12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_active_infection_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_active_infection_list_15.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_active_infection_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_active_infection_list_lte12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_active_infection_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_active_infection_list_13_18.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_19_60.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_gte61.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_active_infection_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Mouth pain due to reversible pulpitis
                            numerator_reversible_pulpitis_total.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_6.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_15.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need ART filling
                            numerator_need_art_filling_total.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_6.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_15.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_art_filling_list_lte12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_13_18.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_19_60.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_gte61.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need SDF
                            numerator_need_sdf_total.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_6.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_15.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_sdf_list_lte12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_13_18.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_19_60.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_gte61.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need Extraction
                            numerator_need_extraction_total.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_6.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_15.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_extraction_list_lte12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_13_18.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_19_60.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_gte61.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need fv
                            numerator_need_fv_total.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_fv_list_6.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_fv_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_fv_list_12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_fv_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_fv_list_15.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_fv_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_fv_list_lte12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_fv_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_fv_list_13_18.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_19_60.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_gte61.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_fv_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need dentist or hygienist
                            numerator_need_dentist_or_hygienist_total.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                        
                        elif not referral_type and reason_for_visit:
                            print("inside no referral type")
                            # carries risk low
                            numerator_carries_risk_low_total.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            denominator_all.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_6.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_15.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_low_list_lte12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_13_18.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_19_60.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_gte61.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk medium
                            numerator_carries_risk_medium_total.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_6.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_15.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk high
                            numerator_carries_risk_high_total.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_6.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_15.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_high_list_lte12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_13_18.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_19_60.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_gte61.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # untreated caries present
                            numerator_untreated_caries_present_total.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Number of decayed primary teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_6.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_15.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_lte12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_13_18.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_19_60.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_gte61.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_gte61.append(0)

                            # Number of decayed permanent teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_6.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_15.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_lte12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_13_18.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_19_60.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_gte61.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_gte61.append(0)

                            # Cavity permanent molar or premolar
                            numerator_cavity_permanent_molar_total.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Cavity permanent anterior
                            numerator_cavity_permanent_anterior_total.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Active Infection
                            numerator_active_infection_total.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_active_infection_list_6.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_active_infection_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_active_infection_list_12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_active_infection_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_active_infection_list_15.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_active_infection_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_active_infection_list_lte12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_active_infection_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_active_infection_list_13_18.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_19_60.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_gte61.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_active_infection_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Mouth pain due to reversible pulpitis
                            numerator_reversible_pulpitis_total.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_6.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_15.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Need ART filling
                            numerator_need_art_filling_total.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_6.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_15.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_need_art_filling_list_lte12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_13_18.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_19_60.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_gte61.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Need SDF
                            numerator_need_sdf_total.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_6.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_15.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_need_sdf_list_lte12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_13_18.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_19_60.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_gte61.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Need Extraction
                            numerator_need_extraction_total.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_6.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_15.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_need_extraction_list_lte12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_13_18.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_19_60.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_gte61.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Need fv
                            numerator_need_fv_total.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_need_fv_list_6.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_need_fv_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_need_fv_list_12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_need_fv_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_need_fv_list_15.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_need_fv_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_need_fv_list_lte12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_fv_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_fv_list_13_18.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_19_60.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_gte61.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_fv_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())

                            # Need dentist or hygienist
                            numerator_need_dentist_or_hygienist_total.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=6).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=12).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age=15).values('patiend_id').distinct().count())

                            numerator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,reason_for_visit=reason_for_visit,age__gt=60).values('patiend_id').distinct().count())
                        elif referral_type and not reason_for_visit:
                            print("inside no reason for visit")
                            # carries risk low
                            numerator_carries_risk_low_total.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            denominator_all.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_6.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_15.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_low_list_lte12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_13_18.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_19_60.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_gte61.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk medium
                            numerator_carries_risk_medium_total.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_6.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_15.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk high
                            numerator_carries_risk_high_total.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_6.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_15.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_high_list_lte12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_13_18.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_19_60.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_gte61.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # untreated caries present
                            numerator_untreated_caries_present_total.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Number of decayed primary teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_6.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_15.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_lte12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_13_18.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_19_60.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_gte61.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_gte61.append(0)

                            # Number of decayed permanent teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_6.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_15.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_lte12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_13_18.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_19_60.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_gte61.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_gte61.append(0)

                            # Cavity permanent molar or premolar
                            numerator_cavity_permanent_molar_total.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Cavity permanent anterior
                            numerator_cavity_permanent_anterior_total.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Active Infection
                            numerator_active_infection_total.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_active_infection_list_6.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_active_infection_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_active_infection_list_12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_active_infection_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_active_infection_list_15.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_active_infection_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_active_infection_list_lte12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_active_infection_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_active_infection_list_13_18.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_19_60.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_gte61.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_active_infection_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Mouth pain due to reversible pulpitis
                            numerator_reversible_pulpitis_total.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_6.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_15.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need ART filling
                            numerator_need_art_filling_total.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_6.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_15.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_art_filling_list_lte12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_13_18.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_19_60.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_gte61.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need SDF
                            numerator_need_sdf_total.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_6.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_15.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_sdf_list_lte12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_13_18.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_19_60.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_gte61.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need Extraction
                            numerator_need_extraction_total.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_6.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_15.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_extraction_list_lte12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_13_18.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_19_60.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_gte61.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need fv
                            numerator_need_fv_total.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_fv_list_6.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_fv_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_fv_list_12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_fv_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_fv_list_15.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_fv_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_fv_list_lte12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_fv_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_fv_list_13_18.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_19_60.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_gte61.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_fv_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())

                            # Need dentist or hygienist
                            numerator_need_dentist_or_hygienist_total.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=6).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=12).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age=15).values('patiend_id').distinct().count())

                            numerator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,referral_type=referral_type,age__gt=60).values('patiend_id').distinct().count())
                        elif not referral_type and not reason_for_visit:
                            print("inside no referral and no reason for visit")
                            # carries risk low
                            numerator_carries_risk_low_total.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            denominator_all.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_6.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_15.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_low_list_lte12.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_13_18.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_19_60.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_low_list_gte61.append(Visualization.objects.filter(carries_risk="Low",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_low_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk medium
                            numerator_carries_risk_medium_total.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_6.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_15.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(carries_risk="Medium",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_medium_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # carries risk high
                            numerator_carries_risk_high_total.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_6.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_15.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_carries_risk_high_list_lte12.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_13_18.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_19_60.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_carries_risk_high_list_gte61.append(Visualization.objects.filter(carries_risk="High",created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_carries_risk_high_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # untreated caries present
                            numerator_untreated_caries_present_total.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(decayed_primary_teeth_number__gt=0)|Q(decayed_permanent_teeth_number__gt=0)).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_untreated_caries_present_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Number of decayed primary teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_6.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_15.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_lte12.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_13_18.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_19_60.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_primary_teeth_list_gte61.append(b.decayed_primary_teeth_number)
                                else:
                                    numerator_decayed_primary_teeth_list_gte61.append(0)
                            # Number of decayed permanent teeth
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_6.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_6.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_15.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_15.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_lte12.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_lte12.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_13_18.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_13_18.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60],patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_19_60.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_19_60.append(0)
                            for x in Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct():
                                b = Visualization.objects.filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60,patiend_id=x["patiend_id"]).order_by('-created_at').first()
                                if b:
                                    numerator_decayed_permanent_teeth_list_gte61.append(b.decayed_permanent_teeth_number)
                                else:
                                    numerator_decayed_permanent_teeth_list_gte61.append(0)

                            # Cavity permanent molar or premolar
                            numerator_cavity_permanent_molar_total.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(cavity_permanent_posterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_molar_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Cavity permanent anterior
                            numerator_cavity_permanent_anterior_total.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(cavity_permanent_anterior_teeth=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_cavity_permanent_anterior_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Active Infection
                            numerator_active_infection_total.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_active_infection_list_6.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_active_infection_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_active_infection_list_12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_active_infection_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_active_infection_list_15.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_active_infection_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_active_infection_list_lte12.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_active_infection_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_active_infection_list_13_18.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_19_60.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_active_infection_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_active_infection_list_gte61.append(Visualization.objects.filter(active_infection=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_active_infection_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Mouth pain due to reversible pulpitis
                            numerator_reversible_pulpitis_total.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_6.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_15.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(reversible_pulpitis=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_reversible_pulpitis_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Need ART filling
                            numerator_need_art_filling_total.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_6.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_15.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_need_art_filling_list_lte12.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_13_18.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_19_60.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_art_filling_list_gte61.append(Visualization.objects.filter(need_art_filling=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_art_filling_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Need SDF
                            numerator_need_sdf_total.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_6.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_15.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_need_sdf_list_lte12.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_13_18.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_19_60.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_sdf_list_gte61.append(Visualization.objects.filter(need_sdf=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_sdf_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Need Extraction
                            numerator_need_extraction_total.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_6.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_15.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_need_extraction_list_lte12.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_13_18.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_19_60.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_extraction_list_gte61.append(Visualization.objects.filter(need_extraction=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_extraction_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                    
                            # Need fv
                            numerator_need_fv_total.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_need_fv_list_6.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_need_fv_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_need_fv_list_12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_need_fv_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_need_fv_list_15.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_need_fv_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_need_fv_list_lte12.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_fv_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_fv_list_13_18.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_19_60.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_fv_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_fv_list_gte61.append(Visualization.objects.filter(need_fv=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_fv_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                            # Need dentist or hygienist
                            numerator_need_dentist_or_hygienist_total.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_6.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=6).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=12).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_15.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age=15).values('patiend_id').distinct().count())

                            numerator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_lte12.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__lt=13).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_13_18.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[13,18]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_19_60.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__range=[19,60]).values('patiend_id').distinct().count())
                            numerator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(need_dentist_or_hygienist=True,created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())
                            denominator_need_dentist_or_hygienist_list_gte61.append(Visualization.objects.filter(Q(carries_risk="Low")|Q(carries_risk="Medium")|Q(carries_risk="High")).filter(created_at__range=[start_date, end_date],geography_id=l.id,activities_id=a.id,age__gt=60).values('patiend_id').distinct().count())

                numerator_carries_risk_low_A = sum(numerator_carries_risk_low_list_6)
                denominator = sum(denominator_carries_risk_low_list_6)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_A/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)

                numerator_carries_risk_low_B = sum(numerator_carries_risk_low_list_12)
                denominator = sum(denominator_carries_risk_low_list_12)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_B/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)

                numerator_carries_risk_low_C = sum(numerator_carries_risk_low_list_15)
                denominator = sum(denominator_carries_risk_low_list_15)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_C/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)

                numerator_carries_risk_low_E = sum(numerator_carries_risk_low_list_lte12)
                denominator = sum(denominator_carries_risk_low_list_lte12)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_E/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)

                numerator_carries_risk_low_F = sum(numerator_carries_risk_low_list_13_18)
                denominator = sum(denominator_carries_risk_low_list_13_18)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_F/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)

                numerator_carries_risk_low_G = sum(numerator_carries_risk_low_list_19_60)
                denominator = sum(denominator_carries_risk_low_list_19_60)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_G/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)

                numerator_carries_risk_low_H = sum(numerator_carries_risk_low_list_gte61)
                denominator = sum(denominator_carries_risk_low_list_gte61)
                try:
                    total_carries_risk_low.append(round((numerator_carries_risk_low_H/denominator)*100,1))
                except:
                    total_carries_risk_low.append(0)
                
                carries_risk_low_ABC = [numerator_carries_risk_low_A,numerator_carries_risk_low_B,numerator_carries_risk_low_C]
                carries_risk_low_EFGH = [numerator_carries_risk_low_E,numerator_carries_risk_low_F,numerator_carries_risk_low_G,numerator_carries_risk_low_H]

                # carries risk medium
                numerator_carries_risk_medium_A = sum(numerator_carries_risk_medium_list_6)
                denominator = sum(denominator_carries_risk_medium_list_6)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_A/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)

                numerator_carries_risk_medium_B = sum(numerator_carries_risk_medium_list_12)
                denominator = sum(denominator_carries_risk_medium_list_12)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_B/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)

                numerator_carries_risk_medium_C = sum(numerator_carries_risk_medium_list_15)
                denominator = sum(denominator_carries_risk_medium_list_15)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_C/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)

                numerator_carries_risk_medium_E = sum(numerator_carries_risk_medium_list_lte12)
                denominator = sum(denominator_carries_risk_medium_list_lte12)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_E/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)

                numerator_carries_risk_medium_F = sum(numerator_carries_risk_medium_list_13_18)
                denominator = sum(denominator_carries_risk_medium_list_13_18)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_F/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)

                numerator_carries_risk_medium_G = sum(numerator_carries_risk_medium_list_19_60)
                denominator = sum(denominator_carries_risk_medium_list_19_60)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_G/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)

                numerator_carries_risk_medium_H = sum(numerator_carries_risk_medium_list_gte61)
                denominator = sum(denominator_carries_risk_medium_list_gte61)
                try:
                    total_carries_risk_medium.append(round((numerator_carries_risk_medium_H/denominator)*100,1))
                except:
                    total_carries_risk_medium.append(0)
                
                carries_risk_medium_ABC = [numerator_carries_risk_medium_A,numerator_carries_risk_medium_B,numerator_carries_risk_medium_C]
                carries_risk_medium_EFGH = [numerator_carries_risk_medium_E,numerator_carries_risk_medium_F,numerator_carries_risk_medium_G,numerator_carries_risk_medium_H]

                # carries risk high
                numerator_carries_risk_high_A = sum(numerator_carries_risk_high_list_6)
                denominator = sum(denominator_carries_risk_high_list_6)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_A/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)

                numerator_carries_risk_high_B = sum(numerator_carries_risk_high_list_12)
                denominator = sum(denominator_carries_risk_high_list_12)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_B/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)

                numerator_carries_risk_high_C = sum(numerator_carries_risk_high_list_15)
                denominator = sum(denominator_carries_risk_high_list_15)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_C/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)

                numerator_carries_risk_high_E = sum(numerator_carries_risk_high_list_lte12)
                denominator = sum(denominator_carries_risk_high_list_lte12)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_E/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)

                numerator_carries_risk_high_F = sum(numerator_carries_risk_high_list_13_18)
                denominator = sum(denominator_carries_risk_high_list_13_18)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_F/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)

                numerator_carries_risk_high_G = sum(numerator_carries_risk_high_list_19_60)
                denominator = sum(denominator_carries_risk_high_list_19_60)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_G/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)

                numerator_carries_risk_high_H = sum(numerator_carries_risk_high_list_gte61)
                denominator = sum(denominator_carries_risk_high_list_gte61)
                try:
                    total_carries_risk_high.append(round((numerator_carries_risk_high_H/denominator)*100,1))
                except:
                    total_carries_risk_high.append(0)
                
                carries_risk_high_ABC = [numerator_carries_risk_high_A,numerator_carries_risk_high_B,numerator_carries_risk_high_C]
                carries_risk_high_EFGH = [numerator_carries_risk_high_E,numerator_carries_risk_high_F,numerator_carries_risk_high_G,numerator_carries_risk_high_H]
                
                # p-value calculation for ABC
                # WHO Indicator age-groups
                try:
                    table_ABC1 = [carries_risk_low_ABC,carries_risk_medium_ABC,carries_risk_high_ABC]
                    stat, p, dof, expected = chi2_contingency(table_ABC1)
                    if numpy.isnan(p):
                        abc1_pvalue = "nan" 
                    else:
                        abc1_pvalue = round(p,3)
                except:
                    abc1_pvalue = 0
                total_carries_risk_low.insert(3, abc1_pvalue)
                total_carries_risk_medium.insert(3, abc1_pvalue)
                total_carries_risk_high.insert(3, abc1_pvalue)

                # p-value calculation for EFGH
                # Jevaia’s indicator age-groups
                try:
                    table_EFGH1 = [carries_risk_low_EFGH,carries_risk_medium_EFGH,carries_risk_high_EFGH]
                    stat, p, dof, expected = chi2_contingency(table_EFGH1)
                    if numpy.isnan(p):
                        efgh1_pvalue = "nan" 
                    else:
                        efgh1_pvalue = round(p,3)
                except:
                    efgh1_pvalue = 0

                total_carries_risk_low.append(efgh1_pvalue)
                total_carries_risk_medium.append(efgh1_pvalue)
                total_carries_risk_high.append(efgh1_pvalue)

                try:
                    total_carries_risk_low.append(round((sum(numerator_carries_risk_low_total)/sum(denominator_all))*100,1))
                except:
                    total_carries_risk_low.append(0)
                
                try:
                    total_carries_risk_medium.append(round((sum(numerator_carries_risk_medium_total)/sum(denominator_all))*100,1))
                except:
                    total_carries_risk_medium.append(0)
                
                try:
                    total_carries_risk_high.append(round((sum(numerator_carries_risk_high_total)/sum(denominator_all))*100,1))
                except:
                    total_carries_risk_high.append(0)


                final_total_carries_risk_low = [
                    'Low',
                    str(numerator_carries_risk_low_A ) + "(" + str(total_carries_risk_low[0]) + "%)",
                    str(numerator_carries_risk_low_B) + "(" + str(total_carries_risk_low[1]) + "%)",
                    str(numerator_carries_risk_low_C) + "(" + str(total_carries_risk_low[2]) + "%)",
                    total_carries_risk_low[3],
                    str(numerator_carries_risk_low_E) + "(" + str(total_carries_risk_low[4]) + "%)",
                    str(numerator_carries_risk_low_F) + "(" + str(total_carries_risk_low[5]) + "%)",
                    str(numerator_carries_risk_low_G) + "(" + str(total_carries_risk_low[6]) + "%)",
                    str(numerator_carries_risk_low_H) + "(" + str(total_carries_risk_low[7]) + "%)",
                    total_carries_risk_low[8],
                    str(sum(numerator_carries_risk_low_total)) + "(" + str(total_carries_risk_low[9]) + "%)",
                ]
            
                final_total_carries_risk_medium = [
                    'Medium',
                    str(numerator_carries_risk_medium_A) + "(" + str(total_carries_risk_medium[0]) + "%)",
                    str(numerator_carries_risk_medium_B) + "(" + str(total_carries_risk_medium[1]) + "%)",
                    str(numerator_carries_risk_medium_C) + "(" + str(total_carries_risk_medium[2]) + "%)",
                    total_carries_risk_medium[3],
                    str(numerator_carries_risk_medium_E) + "(" + str(total_carries_risk_medium[4]) + "%)",
                    str(numerator_carries_risk_medium_F) + "(" + str(total_carries_risk_medium[5]) + "%)",
                    str(numerator_carries_risk_medium_G) + "(" + str(total_carries_risk_medium[6]) + "%)",
                    str(numerator_carries_risk_medium_H) + "(" + str(total_carries_risk_medium[7]) + "%)",
                    total_carries_risk_medium[8],
                    str(sum(numerator_carries_risk_medium_total)) + "(" + str(total_carries_risk_medium[9]) + "%)",
                ]
                
                final_total_carries_risk_high = [
                    'High' ,
                    str(numerator_carries_risk_high_A) + "(" + str(total_carries_risk_high[0]) + "%)",
                    str(numerator_carries_risk_high_B) + "(" + str(total_carries_risk_high[1]) + "%)",
                    str(numerator_carries_risk_high_C) + "(" + str(total_carries_risk_high[2]) + "%)",
                    total_carries_risk_high[3],
                    str(numerator_carries_risk_high_E) + "(" + str(total_carries_risk_high[4]) + "%)",
                    str(numerator_carries_risk_high_F) + "(" + str(total_carries_risk_high[5]) + "%)",
                    str(numerator_carries_risk_high_G) + "(" + str(total_carries_risk_high[6]) + "%)",
                    str(numerator_carries_risk_high_H) + "(" + str(total_carries_risk_high[7]) + "%)",
                    total_carries_risk_high[8],
                    str(sum(numerator_carries_risk_high_total)) + "(" + str(total_carries_risk_high[9]) + "%)",
                ]

                # untreated caries present
                numerator_untreated_caries_present_A = sum(numerator_untreated_caries_present_list_6)
                denominator = sum(denominator_untreated_caries_present_list_6)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_A/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                numerator_untreated_caries_present_B = sum(numerator_untreated_caries_present_list_12)
                denominator = sum(denominator_untreated_caries_present_list_12)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_B/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                numerator_untreated_caries_present_C = sum(numerator_untreated_caries_present_list_15)
                denominator = sum(denominator_untreated_caries_present_list_15)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_C/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                numerator_untreated_caries_present_E = sum(numerator_untreated_caries_present_list_lte12)
                denominator = sum(denominator_untreated_caries_present_list_lte12)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_E/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                numerator_untreated_caries_present_F = sum(numerator_untreated_caries_present_list_13_18)
                denominator = sum(denominator_untreated_caries_present_list_13_18)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_F/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                numerator_untreated_caries_present_G = sum(numerator_untreated_caries_present_list_19_60)
                denominator = sum(denominator_untreated_caries_present_list_19_60)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_G/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                numerator_untreated_caries_present_H = sum(numerator_untreated_caries_present_list_gte61)
                denominator = sum(denominator_untreated_caries_present_list_gte61)
                try:
                    total_untreated_caries_present.append(round((numerator_untreated_caries_present_H/denominator)*100,1))
                except:
                    total_untreated_caries_present.append(0)

                untreated_caries_present_ABC = numerator_untreated_caries_present_A + numerator_untreated_caries_present_B + numerator_untreated_caries_present_C
                untreated_caries_present_EFGH =  numerator_untreated_caries_present_E + numerator_untreated_caries_present_F + numerator_untreated_caries_present_G + numerator_untreated_caries_present_H

                # Number of decayed primary teeth
                decayed_primary_teeth_mean_list_ABC = []
                decayed_primary_teeth_mean_list_EFGH = []
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_6),1))
                    decayed_primary_teeth_mean_list_ABC.append(round(statistics.mean(numerator_decayed_primary_teeth_list_6),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_ABC.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_12),1))
                    decayed_primary_teeth_mean_list_ABC.append(round(statistics.mean(numerator_decayed_primary_teeth_list_12),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_ABC.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_15),1))
                    decayed_primary_teeth_mean_list_ABC.append(round(statistics.mean(numerator_decayed_primary_teeth_list_15),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_ABC.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_lte12),1))
                    decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_primary_teeth_list_lte12),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_EFGH.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_13_18),1))
                    decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_primary_teeth_list_13_18),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_EFGH.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_19_60),1))
                    decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_primary_teeth_list_19_60),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_EFGH.append(0)
                
                try:
                    total_decayed_primary_teeth.append(round(statistics.stdev(numerator_decayed_primary_teeth_list_gte61),1))
                    decayed_primary_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_primary_teeth_list_gte61),1))
                except:
                    total_decayed_primary_teeth.append(0)
                    decayed_primary_teeth_mean_list_EFGH.append(0)
                                
                # Number of decayed permanent teeth
                decayed_permanent_teeth_mean_list_ABC = []
                decayed_permanent_teeth_mean_list_EFGH = []
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_6),1))
                    decayed_permanent_teeth_mean_list_ABC.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_6),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_ABC.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_12),1))
                    decayed_permanent_teeth_mean_list_ABC.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_12),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_ABC.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_15),1))
                    decayed_permanent_teeth_mean_list_ABC.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_15),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_ABC.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_lte12),1))
                    decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_lte12),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_EFGH.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_13_18),1))
                    decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_13_18),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_EFGH.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_19_60),1))
                    decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_19_60),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_EFGH.append(0)
                
                try:
                    total_decayed_permanent_teeth.append(round(statistics.stdev(numerator_decayed_permanent_teeth_list_gte61),1))
                    decayed_permanent_teeth_mean_list_EFGH.append(round(statistics.mean(numerator_decayed_permanent_teeth_list_gte61),1))
                except:
                    total_decayed_permanent_teeth.append(0)
                    decayed_permanent_teeth_mean_list_EFGH.append(0)

                # p-value calculation for ABC
                try:
                    stat, p = wilcoxon(decayed_primary_teeth_mean_list_ABC,decayed_permanent_teeth_mean_list_ABC)
                    if numpy.isnan(p):
                        abc_pvalue = "nan" 
                    else:
                        abc_pvalue = round(p,3)
                except:
                    abc_pvalue = 0
                
                total_decayed_primary_teeth.insert(3, abc_pvalue)
                total_decayed_permanent_teeth.insert(3, abc_pvalue)

                # p-value calculation for EFGH
                try:
                    stat, p = wilcoxon(decayed_primary_teeth_mean_list_EFGH,decayed_permanent_teeth_mean_list_EFGH)
                    if numpy.isnan(p):
                        efgh_pvalue = "nan" 
                    else:
                        efgh_pvalue = round(p,3)
                except:
                    efgh_pvalue = 0
                
                total_decayed_primary_teeth.append(efgh_pvalue)
                total_decayed_permanent_teeth.append(efgh_pvalue)

                overall_decayed_primary_teeth = decayed_primary_teeth_mean_list_ABC[0] + decayed_primary_teeth_mean_list_ABC[1] 
                + decayed_primary_teeth_mean_list_ABC[2] + decayed_primary_teeth_mean_list_EFGH[0]
                + decayed_primary_teeth_mean_list_EFGH[1] + decayed_primary_teeth_mean_list_EFGH[2]
                + decayed_primary_teeth_mean_list_EFGH[3]

                mean_overall_decayed_primary_teeth = round(overall_decayed_primary_teeth / 7,1)

                overall_decayed_permanent_teeth = decayed_permanent_teeth_mean_list_ABC[0] + decayed_permanent_teeth_mean_list_ABC[1] 
                + decayed_permanent_teeth_mean_list_ABC[2] + decayed_permanent_teeth_mean_list_EFGH[0]
                + decayed_permanent_teeth_mean_list_EFGH[1] + decayed_permanent_teeth_mean_list_EFGH[2]
                + decayed_permanent_teeth_mean_list_EFGH[3]

                mean_overall_decayed_permanent_teeth = round(overall_decayed_permanent_teeth / 7,1)

                
                final_total_decayed_primary_teeth = [
                    "Number of decayed primary teeth",
                    str(decayed_primary_teeth_mean_list_ABC[0]) + "(" + "SD" + str(total_decayed_primary_teeth[0]) + ")",
                    str(decayed_primary_teeth_mean_list_ABC[1]) + "(" + "SD" + str(total_decayed_primary_teeth[1]) + ")",
                    str(decayed_primary_teeth_mean_list_ABC[2]) + "(" + "SD" + str(total_decayed_primary_teeth[2]) + ")",
                    total_decayed_primary_teeth[3],
                    str(decayed_primary_teeth_mean_list_EFGH[0]) + "(" + "SD" + str(total_decayed_primary_teeth[4]) + ")",
                    str(decayed_primary_teeth_mean_list_EFGH[1]) + "(" + "SD" + str(total_decayed_primary_teeth[5]) + ")",
                    str(decayed_primary_teeth_mean_list_EFGH[2]) + "(" + "SD" + str(total_decayed_primary_teeth[6]) + ")",
                    str(decayed_primary_teeth_mean_list_EFGH[3]) + "(" + "SD" + str(total_decayed_primary_teeth[7]) + ")",
                    total_decayed_primary_teeth[8],
                    mean_overall_decayed_primary_teeth,
                ]
            
                final_total_decayed_permanent_teeth = [
                    "Number of decayed permanent teeth",
                    str(decayed_permanent_teeth_mean_list_ABC[0]) + "(" + "SD" + str(total_decayed_permanent_teeth[0]) + ")",
                    str(decayed_permanent_teeth_mean_list_ABC[1]) + "(" + "SD" + str(total_decayed_permanent_teeth[1]) + ")",
                    str(decayed_permanent_teeth_mean_list_ABC[2]) + "(" + "SD" + str(total_decayed_permanent_teeth[2]) + ")",
                    total_decayed_permanent_teeth[3],
                    str(decayed_permanent_teeth_mean_list_EFGH[0]) + "(" + "SD" + str(total_decayed_permanent_teeth[4]) + ")",
                    str(decayed_permanent_teeth_mean_list_EFGH[1]) + "(" + "SD" + str(total_decayed_permanent_teeth[5]) + ")",
                    str(decayed_permanent_teeth_mean_list_EFGH[2]) + "(" + "SD" + str(total_decayed_permanent_teeth[6]) + ")",
                    str(decayed_permanent_teeth_mean_list_EFGH[3]) + "(" + "SD" + str(total_decayed_permanent_teeth[7]) + ")",
                    total_decayed_permanent_teeth[8],
                    mean_overall_decayed_permanent_teeth,
                ]
                
                # Cavity permanent molar or premolar
                numerator_cavity_permanent_molar_A = sum(numerator_cavity_permanent_molar_list_6)
                denominator = sum(denominator_cavity_permanent_molar_list_6)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_A/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)

                numerator_cavity_permanent_molar_B = sum(numerator_cavity_permanent_molar_list_12)
                denominator = sum(denominator_cavity_permanent_molar_list_12)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_B/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)

                numerator_cavity_permanent_molar_C = sum(numerator_cavity_permanent_molar_list_15)
                denominator = sum(denominator_cavity_permanent_molar_list_15)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_C/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)

                numerator_cavity_permanent_molar_E = sum(numerator_cavity_permanent_molar_list_lte12)
                denominator = sum(denominator_cavity_permanent_molar_list_lte12)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_E/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)

                numerator_cavity_permanent_molar_F = sum(numerator_cavity_permanent_molar_list_13_18)
                denominator = sum(denominator_cavity_permanent_molar_list_13_18)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_F/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)

                numerator_cavity_permanent_molar_G = sum(numerator_cavity_permanent_molar_list_19_60)
                denominator = sum(denominator_cavity_permanent_molar_list_19_60)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_G/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)

                numerator_cavity_permanent_molar_H = sum(numerator_cavity_permanent_molar_list_gte61)
                denominator = sum(denominator_cavity_permanent_molar_list_gte61)
                try:
                    total_cavity_permanent_molar.append(round((numerator_cavity_permanent_molar_H/denominator)*100,1))
                except:
                    total_cavity_permanent_molar.append(0)
                
                cavity_permanent_molar_ABC = [numerator_cavity_permanent_molar_A,numerator_cavity_permanent_molar_B,numerator_cavity_permanent_molar_C]
                cavity_permanent_molar_EFGH = [numerator_cavity_permanent_molar_E,numerator_cavity_permanent_molar_F,numerator_cavity_permanent_molar_G,numerator_cavity_permanent_molar_H]

                # Cavity permanent anterior
                numerator_cavity_permanent_anterior_A = sum(numerator_cavity_permanent_anterior_list_6)
                denominator = sum(denominator_cavity_permanent_anterior_list_6)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_A/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator_cavity_permanent_anterior_B = sum(numerator_cavity_permanent_anterior_list_12)
                denominator = sum(denominator_cavity_permanent_anterior_list_12)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_B/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator_cavity_permanent_anterior_C = sum(numerator_cavity_permanent_anterior_list_15)
                denominator = sum(denominator_cavity_permanent_anterior_list_15)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_C/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator_cavity_permanent_anterior_E = sum(numerator_cavity_permanent_anterior_list_lte12)
                denominator = sum(denominator_cavity_permanent_anterior_list_lte12)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_E/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator_cavity_permanent_anterior_F = sum(numerator_cavity_permanent_anterior_list_13_18)
                denominator = sum(denominator_cavity_permanent_anterior_list_13_18)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_F/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator_cavity_permanent_anterior_G = sum(numerator_cavity_permanent_anterior_list_19_60)
                denominator = sum(denominator_cavity_permanent_anterior_list_19_60)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_G/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)

                numerator_cavity_permanent_anterior_H = sum(numerator_cavity_permanent_anterior_list_gte61)
                denominator = sum(denominator_cavity_permanent_anterior_list_gte61)
                try:
                    total_cavity_permanent_anterior.append(round((numerator_cavity_permanent_anterior_H/denominator)*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)
                
                cavity_permanent_anterior_ABC = [numerator_cavity_permanent_anterior_A,numerator_cavity_permanent_anterior_B,numerator_cavity_permanent_anterior_C]
                cavity_permanent_anterior_EFGH = [numerator_cavity_permanent_anterior_E,numerator_cavity_permanent_anterior_F,numerator_cavity_permanent_anterior_G,numerator_cavity_permanent_anterior_H]


                # Active Infection
                numerator_active_infection_A = sum(numerator_active_infection_list_6)
                denominator = sum(denominator_active_infection_list_6)
                try:
                    total_active_infection.append(round((numerator_active_infection_A/denominator)*100,1))
                except:
                    total_active_infection.append(0)

                numerator_active_infection_B = sum(numerator_active_infection_list_12)
                denominator = sum(denominator_active_infection_list_12)
                try:
                    total_active_infection.append(round((numerator_active_infection_B/denominator)*100,1))
                except:
                    total_active_infection.append(0)

                numerator_active_infection_C = sum(numerator_active_infection_list_15)
                denominator = sum(denominator_active_infection_list_15)
                try:
                    total_active_infection.append(round((numerator_active_infection_C/denominator)*100,1))
                except:
                    total_active_infection.append(0)

                numerator_active_infection_E = sum(numerator_active_infection_list_lte12)
                denominator = sum(denominator_active_infection_list_lte12)
                try:
                    total_active_infection.append(round((numerator_active_infection_E/denominator)*100,1))
                except:
                    total_active_infection.append(0)

                numerator_active_infection_F = sum(numerator_active_infection_list_13_18)
                denominator = sum(denominator_active_infection_list_13_18)
                try:
                    total_active_infection.append(round((numerator_active_infection_F/denominator)*100,1))
                except:
                    total_active_infection.append(0)

                numerator_active_infection_G = sum(numerator_active_infection_list_19_60)
                denominator = sum(denominator_active_infection_list_19_60)
                try:
                    total_active_infection.append(round((numerator_active_infection_G/denominator)*100,1))
                except:
                    total_active_infection.append(0)

                numerator_active_infection_H = sum(numerator_active_infection_list_gte61)
                denominator = sum(denominator_active_infection_list_gte61)
                try:
                    total_active_infection.append(round((numerator_active_infection_H/denominator)*100,1))
                except:
                    total_active_infection.append(0)
                
                active_infection_ABC = [numerator_active_infection_A,numerator_active_infection_B,numerator_active_infection_C]
                active_infection_EFGH = [numerator_active_infection_E,numerator_active_infection_F,numerator_active_infection_G,numerator_active_infection_H]
                
                # Mouth pain due to reversible pulpitis
                numerator_reversible_pulpitis_A = sum(numerator_reversible_pulpitis_list_6)
                denominator = sum(denominator_reversible_pulpitis_list_6)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_A/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                numerator_reversible_pulpitis_B = sum(numerator_reversible_pulpitis_list_12)
                denominator = sum(denominator_reversible_pulpitis_list_12)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_B/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                numerator_reversible_pulpitis_C = sum(numerator_reversible_pulpitis_list_15)
                denominator = sum(denominator_reversible_pulpitis_list_15)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_C/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                numerator_reversible_pulpitis_E = sum(numerator_reversible_pulpitis_list_lte12)
                denominator = sum(denominator_reversible_pulpitis_list_lte12)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_E/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                numerator_reversible_pulpitis_F = sum(numerator_reversible_pulpitis_list_13_18)
                denominator = sum(denominator_reversible_pulpitis_list_13_18)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_F/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                numerator_reversible_pulpitis_G = sum(numerator_reversible_pulpitis_list_19_60)
                denominator = sum(denominator_reversible_pulpitis_list_19_60)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_G/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                numerator_reversible_pulpitis_H = sum(numerator_reversible_pulpitis_list_gte61)
                denominator = sum(denominator_reversible_pulpitis_list_gte61)
                try:
                    total_reversible_pulpitis.append(round((numerator_reversible_pulpitis_H/denominator)*100,1))
                except:
                    total_reversible_pulpitis.append(0)
                
                reversible_pulpitis_ABC = [numerator_reversible_pulpitis_A,numerator_reversible_pulpitis_B,numerator_reversible_pulpitis_C]
                reversible_pulpitis_EFGH = [numerator_reversible_pulpitis_E,numerator_reversible_pulpitis_F,numerator_reversible_pulpitis_G,numerator_reversible_pulpitis_H]

                # Need ART filling
                numerator_need_art_filling_A = sum(numerator_need_art_filling_list_6)
                denominator = sum(denominator_need_art_filling_list_6)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_A/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)

                numerator_need_art_filling_B = sum(numerator_need_art_filling_list_12)
                denominator = sum(denominator_need_art_filling_list_12)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_B/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)

                numerator_need_art_filling_C = sum(numerator_need_art_filling_list_15)
                denominator = sum(denominator_need_art_filling_list_15)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_C/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)

                numerator_need_art_filling_E = sum(numerator_need_art_filling_list_lte12)
                denominator = sum(denominator_need_art_filling_list_lte12)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_E/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)

                numerator_need_art_filling_F = sum(numerator_need_art_filling_list_13_18)
                denominator = sum(denominator_need_art_filling_list_13_18)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_F/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)

                numerator_need_art_filling_G = sum(numerator_need_art_filling_list_19_60)
                denominator = sum(denominator_need_art_filling_list_19_60)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_G/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)

                numerator_need_art_filling_H = sum(numerator_need_art_filling_list_gte61)
                denominator = sum(denominator_need_art_filling_list_gte61)
                try:
                    total_need_art_filling.append(round((numerator_need_art_filling_H/denominator)*100,1))
                except:
                    total_need_art_filling.append(0)
                
                need_art_filling_ABC = [numerator_need_art_filling_A,numerator_need_art_filling_B,numerator_need_art_filling_C]
                need_art_filling_EFGH = [numerator_need_art_filling_E,numerator_need_art_filling_F,numerator_need_art_filling_G,numerator_need_art_filling_H]

                # Need SDF
                numerator_need_sdf_A = sum(numerator_need_sdf_list_6)
                denominator = sum(denominator_need_sdf_list_6)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_A/denominator)*100,1))
                except:
                    total_need_sdf.append(0)

                numerator_need_sdf_B = sum(numerator_need_sdf_list_12)
                denominator = sum(denominator_need_sdf_list_12)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_B/denominator)*100,1))
                except:
                    total_need_sdf.append(0)

                numerator_need_sdf_C = sum(numerator_need_sdf_list_15)
                denominator = sum(denominator_need_sdf_list_15)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_C/denominator)*100,1))
                except:
                    total_need_sdf.append(0)

                numerator_need_sdf_E = sum(numerator_need_sdf_list_lte12)
                denominator = sum(denominator_need_sdf_list_lte12)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_E/denominator)*100,1))
                except:
                    total_need_sdf.append(0)

                numerator_need_sdf_F = sum(numerator_need_sdf_list_13_18)
                denominator = sum(denominator_need_sdf_list_13_18)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_F/denominator)*100,1))
                except:
                    total_need_sdf.append(0)

                numerator_need_sdf_G = sum(numerator_need_sdf_list_19_60)
                denominator = sum(denominator_need_sdf_list_19_60)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_G/denominator)*100,1))
                except:
                    total_need_sdf.append(0)

                numerator_need_sdf_H = sum(numerator_need_sdf_list_gte61)
                denominator = sum(denominator_need_sdf_list_gte61)
                try:
                    total_need_sdf.append(round((numerator_need_sdf_H/denominator)*100,1))
                except:
                    total_need_sdf.append(0)
                
                need_sdf_ABC = [numerator_need_sdf_A,numerator_need_sdf_B,numerator_need_sdf_C]
                need_sdf_EFGH = [numerator_need_sdf_E,numerator_need_sdf_F,numerator_need_sdf_G,numerator_need_sdf_H]


                # Need Extraction
                numerator_need_extraction_A = sum(numerator_need_extraction_list_6)
                denominator = sum(denominator_need_extraction_list_6)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_A/denominator)*100,1))
                except:
                    total_need_extraction.append(0)

                numerator_need_extraction_B = sum(numerator_need_extraction_list_12)
                denominator = sum(denominator_need_extraction_list_12)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_B/denominator)*100,1))
                except:
                    total_need_extraction.append(0)

                numerator_need_extraction_C = sum(numerator_need_extraction_list_15)
                denominator = sum(denominator_need_extraction_list_15)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_C/denominator)*100,1))
                except:
                    total_need_extraction.append(0)

                numerator_need_extraction_E = sum(numerator_need_extraction_list_lte12)
                denominator = sum(denominator_need_extraction_list_lte12)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_E/denominator)*100,1))
                except:
                    total_need_extraction.append(0)

                numerator_need_extraction_F = sum(numerator_need_extraction_list_13_18)
                denominator = sum(denominator_need_extraction_list_13_18)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_F/denominator)*100,1))
                except:
                    total_need_extraction.append(0)

                numerator_need_extraction_G = sum(numerator_need_extraction_list_19_60)
                denominator = sum(denominator_need_extraction_list_19_60)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_G/denominator)*100,1))
                except:
                    total_need_extraction.append(0)

                numerator_need_extraction_H = sum(numerator_need_extraction_list_gte61)
                denominator = sum(denominator_need_extraction_list_gte61)
                try:
                    total_need_extraction.append(round((numerator_need_extraction_H/denominator)*100,1))
                except:
                    total_need_extraction.append(0)
                
                need_extraction_ABC = [numerator_need_extraction_A,numerator_need_extraction_B,numerator_need_extraction_C]
                need_extraction_EFGH = [numerator_need_extraction_E,numerator_need_extraction_F,numerator_need_extraction_G,numerator_need_extraction_H]

                # Need fv
                numerator_need_fv_A = sum(numerator_need_fv_list_6)
                denominator = sum(denominator_need_fv_list_6)
                try:
                    total_need_fv.append(round((numerator_need_fv_A/denominator)*100,1))
                except:
                    total_need_fv.append(0)

                numerator_need_fv_B = sum(numerator_need_fv_list_12)
                denominator = sum(denominator_need_fv_list_12)
                try:
                    total_need_fv.append(round((numerator_need_fv_B/denominator)*100,1))
                except:
                    total_need_fv.append(0)

                numerator_need_fv_C = sum(numerator_need_fv_list_15)
                denominator = sum(denominator_need_fv_list_15)
                try:
                    total_need_fv.append(round((numerator_need_fv_C/denominator)*100,1))
                except:
                    total_need_fv.append(0)

                numerator_need_fv_E = sum(numerator_need_fv_list_lte12)
                denominator = sum(denominator_need_fv_list_lte12)
                try:
                    total_need_fv.append(round((numerator_need_fv_E/denominator)*100,1))
                except:
                    total_need_fv.append(0)

                numerator_need_fv_F = sum(numerator_need_fv_list_13_18)
                denominator = sum(denominator_need_fv_list_13_18)
                try:
                    total_need_fv.append(round((numerator_need_fv_F/denominator)*100,1))
                except:
                    total_need_fv.append(0)

                numerator_need_fv_G = sum(numerator_need_fv_list_19_60)
                denominator = sum(denominator_need_fv_list_19_60)
                try:
                    total_need_fv.append(round((numerator_need_fv_G/denominator)*100,1))
                except:
                    total_need_fv.append(0)

                numerator_need_fv_H = sum(numerator_need_fv_list_gte61)
                denominator = sum(denominator_need_fv_list_gte61)
                try:
                    total_need_fv.append(round((numerator_need_fv_H/denominator)*100,1))
                except:
                    total_need_fv.append(0)
                
                need_fv_ABC = [numerator_need_fv_A,numerator_need_fv_B,numerator_need_fv_C]
                need_fv_EFGH = [numerator_need_fv_E,numerator_need_fv_F,numerator_need_fv_G,numerator_need_fv_H]

                # Need dentist or hygienist
                numerator_need_dentist_or_hygienist_A = sum(numerator_need_dentist_or_hygienist_list_6)
                denominator = sum(denominator_need_dentist_or_hygienist_list_6)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_A/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator_need_dentist_or_hygienist_B = sum(numerator_need_dentist_or_hygienist_list_12)
                denominator = sum(denominator_need_dentist_or_hygienist_list_12)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_B/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator_need_dentist_or_hygienist_C = sum(numerator_need_dentist_or_hygienist_list_15)
                denominator = sum(denominator_need_dentist_or_hygienist_list_15)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_C/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)
                

                numerator_need_dentist_or_hygienist_E = sum(numerator_need_dentist_or_hygienist_list_lte12)
                denominator = sum(denominator_need_dentist_or_hygienist_list_lte12)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_E/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator_need_dentist_or_hygienist_F = sum(numerator_need_dentist_or_hygienist_list_13_18)
                denominator = sum(denominator_need_dentist_or_hygienist_list_13_18)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_F/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator_need_dentist_or_hygienist_G = sum(numerator_need_dentist_or_hygienist_list_19_60)
                denominator = sum(denominator_need_dentist_or_hygienist_list_19_60)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_G/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)

                numerator_need_dentist_or_hygienist_H = sum(numerator_need_dentist_or_hygienist_list_gte61)
                denominator = sum(denominator_need_dentist_or_hygienist_list_gte61)
                try:
                    total_need_dentist_or_hygienist.append(round((numerator_need_dentist_or_hygienist_H/denominator)*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)
                

                need_dentist_or_hygienist_ABC = [numerator_need_dentist_or_hygienist_A,numerator_need_dentist_or_hygienist_B,numerator_need_dentist_or_hygienist_C]
                need_dentist_or_hygienist_EFGH = [numerator_need_dentist_or_hygienist_E,numerator_need_dentist_or_hygienist_F,numerator_need_dentist_or_hygienist_G,numerator_need_dentist_or_hygienist_H]

                # p-value calculation for ABC2
                # WHO Indicator age-groups
                try:
                    table_ABC2 = [untreated_caries_present_ABC,cavity_permanent_molar_ABC,cavity_permanent_anterior_ABC,active_infection_ABC,reversible_pulpitis_ABC,need_art_filling_ABC,need_sdf_ABC,need_extraction_ABC,need_fv_ABC,need_dentist_or_hygienist_ABC]
                    stat, p, dof, expected = chi2_contingency(table_ABC2)
                    if numpy.isnan(p):
                        abc2_pvalue = "nan" 
                    else:
                        abc2_pvalue = round(p,3)
                except:
                    abc2_pvalue = 0

                total_untreated_caries_present.insert(3, abc2_pvalue)
                total_cavity_permanent_molar.insert(3, abc2_pvalue)
                total_cavity_permanent_anterior.insert(3, abc2_pvalue)
                total_active_infection.insert(3, abc2_pvalue)
                total_reversible_pulpitis.insert(3, abc2_pvalue)
                total_need_art_filling.insert(3, abc2_pvalue)
                total_need_sdf.insert(3, abc2_pvalue)
                total_need_extraction.insert(3, abc2_pvalue)
                total_need_fv.insert(3, abc2_pvalue)
                total_need_dentist_or_hygienist.insert(3, abc2_pvalue)

                # p-value calculation for EFGH2
                # Jevaia’s indicator age-groups
                try:
                    table_EFGH2 = [untreated_caries_present_EFGH,cavity_permanent_molar_EFGH,cavity_permanent_anterior_EFGH,active_infection_EFGH,reversible_pulpitis_EFGH,need_art_filling_EFGH,need_sdf_EFGH,need_extraction_EFGH,need_fv_EFGH,need_dentist_or_hygienist_EFGH] 
                    stat, p, dof, expected = chi2_contingency(table_EFGH2)
                    if numpy.isnan(p):
                        efgh2_pvalue = "nan" 
                    else:
                        efgh2_pvalue = round(p,3)
                except:
                    efgh2_pvalue = 0

                total_untreated_caries_present.append(efgh2_pvalue)
                total_cavity_permanent_molar.append(efgh2_pvalue)
                total_cavity_permanent_anterior.append(efgh2_pvalue)
                total_active_infection.append(efgh2_pvalue)
                total_reversible_pulpitis.append(efgh2_pvalue)
                total_need_art_filling.append(efgh2_pvalue)
                total_need_sdf.append(efgh2_pvalue)
                total_need_extraction.append(efgh2_pvalue)
                total_need_fv.append(efgh2_pvalue)
                total_need_dentist_or_hygienist.append(efgh2_pvalue)

                try:
                    total_untreated_caries_present.append(round((sum(numerator_untreated_caries_present_total)/sum(denominator_all))*100,1))
                except:
                    total_untreated_caries_present.append(0)
                
                try:
                    total_cavity_permanent_molar.append(round((sum(numerator_cavity_permanent_molar_total)/sum(denominator_all))*100,1))
                except:
                    total_cavity_permanent_molar.append(0)
                
                try:
                    total_cavity_permanent_anterior.append(round((sum(numerator_cavity_permanent_anterior_total)/sum(denominator_all))*100,1))
                except:
                    total_cavity_permanent_anterior.append(0)
                
                try:
                    total_active_infection.append(round((sum(numerator_active_infection_total)/sum(denominator_all))*100,1))
                except:
                    total_active_infection.append(0)
                
                try:
                    total_reversible_pulpitis.append(round((sum(numerator_reversible_pulpitis_total)/sum(denominator_all))*100,1))
                except:
                    total_reversible_pulpitis.append(0)

                try:
                    total_need_art_filling.append(round((sum(numerator_need_art_filling_total)/sum(denominator_all))*100,1))
                except:
                    total_need_art_filling.append(0)
                
                try:
                    total_need_sdf.append(round((sum(numerator_need_sdf_total)/sum(denominator_all))*100,1))
                except:
                    total_need_sdf.append(0)
                
                try:
                    total_need_extraction.append(round((sum(numerator_need_extraction_total)/sum(denominator_all))*100,1))
                except:
                    total_need_extraction.append(0)
                
                try:
                    total_need_fv.append(round((sum(numerator_need_fv_total)/sum(denominator_all))*100,1))
                except:
                    total_need_fv.append(0)
                
                try:
                    total_need_dentist_or_hygienist.append(round((sum(numerator_need_dentist_or_hygienist_total)/sum(denominator_all))*100,1))
                except:
                    total_need_dentist_or_hygienist.append(0)
                
                
                final_total_untreated_caries_present = [
                    "Any untreated caries present" ,
                    str(numerator_untreated_caries_present_A) + "(" + str(total_untreated_caries_present[0]) + "%)",
                    str(numerator_untreated_caries_present_B) + "(" + str(total_untreated_caries_present[1]) + "%)",
                    str(numerator_untreated_caries_present_C) + "(" + str(total_untreated_caries_present[2]) + "%)",
                    total_untreated_caries_present[3],
                    str(numerator_untreated_caries_present_E) + "(" + str(total_untreated_caries_present[4]) + "%)",
                    str(numerator_untreated_caries_present_F) + "(" + str(total_untreated_caries_present[5]) + "%)",
                    str(numerator_untreated_caries_present_G) + "(" + str(total_untreated_caries_present[6]) + "%)",
                    str(numerator_untreated_caries_present_H) + "(" + str(total_untreated_caries_present[7]) + "%)",
                    total_untreated_caries_present[8],
                    str(sum(numerator_untreated_caries_present_total)) + "(" + str(total_untreated_caries_present[9]) + "%)",
                ]
            
                final_total_cavity_permanent_molar = [
                    "Cavity permanent molar or premolar" ,
                    str(numerator_cavity_permanent_molar_A) + "(" + str(total_cavity_permanent_molar[0]) + "%)",
                    str(numerator_cavity_permanent_molar_B) + "(" + str(total_cavity_permanent_molar[1]) + "%)",
                    str(numerator_cavity_permanent_molar_C) + "(" + str(total_cavity_permanent_molar[2]) + "%)",
                    total_cavity_permanent_molar[3],
                    str(numerator_cavity_permanent_molar_E) + "(" + str(total_cavity_permanent_molar[4]) + "%)",
                    str(numerator_cavity_permanent_molar_F) + "(" + str(total_cavity_permanent_molar[5]) + "%)",
                    str(numerator_cavity_permanent_molar_G) + "(" + str(total_cavity_permanent_molar[6]) + "%)",
                    str(numerator_cavity_permanent_molar_H) + "(" + str(total_cavity_permanent_molar[7]) + "%)",
                    total_cavity_permanent_molar[8],
                    str(sum(numerator_cavity_permanent_molar_total)) + "(" + str(total_cavity_permanent_molar[9]) + "%)",
                    ]
                
                final_total_cavity_permanent_anterior = [
                    "Cavity permanent anterior",
                    str(numerator_cavity_permanent_anterior_A) + "(" + str(total_cavity_permanent_anterior[0]) + "%)",
                    str(numerator_cavity_permanent_anterior_B) + "(" + str(total_cavity_permanent_anterior[1]) + "%)",
                    str(numerator_cavity_permanent_anterior_C) + "(" + str(total_cavity_permanent_anterior[2]) + "%)",
                    total_cavity_permanent_anterior[3],
                    str(numerator_cavity_permanent_anterior_E) + "(" + str(total_cavity_permanent_anterior[4]) + "%)",
                    str(numerator_cavity_permanent_anterior_F) + "(" + str(total_cavity_permanent_anterior[5]) + "%)",
                    str(numerator_cavity_permanent_anterior_G) + "(" + str(total_cavity_permanent_anterior[6]) + "%)",
                    str(numerator_cavity_permanent_anterior_H) + "(" + str(total_cavity_permanent_anterior[7]) + "%)",
                    total_cavity_permanent_anterior[8],
                    str(sum(numerator_cavity_permanent_anterior_total)) + "(" + str(total_cavity_permanent_anterior[9]) + "%)",
                    ]
                
                final_total_active_infection = [
                    "Active Infection" ,
                    str(numerator_active_infection_A) + "(" + str(total_active_infection[0]) + "%)",
                    str(numerator_active_infection_B) + "(" + str(total_active_infection[1]) + "%)",
                    str(numerator_active_infection_C) + "(" + str(total_active_infection[2]) + "%)",
                    total_active_infection[3],
                    str(numerator_active_infection_E) + "(" + str(total_active_infection[4]) + "%)",
                    str(numerator_active_infection_F) + "(" + str(total_active_infection[5]) + "%)",
                    str(numerator_active_infection_G) + "(" + str(total_active_infection[6]) + "%)",
                    str(numerator_active_infection_H) + "(" + str(total_active_infection[7]) + "%)",
                    total_active_infection[8],
                    str(sum(numerator_active_infection_total)) + "(" + str(total_active_infection[9]) + "%)",
                    ]
                
                final_total_reversible_pulpitis = [
                    "Mouth pain due to reversible pulpitis" ,
                    str(numerator_reversible_pulpitis_A) + "(" + str(total_reversible_pulpitis[0]) + "%)",
                    str(numerator_reversible_pulpitis_B) + "(" + str(total_reversible_pulpitis[1]) + "%)",
                    str(numerator_reversible_pulpitis_C) + "(" + str(total_reversible_pulpitis[2]) + "%)",
                    total_reversible_pulpitis[3],
                    str(numerator_reversible_pulpitis_E) + "(" + str(total_reversible_pulpitis[4]) + "%)",
                    str(numerator_reversible_pulpitis_F) + "(" + str(total_reversible_pulpitis[5]) + "%)",
                    str(numerator_reversible_pulpitis_G) + "(" + str(total_reversible_pulpitis[6]) + "%)",
                    str(numerator_reversible_pulpitis_H) + "(" + str(total_reversible_pulpitis[7]) + "%)",
                    total_reversible_pulpitis[8],
                    str(sum(numerator_reversible_pulpitis_total)) + "(" + str(total_reversible_pulpitis[9]) + "%)",
                    ]
                
                final_total_need_art_filling = [
                    "Need ART filling" ,
                    str(numerator_need_art_filling_A) + "(" + str(total_need_art_filling[0]) + "%)",
                    str(numerator_need_art_filling_B) + "(" + str(total_need_art_filling[1]) + "%)",
                    str(numerator_need_art_filling_C) + "(" + str(total_need_art_filling[2]) + "%)",
                    total_need_art_filling[3],
                    str(numerator_need_art_filling_E) + "(" + str(total_need_art_filling[4]) + "%)",
                    str(numerator_need_art_filling_F) + "(" + str(total_need_art_filling[5]) + "%)",
                    str(numerator_need_art_filling_G) + "(" + str(total_need_art_filling[6]) + "%)",
                    str(numerator_need_art_filling_H) + "(" + str(total_need_art_filling[7]) + "%)",
                    total_need_art_filling[8],
                    str(sum(numerator_need_art_filling_total)) + "(" + str(total_need_art_filling[9]) + "%)",
                    ]

                final_total_need_sdf = [
                    "Need SDF",
                    str(numerator_need_sdf_A) + "(" + str(total_need_sdf[0]) + "%)",
                    str(numerator_need_sdf_B) + "(" + str(total_need_sdf[1]) + "%)",
                    str(numerator_need_sdf_C) + "(" + str(total_need_sdf[2]) + "%)",
                    total_need_sdf[3],
                    str(numerator_need_sdf_E) + "(" + str(total_need_sdf[4]) + "%)",
                    str(numerator_need_sdf_F) + "(" + str(total_need_sdf[5]) + "%)",
                    str(numerator_need_sdf_G) + "(" + str(total_need_sdf[6]) + "%)",
                    str(numerator_need_sdf_H) + "(" + str(total_need_sdf[7]) + "%)",
                    total_need_sdf[8],
                    str(sum(numerator_need_sdf_total)) + "(" + str(total_need_sdf[9]) + "%)",
                    ]
                
                final_total_need_extraction = [
                    "Need Extraction",
                    str(numerator_need_extraction_A) + "(" + str(total_need_extraction[0]) + "%)",
                    str(numerator_need_extraction_B) + "(" + str(total_need_extraction[1]) + "%)",
                    str(numerator_need_extraction_C) + "(" + str(total_need_extraction[2]) + "%)",
                    total_need_extraction[3],
                    str(numerator_need_extraction_E) + "(" + str(total_need_extraction[4]) + "%)",
                    str(numerator_need_extraction_F) + "(" + str(total_need_extraction[5]) + "%)",
                    str(numerator_need_extraction_G) + "(" + str(total_need_extraction[6]) + "%)",
                    str(numerator_need_extraction_H) + "(" + str(total_need_extraction[7]) + "%)",
                    total_need_extraction[8],
                    str(sum(numerator_need_extraction_total)) + "(" + str(total_need_extraction[9]) + "%)",
                    ]
                
                final_total_need_fv = [
                    "Need FV",
                    str(numerator_need_fv_A) + "(" + str(total_need_fv[0]) + "%)",
                    str(numerator_need_fv_B) + "(" + str(total_need_fv[1]) + "%)",
                    str(numerator_need_fv_C) + "(" + str(total_need_fv[2]) + "%)",
                    total_need_fv[3],
                    str(numerator_need_fv_E) + "(" + str(total_need_fv[4]) + "%)",
                    str(numerator_need_fv_F) + "(" + str(total_need_fv[5]) + "%)",
                    str(numerator_need_fv_G) + "(" + str(total_need_fv[6]) + "%)",
                    str(numerator_need_fv_H) + "(" + str(total_need_fv[7]) + "%)",
                    total_need_fv[8],
                    str(sum(numerator_need_fv_total)) + "(" + str(total_need_fv[9]) + "%)",
                    ]
                
                final_total_need_dentist_or_hygienist = [
                    "Need Dentist or Hygenist",
                    str(numerator_need_dentist_or_hygienist_A) + "(" + str(total_need_dentist_or_hygienist[0]) + "%)",
                    str(numerator_need_dentist_or_hygienist_B) + "(" + str(total_need_dentist_or_hygienist[1]) + "%)",
                    str(numerator_need_dentist_or_hygienist_C) + "(" + str(total_need_dentist_or_hygienist[2]) + "%)",
                    total_need_dentist_or_hygienist[3],
                    str(numerator_need_dentist_or_hygienist_E) + "(" + str(total_need_dentist_or_hygienist[4]) + "%)",
                    str(numerator_need_dentist_or_hygienist_F) + "(" + str(total_need_dentist_or_hygienist[5]) + "%)",
                    str(numerator_need_dentist_or_hygienist_G) + "(" + str(total_need_dentist_or_hygienist[6]) + "%)",
                    str(numerator_need_dentist_or_hygienist_H) + "(" + str(total_need_dentist_or_hygienist[7]) + "%)",
                    total_need_dentist_or_hygienist[8],
                    str(sum(numerator_need_dentist_or_hygienist_total)) + "(" + str(total_need_dentist_or_hygienist[9]) + "%)",
                    ]
                
                rowA_total = numerator_carries_risk_low_A + numerator_carries_risk_medium_A + numerator_carries_risk_high_A 
            
                rowB_total = numerator_carries_risk_low_B + numerator_carries_risk_medium_B + numerator_carries_risk_high_B
                
                rowC_total = numerator_carries_risk_low_C + numerator_carries_risk_medium_C + numerator_carries_risk_high_C 

                rowE_total = numerator_carries_risk_low_E + numerator_carries_risk_medium_E + numerator_carries_risk_high_E 
                
                rowF_total = numerator_carries_risk_low_F + numerator_carries_risk_medium_F + numerator_carries_risk_high_F 
                
                rowG_total = numerator_carries_risk_low_G + numerator_carries_risk_medium_G + numerator_carries_risk_high_G 
                
                rowH_total = numerator_carries_risk_low_H + numerator_carries_risk_medium_H + numerator_carries_risk_high_H
                
            
                grand_total = rowE_total + rowF_total + rowG_total + rowH_total
                try:
                    rowA_total_percent = round((rowA_total / grand_total) * 100,1)
                except:
                    rowA_total_percent = 0

                try:
                    rowB_total_percent = round((rowB_total / grand_total) * 100,1)
                except:
                    rowB_total_percent = 0
                
                try:
                    rowC_total_percent = round((rowC_total / grand_total) * 100,1)
                except:
                    rowC_total_percent = 0
                
                try:
                    rowE_total_percent = round((rowE_total / grand_total) * 100,1)
                except:
                    rowE_total_percent = 0
                
                try:
                    rowF_total_percent = round((rowF_total / grand_total) * 100,1)
                except:
                    rowF_total_percent = 0

                try:
                    rowG_total_percent = round((rowG_total / grand_total) * 100,1)
                except:
                    rowG_total_percent = 0
                
                try:
                    rowH_total_percent = round((rowH_total / grand_total) * 100,1)
                except:
                    rowH_total_percent = 0

                try:
                    grand_total_percent = round((grand_total / grand_total) * 100,1)
                except:
                    grand_total_percent = 0

                row_total = [
                    "Totals",
                    str(rowA_total) + "(" + str(rowA_total_percent) + "%" + ")",
                    str(rowB_total) + "(" + str(rowB_total_percent) + "%" + ")",
                    str(rowC_total) + "(" + str(rowC_total_percent) + "%" + ")",
                    "",
                    str(rowE_total) + "(" + str(rowE_total_percent) + "%" + ")",
                    str(rowF_total) + "(" + str(rowF_total_percent) + "%" + ")",
                    str(rowG_total) + "(" + str(rowG_total_percent) + "%" + ")",
                    str(rowH_total) + "(" + str(rowH_total_percent) + "%" + ")",
                    "",
                    str(grand_total) + "(" + str(grand_total_percent) + "%" + ")",
                ]
   
                data = [
                    carries_risk,
                    final_total_carries_risk_low ,
                    final_total_carries_risk_medium ,
                    final_total_carries_risk_high ,
                    final_total_untreated_caries_present,
                    final_total_decayed_primary_teeth ,
                    final_total_decayed_permanent_teeth ,
                    final_total_cavity_permanent_molar ,
                    final_total_cavity_permanent_anterior ,
                    final_total_active_infection,
                    final_total_reversible_pulpitis ,
                    final_total_need_art_filling ,
                    final_total_need_sdf,
                    final_total_need_extraction,
                    final_total_need_fv,
                    final_total_need_dentist_or_hygienist,
                    row_total
                    ]
                
                return Response(data)
            return Response({"message":"Do not have permission."},status=401)
        return Response({"message":serializer.errors},status=400)    

