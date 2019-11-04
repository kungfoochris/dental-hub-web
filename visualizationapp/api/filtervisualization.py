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
greaterthan60 = d - datetime.timedelta(days=365*60)


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class OverviewVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request,start_date,end_date,location_id,healthpost_id,seminar_id,format=None):
            if User.objects.filter(id=request.user.id).exists():
                total_sdf = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')|Q(encounter_id__activity_area__id=healthpost_id),Q(encounter_id__activity_area__id=seminar_id)).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__patient__gender='male',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__patient__gender='female',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_child = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__patient__dob__gt=lessthan18,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_adult = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__patient__dob__range=(greaterthan60,lessthan18),encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_old = total_sdf-total_sdf_child-total_sdf_adult


                total_seal = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAl') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__patient__gender='male',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__patient__gender='female',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_child = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__patient__dob__gt=lessthan18,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_adult = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__patient__dob__range=(greaterthan60,lessthan18),encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_old = total_seal-total_seal_child-total_seal_adult



                total_art = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__patient__gender='male',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__patient__gender='female',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_child = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__patient__dob__gt=lessthan18,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_adult = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__patient__dob__range=(greaterthan60,lessthan18),encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_old = total_art-total_art_child-total_art_adult


                total_exo = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_male = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__patient__gender='male',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_female = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__patient__gender='female',encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_child = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__patient__dob__gt=lessthan18,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_adult = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__patient__dob__range=(greaterthan60,lessthan18),encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_old = total_exo-total_exo_child-total_exo_adult


                total_fv = Treatment.objects.select_related('encounter_id').filter(fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                totalfv_male = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                totalfv_female = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                totalfv_child = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                totalfv_adult = Treatment.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60,lessthan18),fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                totalfv_old = total_fv-totalfv_child-totalfv_adult

                total_sdf_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="Health Post",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_sdf_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="Training",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()


                total_exo_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="Health Post",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_exo_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="Training",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()


                total_art_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="Health Post",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_art_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="Training",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()


                total_seal_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="Health Post",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_seal_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="Training",encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()


                total_fv_health_post = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='Health Post',fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                total_fv_outreach_obj = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='Community Outreach',fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                total_fv_school_obj = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='School Seminar',fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                total_fv_training_obj = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='Training',fv_applied=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()

                total_refer = Refer.objects.select_related('encounter_id').filter(encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                total_health_post = Refer.objects.select_related('encounter_id').filter(health_post=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhealth_post_male = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',health_post=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhealth_post_female = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',health_post=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhealth_post_child = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,health_post=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhealth_post_adult = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),health_post=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhealth_post_old = total_refer-referhealth_post_child-referhealth_post_adult


                total_hygienist = Refer.objects.select_related('encounter_id').filter(hygienist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhygienist_male = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',hygienist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhygienist_female = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',hygienist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhygienist_child = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,hygienist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhygienist_adult = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),hygienist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referhygienist_old = total_hygienist-referhygienist_child-referhygienist_adult


                total_dentist = Refer.objects.select_related('encounter_id').filter(dentist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referdentist_male = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',dentist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referdentist_female = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',dentist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referdentist_child = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,dentist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referdentist_adult = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),dentist=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referdentist_old = total_dentist-referdentist_child-referdentist_adult


                total_physician = Refer.objects.select_related('encounter_id').filter(general_physician=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referphysician_male = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',general_physician=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referphysician_female = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',general_physician=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referphysician_child = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,general_physician=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referphysician_adult = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),general_physician=True,encounter_id__created_at__range=[start_date,end_date],encounter_id__geography__id=location_id).count()
                referphysician_old = total_physician-referphysician_child-referphysician_adult

                total_refer_other  = Refer.objects.select_related('encounter_id').filter(encounter_id__geography__id=location_id).values('other').annotate(Count('other')).count()
                total_refer_male = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='male',encounter_id__geography__id=location_id).values('other').annotate(Count('other')).count()
                total_refer_female = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__gender='female',encounter_id__geography__id=location_id).values('other').annotate(Count('other')).count()
                total_refer_child = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__gt=lessthan18,encounter_id__geography__id=location_id).values('other').annotate(Count('other')).count()
                total_refer_adult = Refer.objects.select_related('encounter_id').filter(encounter_id__patient__dob__range=(greaterthan60, lessthan18),encounter_id__geography__id=location_id).values('other').annotate(Count('other')).count()
                total_refer_old = total_refer_other-total_refer_child-total_refer_adult


                total_encounter = Encounter.objects.filter(geography__id=location_id).count()
                total_encounter_male = Encounter.objects.select_related('patient').filter(patient__gender='male',geography__id=location_id).count()
                total_encounter_female = Encounter.objects.select_related('patient').filter(patient__gender='female',geography__id=location_id).count()
                total_encounter_child = Encounter.objects.select_related('patient').filter(patient__dob__gt=lessthan18,geography__id=location_id).count()
                total_encounter_adult = Encounter.objects.select_related('patient').filter(patient__dob__range=(greaterthan60, lessthan18),geography__id=location_id).count()
                total_encounter_old = total_encounter-total_encounter_child-total_encounter_adult

                return Response([["Kids",total_encounter_child,total_exo_child,total_art_child,total_seal_child,total_sdf_child,totalfv_child,referhealth_post_child, referhygienist_child, referdentist_child, referphysician_child,total_refer_child],\
                    ["Adults",total_encounter_adult,total_exo_adult,total_art_adult,total_seal_adult,total_sdf_adult,totalfv_adult,referhealth_post_adult, referhygienist_adult, referdentist_adult, referphysician_adult, total_refer_adult],\
                    ["Older Adults",total_encounter_old,total_exo_old,total_art_old,total_seal_old,total_sdf_old,totalfv_old,referhealth_post_old, referhygienist_old, referdentist_old, referphysician_old,total_refer_old],\
                    ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf,total_fv,total_health_post, total_hygienist, total_dentist, total_physician,total_refer_other]])
            return Response({"treatment_obj":"do not have a permission"},status=400)





