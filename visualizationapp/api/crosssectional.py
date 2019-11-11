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

# from datetime import datetime
# from datetime import timedelta
import logging
# Get an instance of a logger
from django.db.models import Count

logger = logging.getLogger(__name__)




np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365*18)
lessthan6 = d - datetime.timedelta(days=365*6)
lessthan12 = d - datetime.timedelta(days=365*12)
lessthan15= d - datetime.timedelta(days=365*15)
greaterthan60 = d - datetime.timedelta(days=365*60)


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class SectionalVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request,format=None):
          if User.objects.filter(id=request.user.id).exists():
              total_active_infection=Visualization.objects.filter(active_infection=True).count()
              total_active_infection_6=Visualization.objects.filter(age=6,active_infection=True).count()
              total_active_infection_12=Visualization.objects.filter(age=12,active_infection=True).count()
              total_active_infection_15=Visualization.objects.filter(age=15,active_infection=True).count()
              total_active_infection_child=Visualization.objects.filter(age__lt=18,active_infection=True).count()
              total_active_infection_adult=Visualization.objects.filter(age__range=(18,60),active_infection=True).count()
              total_active_infection_old=Visualization.objects.filter(age__gt=60,active_infection=True).count()

              total_carries_risk=Visualization.objects.all().values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_6=Visualization.objects.filter(age=6).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_12=Visualization.objects.filter(age=12).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_15=Visualization.objects.filter(age=15).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_child=Visualization.objects.filter(age__lt=18).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_adult=Visualization.objects.filter(age__range=(18,60)).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_old=Visualization.objects.filter(age__gt=60).values('carries_risk').annotate(Count('carries_risk')).count()

              otal_decayed_primary_teeth=Visualization.objects.filter(decayed_primary_teeth=True).count()
              total_decayed_primary_teeth_6=Visualization.objects.filter(age=6,decayed_primary_teeth=True).count()
              total_decayed_primary_teeth_12=Visualization.objects.filter(age=12,decayed_primary_teeth=True).count()
              total_decayed_primary_teeth_15=Visualization.objects.filter(age=15,decayed_primary_teeth=True).count()
              total_decayed_primary_teeth_child=Visualization.objects.filter(age__lt=18,decayed_primary_teeth=True).count()
              total_decayed_primary_teeth_adult=Visualization.objects.filter(age__range=(18,60),decayed_primary_teeth=True).count()
              total_decayed_primary_teeth_old=Visualization.objects.filter(age__gt=60,decayed_primary_teeth=True).count()


              total_decayed_permanent_teeth=Visualization.objects.filter(decayed_permanent_teeth=True).count()
              total_decayed_permanent_teeth_6=Visualization.objects.filter(age=6,decayed_permanent_teeth=True).count()
              total_decayed_permanent_teeth_12=Visualization.objects.filter(age=12,decayed_permanent_teeth=True).count()
              total_decayed_permanent_teeth_15=Visualization.objects.filter(age=15,decayed_permanent_teeth=True).count()
              total_decayed_permanent_teeth_child=Visualization.objects.filter(age__lt=18,decayed_permanent_teeth=True).count()
              total_decayed_permanent_teeth_adult=Visualization.objects.filter(age__range=(18,60),decayed_permanent_teeth=True).count()
              total_decayed_permanent_teeth_old=Visualization.objects.filter(age__gt=60,decayed_permanent_teeth=True).count()


              total_cavity_permanent_posterior_teeth=Visualization.objects.filter(cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_6=Visualization.objects.filter(age=6,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_12=Visualization.objects.filter(age=12,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_15=Visualization.objects.filter(age=15,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_child=Visualization.objects.filter(age__lt=18,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_adult=Visualization.objects.filter(age__range=(18,60),cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_old=Visualization.objects.filter(age__gt=60,cavity_permanent_posterior_teeth=True).count()

              total_cavity_permanent_anterior_teeth=Visualization.objects.filter(cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_6=Visualization.objects.filter(age=6,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_12=Visualization.objects.filter(age=12,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_15=Visualization.objects.filter(age=15,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_child=Visualization.objects.filter(age__lt=18,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_adult=Visualization.objects.filter(age__range=(18,60),cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_old=Visualization.objects.filter(age__gt=60,cavity_permanent_anterior_teeth=True).count()
              total_reversible_pulpitis=Visualization.objects.filter(reversible_pulpitis=True).count()
              total_reversible_pulpitis_6=Visualization.objects.filter(age=6,reversible_pulpitis=True).count()
              total_reversible_pulpitis_12=Visualization.objects.filter(age=12,reversible_pulpitis=True).count()
              total_reversible_pulpitis_15=Visualization.objects.filter(age=15,reversible_pulpitis=True).count()
              total_reversible_pulpitis_child=Visualization.objects.filter(age__lt=18,reversible_pulpitis=True).count()
              total_reversible_pulpitis_adult=Visualization.objects.filter(age__range=(18,60),reversible_pulpitis=True).count()
              total_reversible_pulpitis_old=Visualization.objects.filter(age__gt=60,reversible_pulpitis=True).count()

              total_need_art_filling=Visualization.objects.filter(need_art_filling=True).count()
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


              return Response([["Career Risk",total_carries_risk_6,total_carries_risk_12,total_carries_risk_15,total_carries_risk_child,total_carries_risk_adult,total_carries_risk_old],\
              ["Number of decayed primary teeth",total_decayed_primary_teeth_6,total_decayed_primary_teeth_12,total_decayed_primary_teeth_15,total_decayed_primary_teeth_child,total_decayed_primary_teeth_adult,total_decayed_primary_teeth_old],\
              ["Number of decayed permanent teeth",total_decayed_permanent_teeth_6,total_decayed_permanent_teeth_12,total_decayed_permanent_teeth_15,total_decayed_permanent_teeth_child,total_decayed_permanent_teeth_adult,total_decayed_permanent_teeth_old],\
              ["Cavity permanent molar or premolar",total_cavity_permanent_posterior_teeth_6,total_cavity_permanent_posterior_teeth_12,total_cavity_permanent_posterior_teeth_15,total_cavity_permanent_posterior_teeth_child,total_cavity_permanent_posterior_teeth_adult,total_cavity_permanent_posterior_teeth_old],\
              ["Cavity permanent anterior",total_cavity_permanent_anterior_teeth_6,total_cavity_permanent_anterior_teeth_12,total_cavity_permanent_anterior_teeth_15,total_cavity_permanent_anterior_teeth_child,total_cavity_permanent_anterior_teeth_adult,total_cavity_permanent_anterior_teeth_old],\
              ["Active Infection",total_active_infection_6,total_active_infection_12, total_active_infection_15,total_active_infection_child,total_active_infection_adult,total_active_infection_old],\
              ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis_6,total_reversible_pulpitis_12,total_reversible_pulpitis_15,total_reversible_pulpitis_child,total_reversible_pulpitis_adult,total_reversible_pulpitis_old],\
              ["Need ART filling",total_need_art_filling_6,total_need_art_filling_12,total_need_art_filling_15,total_need_art_filling_child,total_need_art_filling_adult,total_need_art_filling_old],\
              ["Need SDF",total_need_sdf_6,total_need_sdf_12,total_need_sdf_15,total_need_sdf_child,total_need_sdf_adult,total_need_sdf_old],\
              ["Need Extraction",total_need_extraction_6,total_need_extraction_12,total_need_extraction_15,total_need_extraction_child,total_need_extraction_adult,total_need_extraction_old]])
