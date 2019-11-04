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
              total_active_infection=Screeing.objects.filter(active_infection=True).count()
              total_active_infection_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,active_infection=True).count()
              total_active_infection_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,active_infection=True).count()
              total_active_infection_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,active_infection=True).count()
              total_active_infection_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,active_infection=True).count()
              total_active_infection_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),active_infection=True).count()
              total_active_infection_old = total_active_infection-total_active_infection_child-total_active_infection_adult

              total_carries_risk=Screeing.objects.all().count()
              total_carries_risk_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18)).values('carries_risk').annotate(Count('carries_risk')).count()
              total_carries_risk_old = total_carries_risk-total_carries_risk_child-total_carries_risk_adult

              total_decayed_primary_teeth_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6).values('decayed_primary_teeth').annotate(Count('decayed_primary_teeth')).count()
              total_decayed_primary_teeth_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12).values('decayed_primary_teeth').annotate(Count('decayed_primary_teeth')).count()
              total_decayed_primary_teeth_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15).values('decayed_primary_teeth').annotate(Count('decayed_primary_teeth')).count()
              total_decayed_primary_teeth_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18).values('decayed_primary_teeth').annotate(Count('decayed_primary_teeth')).count()
              total_decayed_primary_teeth_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18)).values('decayed_primary_teeth').annotate(Count('decayed_primary_teeth')).count()
              total_decayed_primary_teeth_old = total_carries_risk-total_decayed_primary_teeth_child-total_decayed_primary_teeth_adult

              total_decayed_permanent_teeth_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6).values('decayed_permanent_teeth').annotate(Count('decayed_permanent_teeth')).count()
              total_decayed_permanent_teeth_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12).values('decayed_permanent_teeth').annotate(Count('decayed_permanent_teeth')).count()
              total_decayed_permanent_teeth_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15).values('decayed_permanent_teeth').annotate(Count('decayed_permanent_teeth')).count()
              total_decayed_permanent_teeth_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18).values('decayed_permanent_teeth').annotate(Count('decayed_permanent_teeth')).count()
              total_decayed_permanent_teeth_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18)).values('decayed_permanent_teeth').annotate(Count('decayed_permanent_teeth')).count()
              total_decayed_permanent_teeth_old = total_carries_risk-total_carries_risk_child-total_carries_risk_adult


              total_cavity_permanent_posterior_teeth = Screeing.objects.filter(cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),cavity_permanent_posterior_teeth=True).count()
              total_cavity_permanent_posterior_teeth_old = total_cavity_permanent_posterior_teeth-total_cavity_permanent_posterior_teeth_child-total_cavity_permanent_posterior_teeth_adult

              # permanent_posterior_teeth_percent6 =str((total_cavity_permanent_posterior_teeth_lessthen6/total_cavity_permanent_posterior_teeth)*100)+"%"
              # permanent_posterior_teeth_percent12 =str((total_cavity_permanent_posterior_teeth_lessthen12/total_cavity_permanent_posterior_teeth)*100)+"%"
              # permanent_posterior_teeth_percent15 =str((total_cavity_permanent_posterior_teeth_lessthen15/total_cavity_permanent_posterior_teeth)*100)+"%"
              # permanent_posterior_teeth_percentchild =str((total_cavity_permanent_posterior_teeth_child/total_cavity_permanent_posterior_teeth)*100)+"%"
              # permanent_posterior_teeth_percentadult =str((total_cavity_permanent_posterior_teeth_adult/total_cavity_permanent_posterior_teeth)*100)+"%"
              # permanent_posterior_teeth_percentold =str((total_cavity_permanent_posterior_teeth_old/total_cavity_permanent_posterior_teeth)*100)+"%"


              total_cavity_permanent_anterior_teeth = Screeing.objects.filter(cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),cavity_permanent_anterior_teeth=True).count()
              total_cavity_permanent_anterior_teeth_old = total_cavity_permanent_anterior_teeth-total_cavity_permanent_anterior_teeth_child-total_cavity_permanent_anterior_teeth_adult


              total_reversible_pulpitis = Screeing.objects.filter(reversible_pulpitis=True).count()
              total_reversible_pulpitis_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,reversible_pulpitis=True).count()
              total_reversible_pulpitis_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,reversible_pulpitis=True).count()
              total_reversible_pulpitis_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,reversible_pulpitis=True).count()
              total_reversible_pulpitis_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,reversible_pulpitis=True).count()
              total_reversible_pulpitis_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),reversible_pulpitis=True).count()
              total_reversible_pulpitis_old = total_reversible_pulpitis-total_reversible_pulpitis_child-total_reversible_pulpitis_adult


              total_need_art_filling = Screeing.objects.filter(need_art_filling=True).count()
              total_need_art_filling_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,need_art_filling=True).count()
              total_need_art_filling_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,need_art_filling=True).count()
              total_need_art_filling_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,need_art_filling=True).count()
              total_need_art_filling_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,need_art_filling=True).count()
              total_need_art_filling_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),need_art_filling=True).count()
              total_need_art_filling_old = total_need_art_filling-total_need_art_filling_child-total_need_art_filling_adult

              total_need_sdf = Screeing.objects.filter(need_sdf=True).count()
              total_need_sdf_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,need_sdf=True).count()
              total_need_sdf_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,need_sdf=True).count()
              total_need_sdf_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,need_sdf=True).count()
              total_need_sdf_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,need_sdf=True).count()
              total_need_sdf_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),need_sdf=True).count()
              total_need_sdf_old = total_need_sdf-total_need_sdf_child-total_need_sdf_adult

              total_need_extraction = Screeing.objects.filter(need_extraction=True).count()
              total_need_extraction_lessthen6 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan6,need_extraction=True).count()
              total_need_extraction_lessthen12 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan12,need_extraction=True).count()
              total_need_extraction_lessthen15 = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan15,need_extraction=True).count()
              total_need_extraction_child = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,need_extraction=True).count()
              total_need_extraction_adult = Screeing.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),need_extraction=True).count()
              total_need_extraction_old = total_need_extraction-total_need_extraction_child-total_need_extraction_adult


              return Response([["Career Risk",total_carries_risk_lessthen6,total_carries_risk_lessthen12,total_carries_risk_lessthen15,total_carries_risk_child,total_carries_risk_adult,total_carries_risk_old],\
              ["Number of decayed primary teeth",total_decayed_primary_teeth_lessthen6,total_decayed_primary_teeth_lessthen12,total_decayed_primary_teeth_lessthen15,total_decayed_primary_teeth_child,total_decayed_primary_teeth_adult,total_decayed_primary_teeth_old],\
              ["Number of decayed permanent teeth",total_decayed_permanent_teeth_lessthen6,total_decayed_permanent_teeth_lessthen12,total_decayed_permanent_teeth_lessthen15,total_decayed_permanent_teeth_child,total_decayed_permanent_teeth_adult,total_decayed_permanent_teeth_old],\
              ["Cavity permanent molar or premolar",total_cavity_permanent_posterior_teeth_lessthen6,total_cavity_permanent_posterior_teeth_lessthen12,total_cavity_permanent_posterior_teeth_lessthen15,total_cavity_permanent_posterior_teeth_child,total_cavity_permanent_posterior_teeth_adult,total_cavity_permanent_posterior_teeth_old],\
              ["Cavity permanent anterior",total_cavity_permanent_anterior_teeth_lessthen6,total_cavity_permanent_anterior_teeth_lessthen12,total_cavity_permanent_anterior_teeth_lessthen15,total_cavity_permanent_anterior_teeth_child,total_cavity_permanent_anterior_teeth_adult,total_cavity_permanent_anterior_teeth_old],\
              ["Active Infection",total_active_infection_lessthen6,total_active_infection_lessthen12, total_active_infection_lessthen15,total_active_infection_child,total_active_infection_adult,total_active_infection_old],\
              ["Mouth pain due to reversible pulpitis",total_reversible_pulpitis_lessthen6,total_reversible_pulpitis_lessthen12,total_reversible_pulpitis_lessthen15,total_reversible_pulpitis_child,total_reversible_pulpitis_adult,total_reversible_pulpitis_old],\
              ["Need ART filling",total_need_art_filling_lessthen6,total_need_art_filling_lessthen12,total_need_art_filling_lessthen15,total_need_art_filling_child,total_need_art_filling_adult,total_need_art_filling_old],\
              ["Need SDF",total_need_sdf_lessthen6,total_need_sdf_lessthen12,total_need_sdf_lessthen15,total_need_sdf_child,total_need_sdf_adult,total_need_sdf_old],\
              ["Need Extraction",total_need_extraction_lessthen6,total_need_extraction_lessthen12,total_need_extraction_lessthen15,total_need_extraction_child,total_need_extraction_adult,total_need_extraction_old]])