class TreatmentVisualizationFilter(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request, ward_id,format=None):
            if User.objects.filter(id=request.user.id).exists():
                total_sdf_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="Health Post",encounter_id__geography__id=ward_id).count()
                total_sdf_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__geography__id=ward_id).count()
                total_sdf_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__geography__id=ward_id).count()
                total_sdf_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__activity_area__name="Training",encounter_id__geography__id=ward_id).count()


                total_exo_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="Health Post",encounter_id__geography__id=ward_id).count()
                total_exo_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__geography__id=ward_id).count()
                total_exo_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__geography__id=ward_id).count()
                total_exo_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
                    |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
                    |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__activity_area__name="Training",encounter_id__geography__id=ward_id).count()


                total_art_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="Health Post",encounter_id__geography__id=ward_id).count()
                total_art_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__geography__id=ward_id).count()
                total_art_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__geography__id=ward_id).count()
                total_art_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__activity_area__name="Training",encounter_id__geography__id=ward_id).count()


                total_seal_health_post = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="Health Post",encounter_id__geography__id=ward_id).count()
                total_seal_school_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="School Seminar",encounter_id__geography__id=ward_id).count()
                total_seal_outreach_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="Community Outreach",encounter_id__geography__id=ward_id).count()
                total_seal_training_obj = Treatment.objects.select_related('encounter_id').filter(Q(tooth11='SEAL') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__activity_area__name="Training",encounter_id__geography__id=ward_id).count()


                total_fv_health_post = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='Health Post',fv_applied=True,encounter_id__geography__id=ward_id).count()
                total_fv_outreach_obj = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='Community Outreach',fv_applied=True,encounter_id__geography__id=ward_id).count()
                total_fv_school_obj = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='School Seminar',fv_applied=True,encounter_id__geography__id=ward_id).count()
                total_fv_training_obj = Treatment.objects.select_related('encounter_id').filter(encounter_id__activity_area__name='Training',fv_applied=True,encounter_id__geography__id=ward_id).count()
                return Response([["By Ward",0,0,0,0,0,0],\
                    ["Clinic",total_exo_health_post, total_art_health_post, total_seal_health_post, total_sdf_health_post, total_fv_health_post, 0],\
                    ["Seminar",total_exo_school_obj, total_art_school_obj, total_seal_school_obj, total_sdf_school_obj, total_fv_school_obj, 0],\
                    ["Outreach",total_exo_outreach_obj, total_art_outreach_obj, total_seal_outreach_obj, total_sdf_outreach_obj, total_fv_outreach_obj, 0],\
                    ["Training",total_exo_training_obj, total_art_training_obj, total_seal_training_obj, total_sdf_training_obj, total_fv_training_obj, 0]])
            return Response({"treatment_obj":"do not have a permission"},status=400)
