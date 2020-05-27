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

import logging
# Get an instance of a logger
from django.db.models import Count, Case, When, Value
logger = logging.getLogger(__name__)


np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365*18)
greaterthan60 = d - datetime.timedelta(days=365*60)



today_date = datetime.date.today()
last_30_days = datetime.date.today() + datetime.timedelta(-30)

today_date_obj = str(NepaliDate.from_date(today_date))
last_30_days_obj = str(NepaliDate.from_date(last_30_days))


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class OverviewVisualization1(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = OverViewVisualization
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            kid_encounter = Visualization.objects.filter(age__lt=12,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_encounter_male = Visualization.objects.filter(age__lt=12,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_encounter_female = Visualization.objects.filter(age__lt=12,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_exo = Visualization.objects.filter(age__lt=12,exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_exo_male = Visualization.objects.filter(age__lt=12,exo=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_exo_female = Visualization.objects.filter(age__lt=12,exo=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_art = Visualization.objects.filter(age__lt=12,art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_art_male = Visualization.objects.filter(age__lt=12,art=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_art_female = Visualization.objects.filter(age__lt=12,art=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_seal = Visualization.objects.filter(age__lt=12,seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_seal_male = Visualization.objects.filter(age__lt=12,seal=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_seal_female = Visualization.objects.filter(age__lt=12,seal=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_sdf = Visualization.objects.filter(age__lt=12,sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_sdf_male = Visualization.objects.filter(age__lt=12,sdf=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_sdf_female = Visualization.objects.filter(age__lt=12,sdf=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_fv = Visualization.objects.filter(age__lt=12,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_fv_male = Visualization.objects.filter(age__lt=12,fv=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_fv_female = Visualization.objects.filter(age__lt=12,fv=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_health_post = Visualization.objects.filter(age__lt=12,refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_health_post_male = Visualization.objects.filter(age__lt=12,refer_hp=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_health_post_female = Visualization.objects.filter(age__lt=12,refer_hp=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_refer_hyg = Visualization.objects.filter(age__lt=12,refer_hyg=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_hyg_male = Visualization.objects.filter(age__lt=12,refer_hyg=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_hyg_female = Visualization.objects.filter(age__lt=12,refer_hyg=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_refer_dent = Visualization.objects.filter(age__lt=12,refer_dent=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_dent_male = Visualization.objects.filter(age__lt=12,refer_dent=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_dent_female = Visualization.objects.filter(age__lt=12,refer_dent=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_refer_dr = Visualization.objects.filter(age__lt=12,refer_dr=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_dr_male = Visualization.objects.filter(age__lt=12,refer_dr=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_dr_female = Visualization.objects.filter(age__lt=12,refer_dr=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_refer_other = Visualization.objects.filter(age__lt=12,refer_other=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_other_male = Visualization.objects.filter(age__lt=12,refer_other=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_refer_other_female = Visualization.objects.filter(age__lt=12,refer_other=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            kid_sdf_whole_mouth = Visualization.objects.filter(age__lt=12,sdf_whole_mouth=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_sdf_whole_mouth_male = Visualization.objects.filter(age__lt=12,sdf_whole_mouth=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            kid_sdf_whole_mouth_female = Visualization.objects.filter(age__lt=12,sdf_whole_mouth=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()


            teen_encounter = Visualization.objects.filter(age__range=(12,19),created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_encounter_male = Visualization.objects.filter(age__range=(12,19),gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_encounter_female = Visualization.objects.filter(age__range=(12,19),gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_exo = Visualization.objects.filter(age__range=(12,19),exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_exo_male = Visualization.objects.filter(age__range=(12,19),exo=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_exo_female = Visualization.objects.filter(age__range=(12,19),exo=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_art = Visualization.objects.filter(age__range=(12,19),art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_art_male = Visualization.objects.filter(age__range=(12,19),art=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_art_female = Visualization.objects.filter(age__range=(12,19),art=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_seal = Visualization.objects.filter(age__range=(12,19),seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_seal_male = Visualization.objects.filter(age__range=(12,19),seal=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_seal_female = Visualization.objects.filter(age__range=(12,19),seal=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_sdf = Visualization.objects.filter(age__range=(12,19),sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_sdf_male = Visualization.objects.filter(age__range=(12,19),sdf=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_sdf_female = Visualization.objects.filter(age__range=(12,19),sdf=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_fv = Visualization.objects.filter(age__range=(12,19),fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_fv_male = Visualization.objects.filter(age__range=(12,19),fv=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_fv_female = Visualization.objects.filter(age__range=(12,19),fv=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_health_post = Visualization.objects.filter(age__range=(12,19),refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_health_post_male = Visualization.objects.filter(age__range=(12,19),refer_hp=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_health_post_female = Visualization.objects.filter(age__range=(12,19),refer_hp=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_refer_hyg = Visualization.objects.filter(age__range=(12,19),refer_hyg=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_hyg_male = Visualization.objects.filter(age__range=(12,19),refer_hyg=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_hyg_female = Visualization.objects.filter(age__range=(12,19),refer_hyg=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_refer_dent = Visualization.objects.filter(age__range=(12,19),refer_dent=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_dent_male = Visualization.objects.filter(age__range=(12,19),refer_dent=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_dent_female = Visualization.objects.filter(age__range=(12,19),refer_dent=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_refer_dr = Visualization.objects.filter(age__range=(12,19),refer_dr=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_dr_male = Visualization.objects.filter(age__range=(12,19),refer_dr=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_dr_female = Visualization.objects.filter(age__range=(12,19),refer_dr=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_refer_other = Visualization.objects.filter(age__range=(12,19),refer_other=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_other_male = Visualization.objects.filter(age__range=(12,19),refer_other=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_refer_other_female = Visualization.objects.filter(age__range=(12,19),refer_other=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            teen_sdf_whole_mouth = Visualization.objects.filter(age__range=(12,19),sdf_whole_mouth=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_sdf_whole_mouth_male = Visualization.objects.filter(age__range=(12,19),sdf_whole_mouth=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            teen_sdf_whole_mouth_female = Visualization.objects.filter(age__range=(12,19),sdf_whole_mouth=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_encounter = Visualization.objects.filter(age__range=(19,61),created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_encounter_male = Visualization.objects.filter(age__range=(19,61),gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_encounter_female = Visualization.objects.filter(age__range=(19,61),gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_exo = Visualization.objects.filter(age__range=(19,61),exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_exo_male = Visualization.objects.filter(age__range=(19,61),exo=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_exo_female = Visualization.objects.filter(age__range=(19,61),exo=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_art = Visualization.objects.filter(age__range=(19,61),art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_art_male = Visualization.objects.filter(age__range=(19,61),art=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_art_female = Visualization.objects.filter(age__range=(19,61),art=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_seal = Visualization.objects.filter(age__range=(19,61),seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_seal_male = Visualization.objects.filter(age__range=(19,61),seal=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_seal_female = Visualization.objects.filter(age__range=(19,61),seal=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_sdf = Visualization.objects.filter(age__range=(19,61),sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_sdf_male = Visualization.objects.filter(age__range=(19,61),sdf=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_sdf_female = Visualization.objects.filter(age__range=(19,61),sdf=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_fv = Visualization.objects.filter(age__range=(19,61),fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_fv_male = Visualization.objects.filter(age__range=(19,61),fv=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_fv_female = Visualization.objects.filter(age__range=(19,61),fv=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_health_post = Visualization.objects.filter(age__range=(19,61),refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_health_post_male = Visualization.objects.filter(age__range=(19,61),refer_hp=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_health_post_female = Visualization.objects.filter(age__range=(19,61),refer_hp=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_refer_hyg = Visualization.objects.filter(age__range=(19,61),refer_hyg=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_hyg_male = Visualization.objects.filter(age__range=(19,61),refer_hyg=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_hyg_female = Visualization.objects.filter(age__range=(19,61),refer_hyg=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_refer_dent = Visualization.objects.filter(age__range=(19,61),refer_dent=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_dent_male = Visualization.objects.filter(age__range=(19,61),refer_dent=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_dent_female = Visualization.objects.filter(age__range=(19,61),refer_dent=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_refer_dr = Visualization.objects.filter(age__range=(19,61),refer_dr=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_dr_male = Visualization.objects.filter(age__range=(19,61),refer_dr=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_dr_female = Visualization.objects.filter(age__range=(19,61),refer_dr=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_refer_other = Visualization.objects.filter(age__range=(19,61),refer_other=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_other_male = Visualization.objects.filter(age__range=(19,61),refer_other=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_refer_other_female = Visualization.objects.filter(age__range=(19,61),refer_other=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            adult_sdf_whole_mouth = Visualization.objects.filter(age__range=(19,61),sdf_whole_mouth=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_sdf_whole_mouth_male = Visualization.objects.filter(age__range=(19,61),sdf_whole_mouth=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            adult_sdf_whole_mouth_female = Visualization.objects.filter(age__range=(19,61),sdf_whole_mouth=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_encounter = Visualization.objects.filter(age__gt=60,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_encounter_male = Visualization.objects.filter(age__gt=60,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_encounter_female = Visualization.objects.filter(age__gt=60,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_exo = Visualization.objects.filter(age__gt=60,exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_exo_male = Visualization.objects.filter(age__gt=60,exo=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_exo_female = Visualization.objects.filter(age__gt=60,exo=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_art = Visualization.objects.filter(age__gt=60,art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_art_male = Visualization.objects.filter(age__gt=60,art=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_art_female = Visualization.objects.filter(age__gt=60,art=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_seal = Visualization.objects.filter(age__gt=60,seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_seal_male = Visualization.objects.filter(age__gt=60,seal=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_seal_female = Visualization.objects.filter(age__gt=60,seal=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_sdf = Visualization.objects.filter(age__gt=60,sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_sdf_male = Visualization.objects.filter(age__gt=60,sdf=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_sdf_female = Visualization.objects.filter(age__gt=60,sdf=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_fv = Visualization.objects.filter(age__gt=60,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_fv_male = Visualization.objects.filter(age__gt=60,fv=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_fv_female = Visualization.objects.filter(age__gt=60,fv=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_health_post= Visualization.objects.filter(age__gt=60,refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_health_post_male = Visualization.objects.filter(age__gt=60,refer_hp=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_health_post_female = Visualization.objects.filter(age__gt=60,refer_hp=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_refer_hyg = Visualization.objects.filter(age__gt=60,refer_hyg=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_hyg_male = Visualization.objects.filter(age__gt=60,refer_hyg=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_hyg_female = Visualization.objects.filter(age__gt=60,refer_hyg=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_refer_dent = Visualization.objects.filter(age__gt=60,refer_dent=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_dent_male = Visualization.objects.filter(age__gt=60,refer_dent=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_dent_female = Visualization.objects.filter(age__gt=60,refer_dent=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_refer_dr = Visualization.objects.filter(age__gt=60,refer_dr=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_dr_male = Visualization.objects.filter(age__gt=60,refer_dr=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_dr_female = Visualization.objects.filter(age__gt=60,refer_dr=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_refer_other = Visualization.objects.filter(age__gt=60,refer_other=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_other_male = Visualization.objects.filter(age__gt=60,refer_other=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_refer_other_female = Visualization.objects.filter(age__gt=60,refer_other=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            old_sdf_whole_mouth = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_sdf_whole_mouth_male = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True,gender="male",created_at__range=[last_30_days_obj,today_date_obj]).count()
            old_sdf_whole_mouth_female = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True,gender="female",created_at__range=[last_30_days_obj,today_date_obj]).count()

            total_encounter = kid_encounter + teen_encounter + adult_encounter + old_encounter
            total_exo = kid_exo + teen_exo + adult_exo + old_exo
            total_art = kid_art + teen_art + adult_art + old_art
            total_seal = kid_seal + teen_seal + adult_seal + old_seal
            total_sdf = kid_sdf + teen_sdf + adult_sdf + old_sdf
            total_fv = kid_fv + teen_fv + adult_fv + old_fv
            total_health_post = kid_health_post + teen_health_post + adult_health_post + old_health_post
            total_refer_hyg = kid_refer_hyg + teen_refer_hyg + adult_refer_hyg + old_refer_hyg
            total_refer_dent = kid_refer_dent + teen_refer_dent + adult_refer_dent + old_refer_dent
            total_refer_dr = kid_refer_dr + teen_refer_dr + adult_refer_dr + old_refer_dr
            total_refer_other = kid_refer_other + teen_refer_other + adult_refer_other + old_refer_other
            total_sdf_whole_mouth = kid_sdf_whole_mouth + teen_sdf_whole_mouth + adult_sdf_whole_mouth + old_sdf_whole_mouth

            return Response([["Kids (< 12)",kid_encounter, kid_exo, kid_art, kid_seal, kid_sdf, kid_sdf_whole_mouth, kid_fv, kid_health_post, kid_refer_hyg, kid_refer_dent, kid_refer_dr, kid_refer_other],\
            ['<span class="ml-4">Male</span>',kid_encounter_male, kid_exo_male, kid_art_male, kid_seal_male, kid_sdf_male, kid_sdf_whole_mouth_male, kid_fv_male, kid_health_post_male, kid_refer_hyg_male, kid_refer_dent_male, kid_refer_dr_male,kid_refer_other_male,'secondary'],\
            ['<span class="ml-4">Female</span>',kid_encounter_female, kid_exo_female, kid_art_female, kid_seal_female, kid_sdf_female, kid_sdf_whole_mouth_female, kid_fv_female, kid_health_post_female, kid_refer_hyg_female, kid_refer_dent_female, kid_refer_dr_female ,kid_refer_other_female,'secondary'],\
            ["Teens (12-18)",teen_encounter, teen_exo, teen_art, teen_seal, teen_sdf, teen_sdf_whole_mouth, teen_fv, teen_health_post, teen_refer_hyg, teen_refer_dent, teen_refer_dr, teen_refer_other],\
            ['<span class="ml-4">Male</span>',teen_encounter_male, teen_exo_male, teen_art_male, teen_seal_male, teen_sdf_male, teen_sdf_whole_mouth_male, teen_fv_male, teen_health_post_male, teen_refer_hyg_male,teen_refer_dent_male,teen_refer_dr_male,teen_refer_other_male,'secondary'],\
            ['<span class="ml-4">Female</span>',teen_encounter_female, teen_exo_female, teen_art_female, teen_seal_female, teen_sdf_female, teen_sdf_whole_mouth_female, teen_fv_female, teen_health_post_female,teen_refer_hyg_female,teen_refer_dent_female,teen_refer_dr_female,teen_refer_other_female,'secondary'],\

            ["Adults (19-60)", adult_encounter, adult_exo, adult_art,adult_seal, adult_sdf, adult_sdf_whole_mouth, adult_fv, adult_health_post, adult_refer_hyg, adult_refer_dent,adult_refer_dr, adult_refer_other],\
            ['<span class="ml-4" striped hover :basic="basic">Male</span>',adult_encounter_male, adult_exo_male, adult_art_male, adult_seal_male, adult_sdf_male, adult_sdf_whole_mouth_male, adult_fv_male, adult_health_post_male, adult_refer_hyg_male, adult_refer_dent_male, adult_refer_dr_male, adult_refer_other_male,'secondary'],\
            ['<span class="ml-4">Female</span>',adult_encounter_female, adult_exo_female, adult_art_female, adult_seal_female, adult_sdf_female, adult_sdf_whole_mouth_female, adult_fv_female, adult_health_post_female, adult_refer_hyg_female, adult_refer_dent_female, adult_refer_dr_female, adult_refer_other_female,'secondary'],\
            ["Older Adults (> 60)",old_encounter,old_exo, old_art, old_seal, old_sdf, old_sdf_whole_mouth, old_fv, old_health_post, old_refer_hyg, old_refer_dent,old_refer_dr, old_refer_other],\
            ['<span class="ml-4">Male</span>',old_encounter_male, old_exo_male,old_art_male, old_seal_male,old_sdf_male, old_sdf_whole_mouth_male, old_fv_male, old_health_post_male, old_refer_hyg_male, old_refer_dent_male, old_refer_dr_male,old_refer_other_male,'secondary'],\
            ['<span class="ml-4">Female</span>',old_encounter_female, old_exo_female,old_art_female, old_seal_female,old_sdf_female, old_sdf_whole_mouth_female,old_fv_female,old_health_post_female, old_refer_hyg_female, old_refer_dent_female, old_refer_dr_female,old_refer_other_female,'secondary'],\
            ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf, total_sdf_whole_mouth, total_fv,total_health_post, total_refer_hyg,total_refer_dent, total_refer_dr,total_refer_other]])
        return Response({"treatment_obj":"do not have a permission"},status=400)


    def post(self, request, format=None):
        serializer = OverViewVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location_list = serializer.validated_data['location']
            activities = serializer.validated_data['activities']
            total_encounter=[]
            total_exo=[]
            total_art=[]
            total_seal=[]
            total_sdf=[]
            total_sdf_whole_mouth=[]
            total_fv=[]
            total_health_post=[]
            total_refer_hyg=[]
            total_refer_dr=[]
            total_refer_dent=[]
            total_refer_other=[]


            kid_encounter=[]
            kid_encounter_male=[]
            kid_encounter_female=[]
            kid_exo =[]
            kid_exo_male =[]
            kid_exo_female = []
            kid_art = []
            kid_art_male = []
            kid_art_female = []
            kid_seal = []
            kid_seal_male = []
            kid_seal_female = []
            kid_sdf=[]
            kid_sdf_male = []
            kid_sdf_female = []
            kid_fv = []
            kid_fv_male = []
            kid_fv_female = []
            kid_health_post = []
            kid_health_post_male = []
            kid_health_post_female = []
            kid_refer_hyg = []
            kid_refer_hyg_male = []
            kid_refer_hyg_female = []
            kid_refer_dent =[]
            kid_refer_dent_male = []
            kid_refer_dent_female = []
            kid_refer_dr = []
            kid_refer_dr_male = []
            kid_refer_dr_female = []
            kid_refer_other = []
            kid_refer_other_male = []
            kid_refer_other_female = []
            kid_sdf_whole_mouth = []
            kid_sdf_whole_mouth_male = []
            kid_sdf_whole_mouth_female = []

            teen_encounter=[]
            teen_encounter_male=[]
            teen_encounter_female=[]
            teen_exo =[]
            teen_exo_male =[]
            teen_exo_female = []
            teen_art = []
            teen_art_male = []
            teen_art_female = []
            teen_seal = []
            teen_seal_male = []
            teen_seal_female = []
            teen_sdf=[]
            teen_sdf_male = []
            teen_sdf_female = []
            teen_fv = []
            teen_fv_male = []
            teen_fv_female = []
            teen_health_post = []
            teen_health_post_male = []
            teen_health_post_female = []
            teen_refer_hyg = []
            teen_refer_hyg_male = []
            teen_refer_hyg_female = []
            teen_refer_dent =[]
            teen_refer_dent_male = []
            teen_refer_dent_female = []
            teen_refer_dr = []
            teen_refer_dr_male = []
            teen_refer_dr_female = []
            teen_refer_other = []
            teen_refer_other_male = []
            teen_refer_other_female = []
            teen_sdf_whole_mouth = []
            teen_sdf_whole_mouth_male = []
            teen_sdf_whole_mouth_female = []

            adult_encounter = []
            adult_encounter_male = []
            adult_encounter_female = []
            adult_exo =[]
            adult_exo_male =[]
            adult_exo_female = []
            adult_art = []
            adult_art_male = []
            adult_art_female = []
            adult_seal = []
            adult_seal_male = []
            adult_seal_female = []
            adult_sdf=[]
            adult_sdf_male = []
            adult_sdf_female = []
            adult_fv = []
            adult_fv_male = []
            adult_fv_female = []
            adult_health_post = []
            adult_health_post_male = []
            adult_health_post_female = []
            adult_refer_hyg = []
            adult_refer_hyg_male = []
            adult_refer_hyg_female = []
            adult_refer_dent =[]
            adult_refer_dent_male = []
            adult_refer_dent_female = []
            adult_refer_dr = []
            adult_refer_dr_male = []
            adult_refer_dr_female = []
            adult_refer_other = []
            adult_refer_other_male = []
            adult_refer_other_female = []
            adult_sdf_whole_mouth = []
            adult_sdf_whole_mouth_male = []
            adult_sdf_whole_mouth_female = []

            old_encounter = []
            old_encounter_male = []
            old_encounter_female = []
            old_exo =[]
            old_exo_male =[]
            old_exo_female = []
            old_art = []
            old_art_male = []
            old_art_female = []
            old_seal = []
            old_seal_male = []
            old_seal_female = []
            old_sdf=[]
            old_sdf_male = []
            old_sdf_female = []
            old_fv = []
            old_fv_male = []
            old_fv_female = []
            old_health_post = []
            old_health_post_male = []
            old_health_post_female = []
            old_refer_hyg = []
            old_refer_hyg_male = []
            old_refer_hyg_female = []
            old_refer_dent =[]
            old_refer_dent_male = []
            old_refer_dent_female = []
            old_refer_dr = []
            old_refer_dr_male = []
            old_refer_dr_female = []
            old_refer_other = []
            old_refer_other_male = []
            old_refer_other_female = []
            old_sdf_whole_mouth = []
            old_sdf_whole_mouth_male = []
            old_sdf_whole_mouth_female = []
            if(end_date > start_date):
                if not location_list:
                    for i in activities:
                        kid_encounter.append(Visualization.objects.filter(age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_encounter_male.append(Visualization.objects.filter(age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_encounter_female.append(Visualization.objects.filter(age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_exo.append(Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_exo_male.append(Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_exo_female.append(Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_art.append(Visualization.objects.filter(art=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_art_male.append(Visualization.objects.filter(art=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_art_female.append(Visualization.objects.filter(art=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_seal.append(Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_seal_male.append(Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_seal_female.append(Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_sdf.append(Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_sdf_male.append(Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_sdf_female.append(Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())
                        kid_fv.append(Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_fv_male.append(Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_fv_female.append(Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_health_post.append(Visualization.objects.filter(refer_hp=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_health_post_male.append(Visualization.objects.filter(refer_hp=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_health_post_female.append(Visualization.objects.filter(refer_hp=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_refer_hyg.append(Visualization.objects.filter(refer_hyg=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_refer_hyg_male.append(Visualization.objects.filter(refer_hyg=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_refer_hyg_female.append(Visualization.objects.filter(refer_hyg=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_refer_dent.append(Visualization.objects.filter(refer_dent=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_refer_dent_male.append(Visualization.objects.filter(refer_dent=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_refer_dent_female.append(Visualization.objects.filter(refer_dent=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_refer_dr.append(Visualization.objects.filter(refer_dr=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_refer_dr_male.append(Visualization.objects.filter(refer_dr=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_refer_dr_female.append(Visualization.objects.filter(refer_dr=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_refer_other.append(Visualization.objects.filter(refer_other=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_refer_other_male.append(Visualization.objects.filter(refer_other=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_refer_other_female.append(Visualization.objects.filter(refer_other=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        kid_sdf_whole_mouth.append(Visualization.objects.filter(sdf_whole_mouth=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        kid_sdf_whole_mouth_male.append(Visualization.objects.filter(sdf_whole_mouth=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        kid_sdf_whole_mouth_female.append(Visualization.objects.filter(sdf_whole_mouth=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())


                        teen_encounter.append(Visualization.objects.filter(age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_encounter_male.append(Visualization.objects.filter(age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_encounter_female.append(Visualization.objects.filter(age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_exo.append(Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_exo_male.append(Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_exo_female.append(Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_art.append(Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_art_male.append(Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_art_female.append(Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_seal.append(Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_seal_male.append(Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_seal_female.append(Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_sdf.append(Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_sdf_male.append(Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_sdf_female.append(Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())
                        teen_fv.append(Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_fv_male.append(Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_fv_female.append(Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_health_post.append(Visualization.objects.filter(refer_hp=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_health_post_male.append(Visualization.objects.filter(refer_hp=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_health_post_female.append(Visualization.objects.filter(refer_hp=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_refer_hyg.append(Visualization.objects.filter(refer_hyg=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_refer_hyg_male.append(Visualization.objects.filter(refer_hyg=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_refer_hyg_female.append(Visualization.objects.filter(refer_hyg=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_refer_dent.append(Visualization.objects.filter(refer_dent=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_refer_dent_male.append(Visualization.objects.filter(refer_dent=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_refer_dent_female.append(Visualization.objects.filter(refer_dent=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_refer_dr.append(Visualization.objects.filter(refer_dr=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_refer_dr_male.append(Visualization.objects.filter(refer_dr=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_refer_dr_female.append(Visualization.objects.filter(refer_dr=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_refer_other.append(Visualization.objects.filter(refer_other=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_refer_other_male.append(Visualization.objects.filter(refer_other=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_refer_other_female.append(Visualization.objects.filter(refer_other=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        teen_sdf_whole_mouth.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        teen_sdf_whole_mouth_male.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        teen_sdf_whole_mouth_female.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_encounter.append(Visualization.objects.filter(age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_encounter_male.append(Visualization.objects.filter(age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_encounter_female.append(Visualization.objects.filter(age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_exo.append(Visualization.objects.filter(exo=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_exo_male.append(Visualization.objects.filter(exo=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_exo_female.append(Visualization.objects.filter(exo=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_art.append(Visualization.objects.filter(art=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_art_male.append(Visualization.objects.filter(art=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_art_female.append(Visualization.objects.filter(art=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_seal.append(Visualization.objects.filter(seal=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_seal_male.append(Visualization.objects.filter(seal=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_seal_female.append(Visualization.objects.filter(seal=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_sdf.append(Visualization.objects.filter(sdf=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_sdf_male.append(Visualization.objects.filter(sdf=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_sdf_female.append(Visualization.objects.filter(sdf=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_fv.append(Visualization.objects.filter(fv=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_fv_male.append(Visualization.objects.filter(fv=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_fv_female.append(Visualization.objects.filter(fv=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_health_post.append(Visualization.objects.filter(refer_hp=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_health_post_male.append(Visualization.objects.filter(refer_hp=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_health_post_female.append(Visualization.objects.filter(refer_hp=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_refer_hyg.append(Visualization.objects.filter(refer_hyg=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_refer_hyg_male.append(Visualization.objects.filter(refer_hyg=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_refer_hyg_female.append(Visualization.objects.filter(refer_hyg=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_refer_dent.append(Visualization.objects.filter(refer_dent=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_refer_dent_male.append(Visualization.objects.filter(refer_dent=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_refer_dent_female.append(Visualization.objects.filter(refer_dent=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_refer_dr.append(Visualization.objects.filter(refer_dr=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_refer_dr_male.append(Visualization.objects.filter(refer_dr=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_refer_dr_female.append(Visualization.objects.filter(refer_dr=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_refer_other.append(Visualization.objects.filter(refer_other=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_refer_other_male.append(Visualization.objects.filter(refer_other=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_refer_other_female.append(Visualization.objects.filter(refer_other=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        adult_sdf_whole_mouth.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(19,61),created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        adult_sdf_whole_mouth_male.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        adult_sdf_whole_mouth_female.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())


                        old_encounter.append(Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_encounter_male.append(Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_encounter_female.append(Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_exo.append(Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_exo_male.append(Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_exo_female.append(Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_art.append(Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_art_male.append(Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_art_female.append(Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_seal.append(Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_seal_male.append(Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_seal_female.append(Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_sdf.append(Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_sdf_male.append(Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_sdf_female.append(Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_fv.append(Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_fv_male.append(Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_fv_female.append(Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_health_post.append(Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_health_post_male.append(Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_health_post_female.append(Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_refer_hyg.append(Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_refer_hyg_male.append(Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_refer_hyg_female.append(Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_refer_dent.append(Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_refer_dent_male.append(Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_refer_dent_female.append(Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())
                        old_refer_dr.append(Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_refer_dr_male.append(Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_refer_dr_female.append(Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())
                        old_refer_other.append(Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_refer_other_male.append(Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_refer_other_female.append(Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())

                        old_sdf_whole_mouth.append(Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date]).filter(activities_id=i.id).count())
                        old_sdf_whole_mouth_male.append(Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id).count())
                        old_sdf_whole_mouth_female.append(Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id).count())
                else:
                    for location in location_list:
                        kid_encounter1=[]
                        kid_encounter_male1=[]
                        kid_encounter_female1=[]
                        kid_exo1 =[]
                        kid_exo_male1 =[]
                        kid_exo_female1 = []
                        kid_art1 = []
                        kid_art_male1 = []
                        kid_art_female1 = []
                        kid_seal1 = []
                        kid_seal_male1 = []
                        kid_seal_female1 = []
                        kid_sdf1=[]
                        kid_sdf_male1 = []
                        kid_sdf_female1 = []
                        kid_fv1 = []
                        kid_fv_male1 = []
                        kid_fv_female1 = []
                        kid_health_post1 = []
                        kid_health_post_male1 = []
                        kid_health_post_female1 = []
                        kid_refer_hyg1 = []
                        kid_refer_hyg_male1 = []
                        kid_refer_hyg_female1 = []
                        kid_refer_dent1 =[]
                        kid_refer_dent_male1 = []
                        kid_refer_dent_female1 = []
                        kid_refer_dr1 = []
                        kid_refer_dr_male1 = []
                        kid_refer_dr_female1 = []
                        kid_refer_other1 = []
                        kid_refer_other_male1 = []
                        kid_refer_other_female1 = []
                        kid_sdf_whole_mouth1 = []
                        kid_sdf_whole_mouth_male1 = []
                        kid_sdf_whole_mouth_female1 = []

                        teen_encounter1=[]
                        teen_encounter_male1=[]
                        teen_encounter_female1=[]
                        teen_exo1 =[]
                        teen_exo_male1 =[]
                        teen_exo_female1 = []
                        teen_art1 = []
                        teen_art_male1 = []
                        teen_art_female1 = []
                        teen_seal1 = []
                        teen_seal_male1 = []
                        teen_seal_female1 = []
                        teen_sdf1=[]
                        teen_sdf_male1 = []
                        teen_sdf_female1 = []
                        teen_fv1 = []
                        teen_fv_male1 = []
                        teen_fv_female1 = []
                        teen_health_post1 = []
                        teen_health_post_male1 = []
                        teen_health_post_female1 = []
                        teen_refer_hyg1 = []
                        teen_refer_hyg_male1 = []
                        teen_refer_hyg_female1 = []
                        teen_refer_dent1 =[]
                        teen_refer_dent_male1 = []
                        teen_refer_dent_female1 = []
                        teen_refer_dr1 = []
                        teen_refer_dr_male1 = []
                        teen_refer_dr_female1 = []
                        teen_refer_other1 = []
                        teen_refer_other_male1 = []
                        teen_refer_other_female1 = []
                        teen_sdf_whole_mouth1 = []
                        teen_sdf_whole_mouth_male1 = []
                        teen_sdf_whole_mouth_female1 = []

                        adult_encounter1 = []
                        adult_encounter_male1 = []
                        adult_encounter_female1 = []
                        adult_exo1 =[]
                        adult_exo_male1 =[]
                        adult_exo_female1 = []
                        adult_art1 = []
                        adult_art_male1 = []
                        adult_art_female1 = []
                        adult_seal1 = []
                        adult_seal_male1 = []
                        adult_seal_female1 = []
                        adult_sdf1=[]
                        adult_sdf_male1 = []
                        adult_sdf_female1 = []
                        adult_fv1 = []
                        adult_fv_male1 = []
                        adult_fv_female1 = []
                        adult_health_post1 = []
                        adult_health_post_male1 = []
                        adult_health_post_female1 = []
                        adult_refer_hyg1 = []
                        adult_refer_hyg_male1 = []
                        adult_refer_hyg_female1 = []
                        adult_refer_dent1 =[]
                        adult_refer_dent_male1 = []
                        adult_refer_dent_female1 = []
                        adult_refer_dr1 = []
                        adult_refer_dr_male1 = []
                        adult_refer_dr_female1 = []
                        adult_refer_other1 = []
                        adult_refer_other_male1 = []
                        adult_refer_other_female1 = []
                        adult_sdf_whole_mouth1 = []
                        adult_sdf_whole_mouth_male1 = []
                        adult_sdf_whole_mouth_female1 = []

                        old_encounter1 = []
                        old_encounter_male1 = []
                        old_encounter_female1 = []
                        old_exo1 =[]
                        old_exo_male1 =[]
                        old_exo_female1 = []
                        old_art1 = []
                        old_art_male1 = []
                        old_art_female1 = []
                        old_seal1 = []
                        old_seal_male1 = []
                        old_seal_female1 = []
                        old_sdf1=[]
                        old_sdf_male1 = []
                        old_sdf_female1 = []
                        old_fv1 = []
                        old_fv_male1 = []
                        old_fv_female1 = []
                        old_health_post1 = []
                        old_health_post_male1 = []
                        old_health_post_female1 = []
                        old_refer_hyg1 = []
                        old_refer_hyg_male1 = []
                        old_refer_hyg_female1 = []
                        old_refer_dent1 =[]
                        old_refer_dent_male1 = []
                        old_refer_dent_female1 = []
                        old_refer_dr1 = []
                        old_refer_dr_male1 = []
                        old_refer_dr_female1 = []
                        old_refer_other1 = []
                        old_refer_other_male1 = []
                        old_refer_other_female1 = []
                        old_sdf_whole_mouth1 = []
                        old_sdf_whole_mouth_male1 = []
                        old_sdf_whole_mouth_female1 = []
                        for i in activities:
                            kid_encounter1.append(Visualization.objects.filter(age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_encounter_male1.append(Visualization.objects.filter(age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_encounter_female1.append(Visualization.objects.filter(age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_exo1.append(Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_exo_male1.append(Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_exo_female1.append(Visualization.objects.filter(exo=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_art1.append(Visualization.objects.filter(art=True,age__lt=12,created_at__range=[start_date,end_date]).filter(activities_id=i.id,geography_id=location.id).count())
                            kid_art_male1.append(Visualization.objects.filter(art=True,age__lt=12,created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id,geography_id=location.id).count())
                            kid_art_female1.append(Visualization.objects.filter(art=True,age__lt=12,created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id,geography_id=location.id).count())

                            kid_seal1.append(Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_seal_male1.append(Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_seal_female1.append(Visualization.objects.filter(seal=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_sdf1.append(Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_sdf_male1.append(Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_sdf_female1.append(Visualization.objects.filter(sdf=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_fv1.append(Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_fv_male1.append(Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_fv_female1.append(Visualization.objects.filter(fv=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_health_post1.append(Visualization.objects.filter(refer_hp=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_health_post_male1.append(Visualization.objects.filter(refer_hp=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_health_post_female1.append(Visualization.objects.filter(refer_hp=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_refer_hyg1.append(Visualization.objects.filter(refer_hyg=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_hyg_male1.append(Visualization.objects.filter(refer_hyg=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_hyg_female1.append(Visualization.objects.filter(refer_hyg=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_refer_dent1.append(Visualization.objects.filter(refer_dent=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_dent_male1.append(Visualization.objects.filter(refer_dent=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_dent_female1.append(Visualization.objects.filter(refer_dent=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_refer_dr1.append(Visualization.objects.filter(refer_dr=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_dr_male1.append(Visualization.objects.filter(refer_dr=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_dr_female1.append(Visualization.objects.filter(refer_dr=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_refer_other1.append(Visualization.objects.filter(refer_other=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_other_male1.append(Visualization.objects.filter(refer_other=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_refer_other_female1.append(Visualization.objects.filter(refer_other=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            kid_sdf_whole_mouth1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__lt=12,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            kid_sdf_whole_mouth_male1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__lt=12,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            kid_sdf_whole_mouth_female1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__lt=12,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_encounter1.append(Visualization.objects.filter(age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_encounter_male1.append(Visualization.objects.filter(age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_encounter_female1.append(Visualization.objects.filter(age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_exo1.append(Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=i.id).count())
                            teen_exo_male1.append(Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location).filter(activities_id=i.id).count())
                            teen_exo_female1.append(Visualization.objects.filter(exo=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location).filter(activities_id=i.id).count())

                            teen_art1.append(Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[start_date,end_date]).filter(activities_id=i.id,geography_id=location.id).count())
                            teen_art_male1.append(Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male").filter(activities_id=i.id,geography_id=location.id).count())
                            teen_art_female1.append(Visualization.objects.filter(art=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female").filter(activities_id=i.id,geography_id=location.id).count())

                            teen_seal1.append(Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_seal_male1.append(Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_seal_female1.append(Visualization.objects.filter(seal=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_sdf1.append(Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_sdf_male1.append(Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_sdf_female1.append(Visualization.objects.filter(sdf=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_fv1.append(Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_fv_male1.append(Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_fv_female1.append(Visualization.objects.filter(fv=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_health_post1.append(Visualization.objects.filter(refer_hp=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_health_post_male1.append(Visualization.objects.filter(refer_hp=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_health_post_female1.append(Visualization.objects.filter(refer_hp=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_refer_hyg1.append(Visualization.objects.filter(refer_hyg=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=i.id).count())
                            teen_refer_hyg_male1.append(Visualization.objects.filter(refer_hyg=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_hyg_female1.append(Visualization.objects.filter(refer_hyg=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_refer_dent1.append(Visualization.objects.filter(refer_dent=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_dent_male1.append(Visualization.objects.filter(refer_dent=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_dent_female1.append(Visualization.objects.filter(refer_dent=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_refer_dr1.append(Visualization.objects.filter(refer_dr=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_dr_male1.append(Visualization.objects.filter(refer_dr=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_dr_female1.append(Visualization.objects.filter(refer_dr=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_refer_other1.append(Visualization.objects.filter(refer_other=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_other_male1.append(Visualization.objects.filter(refer_other=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_refer_other_female1.append(Visualization.objects.filter(refer_other=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            teen_sdf_whole_mouth1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(12,19),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            teen_sdf_whole_mouth_male1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            teen_sdf_whole_mouth_female1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(12,19),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_encounter1.append(Visualization.objects.filter(age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_encounter_male1.append(Visualization.objects.filter(age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_encounter_female1.append(Visualization.objects.filter(age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_exo1.append(Visualization.objects.filter(exo=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_exo_male1.append(Visualization.objects.filter(exo=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_exo_female1.append(Visualization.objects.filter(exo=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_art1.append(Visualization.objects.filter(art=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_art_male1.append(Visualization.objects.filter(art=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_art_female1.append(Visualization.objects.filter(art=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_seal1.append(Visualization.objects.filter(seal=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_seal_male1.append(Visualization.objects.filter(seal=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_seal_female1.append(Visualization.objects.filter(seal=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_sdf1.append(Visualization.objects.filter(sdf=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_sdf_male1.append(Visualization.objects.filter(sdf=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_sdf_female1.append(Visualization.objects.filter(sdf=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_fv1.append(Visualization.objects.filter(fv=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_fv_male1.append(Visualization.objects.filter(fv=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_fv_female1.append(Visualization.objects.filter(fv=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_health_post1.append(Visualization.objects.filter(refer_hp=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_health_post_male1.append(Visualization.objects.filter(refer_hp=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_health_post_female1.append(Visualization.objects.filter(refer_hp=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_refer_hyg1.append(Visualization.objects.filter(refer_hyg=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_hyg_male1.append(Visualization.objects.filter(refer_hyg=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_hyg_female1.append(Visualization.objects.filter(refer_hyg=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_refer_dent1.append(Visualization.objects.filter(refer_dent=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_dent_male1.append(Visualization.objects.filter(refer_dent=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_dent_female1.append(Visualization.objects.filter(refer_dent=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_refer_dr1.append(Visualization.objects.filter(refer_dr=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_dr_male1.append(Visualization.objects.filter(refer_dr=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_dr_female1.append(Visualization.objects.filter(refer_dr=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_refer_other1.append(Visualization.objects.filter(refer_other=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_other_male1.append(Visualization.objects.filter(refer_other=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_refer_other_female1.append(Visualization.objects.filter(refer_other=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            adult_sdf_whole_mouth1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(19,61),created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            adult_sdf_whole_mouth_male1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            adult_sdf_whole_mouth_female1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__range=(19,61),created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())


                            old_encounter1.append(Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_encounter_male1.append(Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_encounter_female1.append(Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_exo1.append(Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_exo_male1.append(Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_exo_female1.append(Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_art1.append(Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_art_male1.append(Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_art_female1.append(Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_seal1.append(Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_seal_male1.append(Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_seal_female1.append(Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_sdf1.append(Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_sdf_male1.append(Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_sdf_female1.append(Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_fv1.append(Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_fv_male1.append(Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_fv_female1.append(Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_health_post1.append(Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_health_post_male1.append(Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_health_post_female1.append(Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_refer_hyg1.append(Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_hyg_male1.append(Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_hyg_female1.append(Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_refer_dent1.append(Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_dent_male1.append(Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_dent_female1.append(Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_dr1.append(Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_dr_male1.append(Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_dr_female1.append(Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_other1.append(Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_other_male1.append(Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_refer_other_female1.append(Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())

                            old_sdf_whole_mouth1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location.id).filter(activities_id=i.id).count())
                            old_sdf_whole_mouth_male1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],gender="male",geography_id=location.id).filter(activities_id=i.id).count())
                            old_sdf_whole_mouth_female1.append(Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],gender="female",geography_id=location.id).filter(activities_id=i.id).count())
                        kid_encounter.append(sum(kid_encounter1))
                        kid_encounter_male.append(sum(kid_encounter_male1))
                        kid_encounter_female.append(sum(kid_encounter_female1))

                        kid_exo.append(sum(kid_exo1))
                        kid_exo_male.append(sum(kid_exo_male1))
                        kid_exo_female.append(sum(kid_exo_female1))

                        kid_art.append(sum(kid_art1))
                        kid_art_male.append(sum(kid_art_male1))
                        kid_art_female.append(sum(kid_art_female1))

                        kid_seal.append(sum(kid_seal1))
                        kid_seal_male.append(sum(kid_seal_male1))
                        kid_seal_female.append(sum(kid_seal_female1))

                        kid_sdf.append(sum(kid_sdf1))
                        kid_sdf_male.append(sum(kid_sdf_male1))
                        kid_sdf_female.append(sum(kid_sdf_female1))

                        kid_sdf_whole_mouth.append(sum(kid_sdf_whole_mouth1))
                        kid_sdf_whole_mouth_male.append(sum(kid_sdf_whole_mouth_male1))
                        kid_sdf_whole_mouth_female.append(sum(kid_sdf_whole_mouth_female1))

                        kid_fv.append(sum(kid_fv1))
                        kid_fv_male.append(sum(kid_fv_male1))
                        kid_fv_female.append(sum(kid_fv_female1))

                        kid_health_post.append(sum(kid_health_post1))
                        kid_health_post_male.append(sum(kid_health_post_male1))
                        kid_health_post_female.append(sum(kid_health_post_female1))

                        kid_refer_hyg.append(sum(kid_refer_hyg1))
                        kid_refer_hyg_male.append(sum(kid_refer_hyg_male1))
                        kid_refer_hyg_female.append(sum(kid_refer_hyg_female1))

                        kid_refer_dent.append(sum(kid_refer_dent1))
                        kid_refer_dent_male.append(sum(kid_refer_dent_male1))
                        kid_refer_dent_female.append(sum(kid_refer_dent_female1))

                        kid_refer_dr.append(sum(kid_refer_dr1))
                        kid_refer_dr_male.append(sum(kid_refer_dr_male1))
                        kid_refer_dr_female.append(sum(kid_refer_dr_female1))

                        kid_refer_other.append(sum(kid_refer_other))
                        kid_refer_other_male.append(sum(kid_refer_other_male1))
                        kid_refer_other_female.append(sum(kid_refer_other_female1))


                        teen_encounter.append(sum(teen_encounter1))
                        teen_encounter_male.append(sum(teen_encounter_male1))
                        teen_encounter_female.append(sum(teen_encounter_female1))

                        teen_exo.append(sum(teen_exo1))
                        teen_exo_male.append(sum(teen_exo_male1))
                        teen_exo_female.append(sum(teen_exo_female1))

                        teen_art.append(sum(teen_art1))
                        teen_art_male.append(sum(teen_art_male1))
                        teen_art_female.append(sum(teen_art_female1))

                        teen_seal.append(sum(teen_seal1))
                        teen_seal_male.append(sum(teen_seal_male1))
                        teen_seal_female.append(sum(teen_seal_female1))

                        teen_sdf.append(sum(teen_sdf1))
                        teen_sdf_male.append(sum(teen_sdf_male1))
                        teen_sdf_female.append(sum(teen_sdf_female1))

                        teen_sdf_whole_mouth.append(sum(teen_sdf_whole_mouth1))
                        teen_sdf_whole_mouth_male.append(sum(teen_sdf_whole_mouth_male1))
                        teen_sdf_whole_mouth_female.append(sum(teen_sdf_whole_mouth_female1))

                        teen_fv.append(sum(teen_fv1))
                        teen_fv_male.append(sum(teen_fv_male1))
                        teen_fv_female.append(sum(teen_fv_female1))

                        teen_health_post.append(sum(teen_health_post1))
                        teen_health_post_male.append(sum(teen_health_post_male1))
                        teen_health_post_female.append(sum(teen_health_post_female1))

                        teen_refer_hyg.append(sum(teen_refer_hyg1))
                        teen_refer_hyg_male.append(sum(teen_refer_hyg_male1))
                        teen_refer_hyg_female.append(sum(teen_refer_hyg_female1))

                        teen_refer_dent.append(sum(teen_refer_dent1))
                        teen_refer_dent_male.append(sum(teen_refer_dent_male1))
                        teen_refer_dent_female.append(sum(teen_refer_dent_female1))

                        teen_refer_dr.append(sum(teen_refer_dr1))
                        teen_refer_dr_male.append(sum(teen_refer_dr_male1))
                        teen_refer_dr_female.append(sum(teen_refer_dr_female1))

                        teen_refer_other.append(sum(teen_refer_other))
                        teen_refer_other_male.append(sum(teen_refer_other_male1))
                        teen_refer_other_female.append(sum(teen_refer_other_female1))

                        adult_encounter.append(sum(adult_encounter1))
                        adult_encounter_male.append(sum(adult_encounter_male1))
                        adult_encounter_female.append(sum(adult_encounter_female1))

                        adult_exo.append(sum(adult_exo1))
                        adult_exo_male.append(sum(adult_exo_male1))
                        adult_exo_female.append(sum(adult_exo_female1))

                        adult_art.append(sum(adult_art1))
                        adult_art_male.append(sum(adult_art_male1))
                        adult_art_female.append(sum(adult_art_female1))

                        adult_seal.append(sum(adult_seal1))
                        adult_seal_male.append(sum(adult_seal_male1))
                        adult_seal_female.append(sum(adult_seal_female1))

                        adult_sdf.append(sum(adult_sdf1))
                        adult_sdf_male.append(sum(adult_sdf_male1))
                        adult_sdf_female.append(sum(adult_sdf_female1))

                        adult_sdf_whole_mouth.append(sum(adult_sdf_whole_mouth1))
                        adult_sdf_whole_mouth_male.append(sum(adult_sdf_whole_mouth_male1))
                        adult_sdf_whole_mouth_female.append(sum(adult_sdf_whole_mouth_female1))

                        adult_fv.append(sum(adult_fv1))
                        adult_fv_male.append(sum(adult_fv_male1))
                        adult_fv_female.append(sum(adult_fv_female1))

                        adult_health_post.append(sum(adult_health_post1))
                        adult_health_post_male.append(sum(adult_health_post_male1))
                        adult_health_post_female.append(sum(adult_health_post_female1))

                        adult_refer_hyg.append(sum(adult_refer_hyg1))
                        adult_refer_hyg_male.append(sum(adult_refer_hyg_male1))
                        adult_refer_hyg_female.append(sum(adult_refer_hyg_female1))

                        adult_refer_dent.append(sum(adult_refer_dent1))
                        adult_refer_dent_male.append(sum(adult_refer_dent_male1))
                        adult_refer_dent_female.append(sum(adult_refer_dent_female1))

                        adult_refer_dr.append(sum(adult_refer_dr1))
                        adult_refer_dr_male.append(sum(adult_refer_dr_male1))
                        adult_refer_dr_female.append(sum(adult_refer_dr_female1))

                        adult_refer_other.append(sum(adult_refer_other))
                        adult_refer_other_male.append(sum(adult_refer_other_male1))
                        adult_refer_other_female.append(sum(adult_refer_other_female1))

                        old_encounter.append(sum(old_encounter1))
                        old_encounter_male.append(sum(old_encounter_male1))
                        old_encounter_female.append(sum(old_encounter_female1))

                        old_exo.append(sum(old_exo1))
                        old_exo_male.append(sum(old_exo_male1))
                        old_exo_female.append(sum(old_exo_female1))

                        old_art.append(sum(old_art1))
                        old_art_male.append(sum(old_art_male1))
                        old_art_female.append(sum(old_art_female1))

                        old_seal.append(sum(old_seal1))
                        old_seal_male.append(sum(old_seal_male1))
                        old_seal_female.append(sum(old_seal_female1))

                        old_sdf.append(sum(old_sdf1))
                        old_sdf_male.append(sum(old_sdf_male1))
                        old_sdf_female.append(sum(old_sdf_female1))

                        old_sdf_whole_mouth.append(sum(old_sdf_whole_mouth1))
                        old_sdf_whole_mouth_male.append(sum(old_sdf_whole_mouth_male1))
                        old_sdf_whole_mouth_female.append(sum(old_sdf_whole_mouth_female1))

                        old_fv.append(sum(old_fv1))
                        old_fv_male.append(sum(old_fv_male1))
                        old_fv_female.append(sum(old_fv_female1))

                        old_health_post.append(sum(old_health_post1))
                        old_health_post_male.append(sum(old_health_post_male1))
                        old_health_post_female.append(sum(old_health_post_female1))

                        old_refer_hyg.append(sum(old_refer_hyg1))
                        old_refer_hyg_male.append(sum(old_refer_hyg_male1))
                        old_refer_hyg_female.append(sum(old_refer_hyg_female1))

                        old_refer_dent.append(sum(old_refer_dent1))
                        old_refer_dent_male.append(sum(old_refer_dent_male1))
                        old_refer_dent_female.append(sum(old_refer_dent_female1))

                        old_refer_dr.append(sum(old_refer_dr1))
                        old_refer_dr_male.append(sum(old_refer_dr_male1))
                        old_refer_dr_female.append(sum(old_refer_dr_female1))

                        old_refer_other.append(sum(old_refer_other))
                        old_refer_other_male.append(sum(old_refer_other_male1))
                        old_refer_other_female.append(sum(old_refer_other_female1))

                total_encounter.append((sum(kid_encounter)+sum(teen_encounter)+sum(adult_encounter)+sum(old_encounter)))
                total_exo.append((sum(kid_exo)+sum(teen_exo)+sum(adult_exo)+sum(old_exo)))
                total_art.append((sum(kid_art)+sum(teen_art)+sum(adult_art)+sum(old_art)))
                total_seal.append((sum(kid_seal)+sum(teen_seal)+sum(adult_seal)+sum(old_seal)))
                total_sdf.append((sum(kid_sdf)+sum(teen_sdf)+sum(adult_sdf)+sum(old_sdf)))
                total_sdf_whole_mouth.append((sum(kid_sdf_whole_mouth)+sum(teen_sdf_whole_mouth)+sum(adult_sdf_whole_mouth)+sum(old_sdf_whole_mouth)))
                total_fv.append((sum(kid_fv)+sum(teen_fv)+sum(adult_fv)+sum(old_fv)))
                total_health_post.append((sum(kid_health_post)+sum(teen_health_post)+sum(adult_health_post)+sum(old_health_post)))
                total_refer_hyg.append((sum(kid_refer_hyg)+sum(teen_refer_hyg)+sum(adult_refer_hyg)+sum(old_refer_hyg)))
                total_refer_dent.append((sum(kid_refer_dent)+sum(teen_refer_dent)+sum(adult_refer_dent)+sum(old_refer_dent)))
                total_refer_dr.append((sum(kid_refer_dr)+sum(teen_refer_dr)+sum(adult_refer_dr)+sum(old_refer_dr)))
                total_refer_other.append((sum(kid_refer_other)+sum(teen_refer_other)+sum(adult_refer_other)+sum(old_refer_other)))

                return Response([["Kids (< 12)",sum(kid_encounter), sum(kid_exo), sum(kid_art), sum(kid_seal), sum(kid_sdf), sum(kid_sdf_whole_mouth), sum(kid_fv), sum(kid_health_post), sum(kid_refer_hyg), sum(kid_refer_dent), sum(kid_refer_dr), sum(kid_refer_other)],\
                ['<span class="ml-4">Male</span>', sum(kid_encounter_male), sum(kid_exo_male), sum(kid_art_male), sum(kid_seal_male), sum(kid_sdf_male), sum(kid_sdf_whole_mouth_male), sum(kid_fv_male), sum(kid_health_post_male), sum(kid_refer_hyg_male), sum(kid_refer_dent_male), sum(kid_refer_dr_male), sum(kid_refer_other_male),'secondary'],\
                ['<span class="ml-4">Female</span>',sum(kid_encounter_female), sum(kid_exo_female), sum(kid_art_female), sum(kid_seal_female), sum(kid_sdf_female), sum(kid_sdf_whole_mouth_female), sum(kid_fv_female), sum(kid_health_post_female), sum(kid_refer_hyg_female), sum(kid_refer_dent_female), sum(kid_refer_dr_female) ,sum(kid_refer_other_female),'secondary'],\
                ["Teens (12-18)",sum(teen_encounter), sum(teen_exo), sum(teen_art), sum(teen_seal), sum(teen_sdf), sum(teen_sdf_whole_mouth), sum(teen_fv), sum(teen_health_post), sum(teen_refer_hyg), sum(teen_refer_dent), sum(teen_refer_dr), sum(teen_refer_other)],\
                ['<span class="ml-4">Male</span>', sum(teen_encounter_male), sum(teen_exo_male), sum(teen_art_male), sum(teen_seal_male), sum(teen_sdf_male), sum(teen_sdf_whole_mouth_male), sum(teen_fv_male), sum(teen_health_post_male), sum(teen_refer_hyg_male), sum(teen_refer_dent_male), sum(teen_refer_dr_male), sum(teen_refer_other_male),'secondary'],\
                ['<span class="ml-4">Female</span>',sum(teen_encounter_female), sum(teen_exo_female), sum(teen_art_female), sum(teen_seal_female), sum(teen_sdf_female), sum(teen_sdf_whole_mouth_female), sum(teen_fv_female), sum(teen_health_post_female), sum(teen_refer_hyg_female), sum(teen_refer_dent_female), sum(teen_refer_dr_female),sum(teen_refer_other_female),'secondary'],\

                ["Adults (19-60)", sum(adult_encounter), sum(adult_exo), sum(adult_art),sum(adult_seal), sum(adult_sdf), sum(adult_sdf_whole_mouth), sum(adult_fv), sum(adult_health_post), sum(adult_refer_hyg), sum(adult_refer_dent),sum(adult_refer_dr), sum(adult_refer_other)],\
                ['<span class="ml-4">Male</span>',sum(adult_encounter_male), sum(adult_exo_male), sum(adult_art_male), sum(adult_seal_male), sum(adult_sdf_male), sum(adult_sdf_whole_mouth_male), sum(adult_fv_male), sum(adult_health_post_male), sum(adult_refer_hyg_male), sum(adult_refer_dent_male), sum(adult_refer_dr_male), sum(adult_refer_other_male),'secondary'],\
                ['<span class="ml-4">Female</span>',sum(adult_encounter_female), sum(adult_exo_female), sum(adult_art_female), sum(adult_seal_female), sum(adult_sdf_female), sum(adult_sdf_whole_mouth_female), sum(adult_fv_female), sum(adult_health_post_female), sum(adult_refer_hyg_female), sum(adult_refer_dent_female), sum(adult_refer_dr_female), sum(adult_refer_other_female),'secondary'],\
                ["Older Adults (> 60)",sum(old_encounter),sum(old_exo), sum(old_art), sum(old_seal), sum(old_sdf), sum(old_sdf_whole_mouth), sum(old_fv), sum(old_health_post), sum(old_refer_hyg), sum(old_refer_dent),sum(old_refer_dr), sum(old_refer_other)],\
                ['<span class="ml-4">Male</span>',sum(old_encounter_male), sum(old_exo_male),sum(old_art_male), sum(old_seal_male),sum(old_sdf_male), sum(old_sdf_whole_mouth_male), sum(old_fv_male), sum(old_health_post_male), sum(old_refer_hyg_male), sum(old_refer_dent_male), sum(old_refer_dr_male),sum(old_refer_other_male),'secondary'],\
                ['<span class="ml-4">Female</span>',sum(old_encounter_female), sum(old_exo_female), sum(old_art_female), sum(old_seal_female), sum(old_sdf_female), sum(old_sdf_whole_mouth_female), sum(old_fv_female), sum(old_health_post_female), sum(old_refer_hyg_female), sum(old_refer_dent_female), sum(old_refer_dr_female),sum(old_refer_other_female),'secondary'],\
                ["Total",sum(total_encounter), sum(total_exo), sum(total_art), sum(total_seal), sum(total_sdf), sum(total_sdf_whole_mouth), sum(total_fv), sum(total_health_post), sum(total_refer_hyg), sum(total_refer_dent), sum(total_refer_dr), sum(total_refer_other)]])
            return Response({"message":"End date must be greated then Start Date"},status=400)
        return Response({"message":serializer.errors},status=400)


class TreatmentActivityList(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = OverViewVisualization
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            health_post_obj = Activity.objects.get(name="Health Post")
            seminar_obj = Activity.objects.get(name="School Seminar")
            outreach_obj = Activity.objects.get(name="Community Outreach")
            training = Activity.objects.get(name="Training")
            health_post_check = Visualization.objects.filter(activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_exo = Visualization.objects.filter(exo=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_art = Visualization.objects.filter(art=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_seal = Visualization.objects.filter(seal=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_sdf = Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_fv = Visualization.objects.filter(fv=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_refer_hp = Visualization.objects.filter(refer_hp=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_refer_hyg = Visualization.objects.filter(refer_hyg=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_refer_dent = Visualization.objects.filter(refer_dent=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_refer_dr = Visualization.objects.filter(refer_dr=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            health_post_refer_other = Visualization.objects.filter(refer_other=True,activities_id=health_post_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()

            seminar_check = Visualization.objects.filter(activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_exo = Visualization.objects.filter(exo=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_art = Visualization.objects.filter(art=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_seal = Visualization.objects.filter(seal=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_sdf = Visualization.objects.filter(sdf=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_fv = Visualization.objects.filter(fv=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=seminar_obj.id).count()
            seminar_refer_hp = Visualization.objects.filter(refer_hp=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_refer_hyg = Visualization.objects.filter(refer_hyg=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_refer_dent = Visualization.objects.filter(refer_dent=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_refer_dr = Visualization.objects.filter(refer_dr=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seminar_refer_other = Visualization.objects.filter(refer_other=True,activities_id=seminar_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()

            outreach_check = Visualization.objects.filter(activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_exo = Visualization.objects.filter(exo=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_art = Visualization.objects.filter(art=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_seal = Visualization.objects.filter(seal=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_sdf = Visualization.objects.filter(sdf=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_fv = Visualization.objects.filter(fv=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_refer_hp = Visualization.objects.filter(refer_hp=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_refer_hyg = Visualization.objects.filter(refer_hyg=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_refer_dent = Visualization.objects.filter(refer_dent=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_refer_dr = Visualization.objects.filter(refer_dr=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            outreach_refer_other = Visualization.objects.filter(refer_other=True,activities_id=outreach_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()

            training_check = Visualization.objects.filter(activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_exo = Visualization.objects.filter(exo=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_art = Visualization.objects.filter(art=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_seal = Visualization.objects.filter(seal=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_sdf = Visualization.objects.filter(sdf=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_fv = Visualization.objects.filter(fv=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_refer_hp = Visualization.objects.filter(refer_hp=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_refer_hyg = Visualization.objects.filter(refer_hyg=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_refer_dent = Visualization.objects.filter(refer_dent=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_refer_dr = Visualization.objects.filter(refer_dr=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            training_refer_other = Visualization.objects.filter(refer_other=True,activities_id=training.id,created_at__range=[last_30_days_obj,today_date_obj]).count()



            return Response([
            ["Clinic",health_post_check, health_post_exo, health_post_art, health_post_seal, health_post_sdf,health_post_sdf_whole_mouth, health_post_fv, health_post_refer_hp, health_post_refer_hyg,health_post_refer_dent,health_post_refer_dr,health_post_refer_other], \
            ["Seminar",seminar_check,seminar_exo, seminar_art, seminar_seal, seminar_sdf, seminar_sdf_whole_mouth, seminar_fv, seminar_refer_hp, seminar_refer_hyg, seminar_refer_dent, seminar_refer_dr, seminar_refer_other], \
            ["Outreach",outreach_check,outreach_exo, outreach_art, outreach_seal, outreach_sdf, outreach_sdf_whole_mouth, outreach_fv, outreach_refer_hp, outreach_refer_hyg, outreach_refer_dent, outreach_refer_dr, outreach_refer_other], \
            ["Training",training_check, training_exo, training_art, training_seal, training_sdf, training_sdf_whole_mouth, training_fv, training_refer_hp, training_refer_hyg, training_refer_dent, training_refer_dr, training_refer_other]])
        return Response({"treatment_obj":"do not have a permission"},status=400)

    def post(self, request, format=None):
        serializer = OverViewVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location_list = serializer.validated_data['location']
            activities = serializer.validated_data['activities']

            if(end_date > start_date):
                data=[]
                if not location_list:
                    for i in activities:
                        activities_name = []
                        activities_name.append(i.name.capitalize())
                        activities_name.append(Visualization.objects.filter(activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(exo=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(art=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(seal=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(sdf=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(sdf_whole_mouth=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(fv=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(refer_hp=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(refer_hyg=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(refer_dent=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(refer_dr=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        activities_name.append(Visualization.objects.filter(refer_other=True,activities_id=i.id,created_at__range=[start_date,end_date]).count())
                        data.append(activities_name)
                else:
                    for i in activities:
                        activities_data = []
                        activities_check = []
                        activities_exo = []
                        activities_art = []
                        activities_seal = []
                        activities_sdf = []
                        activities_sdf_whole_mouth = []
                        activities_fv = []
                        activities_refer_hp = []
                        activities_refer_hyg = []
                        activities_refer_dent = []
                        activities_refer_dr = []
                        activities_refer_other = []
                        for location in location_list:
                            activities_check.append(Visualization.objects.filter(activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_exo.append(Visualization.objects.filter(exo=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_art.append(Visualization.objects.filter(art=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_seal.append(Visualization.objects.filter(seal=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_sdf.append(Visualization.objects.filter(sdf=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_sdf_whole_mouth.append(Visualization.objects.filter(sdf_whole_mouth=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_fv.append(Visualization.objects.filter(fv=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_refer_hp.append(Visualization.objects.filter(refer_hp=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_refer_hyg.append(Visualization.objects.filter(refer_hyg=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_refer_dent.append(Visualization.objects.filter(refer_dent=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_refer_dr.append(Visualization.objects.filter(refer_dr=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                            activities_refer_other.append(Visualization.objects.filter(refer_other=True,activities_id=i.id,created_at__range=[start_date,end_date],geography_id=location.id).count())
                        activities_data.append(i.name.capitalize())
                        activities_data.append(sum(activities_check))
                        activities_data.append(sum(activities_exo))
                        activities_data.append(sum(activities_art))
                        activities_data.append(sum(activities_seal))
                        activities_data.append(sum(activities_sdf))
                        activities_data.append(sum(activities_sdf_whole_mouth))
                        activities_data.append(sum(activities_fv))
                        activities_data.append(sum(activities_refer_hp))
                        activities_data.append(sum(activities_refer_hyg))
                        activities_data.append(sum(activities_refer_dent))
                        activities_data.append(sum(activities_refer_dr))
                        activities_data.append(sum(activities_refer_other))
                        data.append(activities_data)
                return Response(data)
            return Response({"message":"End date must be greated then Start Date"},status=400)
        return Response({"treatment_obj":"do not have a permission"},status=400)

class TreatmentbyWardList(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = OverViewVisualization
    def get(self, request, format=None):
        list_data=[]
        for war_obj in Ward.objects.filter(status=True):
            loop_data=[]
            check = Visualization.objects.filter(geography_id=war_obj.id,created_at__range=[last_30_days_obj,today_date_obj]).count()
            exo = Visualization.objects.filter(geography_id=war_obj.id,exo=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            art = Visualization.objects.filter(geography_id=war_obj.id,art=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            seal = Visualization.objects.filter(geography_id=war_obj.id,seal=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sdf = Visualization.objects.filter(geography_id=war_obj.id,sdf=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            fv = Visualization.objects.filter(geography_id=war_obj.id,fv=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            sdf_whole_mouth = Visualization.objects.filter(geography_id=war_obj.id,sdf_whole_mouth=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_hp = Visualization.objects.filter(geography_id=war_obj.id,refer_hp=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_hyg = Visualization.objects.filter(geography_id=war_obj.id,refer_hyg=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_dent = Visualization.objects.filter(geography_id=war_obj.id,refer_dent=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_dr = Visualization.objects.filter(geography_id=war_obj.id,refer_dr=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            refer_other = Visualization.objects.filter(geography_id=war_obj.id,refer_other=True,created_at__range=[last_30_days_obj,today_date_obj]).count()
            loop_data.append(war_obj.name)
            loop_data.append(check)
            loop_data.append(exo)
            loop_data.append(art)
            loop_data.append(seal)
            loop_data.append(sdf)
            loop_data.append(sdf_whole_mouth)
            loop_data.append(fv)
            loop_data.append(refer_hp)
            loop_data.append(refer_hyg)
            loop_data.append(refer_dent)
            loop_data.append(refer_dr)
            loop_data.append(refer_other)
            list_data.append(loop_data)
        return Response(list_data)

    def post(self, request, format=None):
        serializer = OverViewVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location_list = serializer.validated_data['location']
            activities = serializer.validated_data['activities']
            list_data=[]
            check=[]
            exo=[]
            art = []
            seal = []
            sdf = []
            fv = []
            sdf_whole_mouth = []
            refer_hp = []
            refer_hyg = []
            refer_dent = []
            refer_dr = []
            refer_other = []
            if (end_date > start_date):
                if not location_list:
                    for war_obj1 in Ward.objects.filter(status=True):
                        loop_data=[]
                        check_obj=[]
                        exo_obj=[]
                        art_obj = []
                        seal_obj = []
                        sdf_obj = []
                        fv_obj = []
                        sdf_whole_mouth_obj = []
                        refer_hp_obj = []
                        refer_hyg_obj = []
                        refer_dent_obj = []
                        refer_dr_obj = []
                        refer_other_obj = []
                        for i in activities:
                            check_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id, created_at__range=[start_date,end_date]).count())
                            exo_obj.append(Visualization.objects.filter(geography_id=war_obj1.id, activities_id=i.id,exo=True,created_at__range=[start_date,end_date]).count())
                            art_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,art=True,created_at__range=[start_date,end_date]).count())
                            seal_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,seal=True,created_at__range=[start_date,end_date]).count())
                            sdf_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,sdf=True,created_at__range=[start_date,end_date]).count())
                            fv_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,fv=True,created_at__range=[start_date,end_date]).count())
                            sdf_whole_mouth_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,sdf_whole_mouth=True,created_at__range=[start_date,end_date]).count())
                            refer_hp_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,refer_hp=True,created_at__range=[start_date,end_date]).count())
                            refer_hyg_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,refer_hyg=True,created_at__range=[start_date,end_date]).count())
                            refer_dent_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,refer_dent=True,created_at__range=[start_date,end_date]).count())
                            refer_dr_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,refer_dr=True,created_at__range=[start_date,end_date]).count())
                            refer_other_obj.append(Visualization.objects.filter(geography_id=war_obj1.id,activities_id=i.id,refer_other=True,created_at__range=[start_date,end_date]).count())
                        loop_data.append(war_obj1.name.capitalize())
                        loop_data.append(sum(check_obj))
                        loop_data.append(sum(exo_obj))
                        loop_data.append(sum(art_obj))
                        loop_data.append(sum(seal_obj))
                        loop_data.append(sum(sdf_obj))
                        loop_data.append(sum(fv_obj))
                        loop_data.append(sum(sdf_whole_mouth_obj))
                        loop_data.append(sum(refer_hp_obj))
                        loop_data.append(sum(refer_hyg_obj))
                        loop_data.append(sum(refer_dent_obj))
                        loop_data.append(sum(refer_dr_obj))
                        loop_data.append(sum(refer_other_obj))
                        list_data.append(loop_data)

                else:
                    for location in location_list:
                        loop_data = []
                        location_check = []
                        location_exo = []
                        location_art = []
                        location_seal = []
                        location_sdf = []
                        location_sdf_whole_mouth = []
                        location_fv = []
                        location_refer_hp = []
                        location_refer_hyg = []
                        location_refer_dent = []
                        location_refer_dr = []
                        location_refer_other = []
                        for i in activities:
                            location_check.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id, created_at__range=[start_date,end_date]).count())
                            location_exo.append(Visualization.objects.filter(geography_id=location.id, activities_id=i.id,exo=True,created_at__range=[start_date,end_date]).count())
                            location_art.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,art=True,created_at__range=[start_date,end_date]).count())
                            location_seal.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,seal=True,created_at__range=[start_date,end_date]).count())
                            location_sdf.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,sdf=True,created_at__range=[start_date,end_date]).count())
                            location_fv.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,fv=True,created_at__range=[start_date,end_date]).count())
                            location_sdf_whole_mouth.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,sdf_whole_mouth=True,created_at__range=[start_date,end_date]).count())
                            location_refer_hp.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,refer_hp=True,created_at__range=[start_date,end_date]).count())
                            location_refer_hyg.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,refer_hyg=True,created_at__range=[start_date,end_date]).count())
                            location_refer_dent.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,refer_dent=True,created_at__range=[start_date,end_date]).count())
                            location_refer_dr.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,refer_dr=True,created_at__range=[start_date,end_date]).count())
                            location_refer_other.append(Visualization.objects.filter(geography_id=location.id,activities_id=i.id,refer_other=True,created_at__range=[start_date,end_date]).count())
                        loop_data.append(location.name.capitalize())
                        loop_data.append(sum(location_check))
                        loop_data.append(sum(location_exo))
                        loop_data.append(sum(location_art))
                        loop_data.append(sum(location_seal))
                        loop_data.append(sum(location_sdf))
                        loop_data.append(sum(location_sdf_whole_mouth))
                        loop_data.append(sum(location_fv))
                        loop_data.append(sum(location_refer_hp))
                        loop_data.append(sum(location_refer_hyg))
                        loop_data.append(sum(location_refer_dent))
                        loop_data.append(sum(location_refer_dr))
                        loop_data.append(sum(location_refer_other))
                        list_data.append(loop_data)
                return Response(list_data)
            return Response({"message":"End date must be greated then Start Date"},status=400)
        return Response({"treatment_obj":"do not have a permission"},status=400)










class DateReturn(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        return Response({"today_date":today_date,"last_30_days":last_30_days,"location":"All Location"})
