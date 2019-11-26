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
from django.db.models import Count
logger = logging.getLogger(__name__)


np_date = NepaliDate()
d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
lessthan18 = d - datetime.timedelta(days=365*18)
greaterthan60 = d - datetime.timedelta(days=365*60)


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class OverviewVisualization1(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = OverViewVisualization
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            total_encounter = Visualization.objects.all().count()
            total_exo = Visualization.objects.filter(exo=True).count()
            total_art = Visualization.objects.filter(art=True).count()
            total_seal = Visualization.objects.filter(seal=True).count()
            total_sdf = Visualization.objects.filter(sdf=True).count()
            total_fv = Visualization.objects.filter(fv=True).count()
            total_health_post = Visualization.objects.filter(refer_hp=True).count()
            total_refer_hyg = Visualization.objects.filter(refer_hyg=True).count()
            total_refer_dent = Visualization.objects.filter(refer_dent=True).count()
            total_refer_dr = Visualization.objects.filter(refer_dr=True).count()
            total_refer_other = Visualization.objects.filter(refer_other=True).count()
            total_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True).count()


            kid_encounter_male = Visualization.objects.filter(age__lt=18,gender="male").count()
            kid_encounter_female = Visualization.objects.filter(age__lt=18,gender="female").count()

            kid_exo_male = Visualization.objects.filter(age__lt=18,exo=True,gender="male").count()
            kid_exo_female = Visualization.objects.filter(age__lt=18,exo=True,gender="female").count()

            kid_art_male = Visualization.objects.filter(age__lt=18,art=True,gender="male").count()
            kid_art_female = Visualization.objects.filter(age__lt=18,art=True,gender="female").count()

            kid_seal_male = Visualization.objects.filter(age__lt=18,seal=True,gender="male").count()
            kid_seal_female = Visualization.objects.filter(age__lt=18,seal=True,gender="female").count()

            kid_sdf_male = Visualization.objects.filter(age__lt=18,sdf=True,gender="male").count()
            kid_sdf_female = Visualization.objects.filter(age__lt=18,sdf=True,gender="female").count()

            kid_fv_male = Visualization.objects.filter(age__lt=18,fv=True,gender="male").count()
            kid_fv_female = Visualization.objects.filter(age__lt=18,fv=True,gender="female").count()

            kid_health_post_male = Visualization.objects.filter(age__lt=18,refer_hp=True,gender="male").count()
            kid_health_post_female = Visualization.objects.filter(age__lt=18,refer_hp=True,gender="female").count()

            kid_refer_hyg_male = Visualization.objects.filter(age__lt=18,refer_hyg=True,gender="male").count()
            kid_refer_hyg_female = Visualization.objects.filter(age__lt=18,refer_hyg=True,gender="female").count()

            kid_refer_dent_male = Visualization.objects.filter(age__lt=18,refer_dent=True,gender="male").count()
            kid_refer_dent_female = Visualization.objects.filter(age__lt=18,refer_dent=True,gender="female").count()

            kid_refer_dr_male = Visualization.objects.filter(age__lt=18,refer_dr=True,gender="male").count()
            kid_refer_dr_female = Visualization.objects.filter(age__lt=18,refer_dr=True,gender="female").count()

            kid_refer_other_male = Visualization.objects.filter(age__lt=18,refer_other=True,gender="male").count()
            kid_refer_other_female = Visualization.objects.filter(age__lt=18,refer_other=True,gender="female").count()

            kid_sdf_whole_mouth_male = Visualization.objects.filter(age__lt=18,sdf_whole_mouth=True,gender="male").count()
            kid_sdf_whole_mouth_female = Visualization.objects.filter(age__lt=18,sdf_whole_mouth=True,gender="female").count()

            adult_encounter_male = Visualization.objects.filter(age__range=(18,60),gender="male").count()
            adult_encounter_female = Visualization.objects.filter(age__range=(18,60),gender="female").count()

            adult_exo_male = Visualization.objects.filter(age__range=(18,60),exo=True,gender="male").count()
            adult_exo_female = Visualization.objects.filter(age__range=(18,60),exo=True,gender="female").count()

            adult_art_male = Visualization.objects.filter(age__range=(18,60),art=True,gender="male").count()
            adult_art_female = Visualization.objects.filter(age__range=(18,60),art=True,gender="female").count()

            adult_seal_male = Visualization.objects.filter(age__range=(18,60),seal=True,gender="male").count()
            adult_seal_female = Visualization.objects.filter(age__range=(18,60),seal=True,gender="female").count()

            adult_sdf_male = Visualization.objects.filter(age__range=(18,60),sdf=True,gender="male").count()
            adult_sdf_female = Visualization.objects.filter(age__range=(18,60),sdf=True,gender="female").count()

            adult_fv_male = Visualization.objects.filter(age__range=(18,60),fv=True,gender="male").count()
            adult_fv_female = Visualization.objects.filter(age__range=(18,60),fv=True,gender="female").count()

            adult_health_post_male = Visualization.objects.filter(age__range=(18,60),refer_hp=True,gender="male").count()
            adult_health_post_female = Visualization.objects.filter(age__range=(18,60),refer_hp=True,gender="female").count()

            adult_refer_hyg_male = Visualization.objects.filter(age__range=(18,60),refer_hyg=True,gender="male").count()
            adult_refer_hyg_female = Visualization.objects.filter(age__range=(18,60),refer_hyg=True,gender="female").count()

            adult_refer_dent_male = Visualization.objects.filter(age__range=(18,60),refer_dent=True,gender="male").count()
            adult_refer_dent_female = Visualization.objects.filter(age__range=(18,60),refer_dent=True,gender="female").count()

            adult_refer_dr_male = Visualization.objects.filter(age__range=(18,60),refer_dr=True,gender="male").count()
            adult_refer_dr_female = Visualization.objects.filter(age__range=(18,60),refer_dr=True,gender="female").count()

            adult_refer_other_male = Visualization.objects.filter(age__range=(18,60),refer_other=True,gender="male").count()
            adult_refer_other_female = Visualization.objects.filter(age__range=(18,60),refer_other=True,gender="female").count()

            adult_sdf_whole_mouth_male = Visualization.objects.filter(age__range=(18,60),sdf_whole_mouth=True,gender="male").count()
            adult_sdf_whole_mouth_female = Visualization.objects.filter(age__range=(18,60),sdf_whole_mouth=True,gender="female").count()


            old_encounter_male = Visualization.objects.filter(age__gt=60,gender="male").count()
            old_encounter_female = Visualization.objects.filter(age__gt=60,gender="female").count()

            old_exo_male = Visualization.objects.filter(age__gt=60,exo=True,gender="male").count()
            old_exo_female = Visualization.objects.filter(age__gt=60,exo=True,gender="female").count()

            old_art_male = Visualization.objects.filter(age__gt=60,art=True,gender="male").count()
            old_art_female = Visualization.objects.filter(age__gt=60,art=True,gender="female").count()

            old_seal_male = Visualization.objects.filter(age__gt=60,seal=True,gender="male").count()
            old_seal_female = Visualization.objects.filter(age__gt=60,seal=True,gender="female").count()

            old_sdf_male = Visualization.objects.filter(age__gt=60,sdf=True,gender="male").count()
            old_sdf_female = Visualization.objects.filter(age__gt=60,sdf=True,gender="female").count()

            old_fv_male = Visualization.objects.filter(age__gt=60,fv=True,gender="male").count()
            old_fv_female = Visualization.objects.filter(age__gt=60,fv=True,gender="female").count()

            old_health_post_male = Visualization.objects.filter(age__gt=60,refer_hp=True,gender="male").count()
            old_health_post_female = Visualization.objects.filter(age__gt=60,refer_hp=True,gender="female").count()

            old_refer_hyg_male = Visualization.objects.filter(age__gt=60,refer_hyg=True,gender="male").count()
            old_refer_hyg_female = Visualization.objects.filter(age__gt=60,refer_hyg=True,gender="female").count()

            old_refer_dent_male = Visualization.objects.filter(age__gt=60,refer_dent=True,gender="male").count()
            old_refer_dent_female = Visualization.objects.filter(age__gt=60,refer_dent=True,gender="female").count()

            old_refer_dr_male = Visualization.objects.filter(age__gt=60,refer_dr=True,gender="male").count()
            old_refer_dr_female = Visualization.objects.filter(age__gt=60,refer_dr=True,gender="female").count()

            old_refer_other_male = Visualization.objects.filter(age__gt=60,refer_other=True,gender="male").count()
            old_refer_other_female = Visualization.objects.filter(age__gt=60,refer_other=True,gender="female").count()

            old_sdf_whole_mouth_male = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True,gender="male").count()
            old_sdf_whole_mouth_female = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True,gender="female").count()

            return Response([["Kids"],\
            ['<span class="ml-4">Male</span>',kid_encounter_male, kid_exo_male, kid_art_male, kid_seal_male, kid_sdf_male, kid_sdf_whole_mouth_male, kid_fv_male, kid_health_post_male, kid_refer_hyg_male, kid_refer_dent_male, kid_refer_dr_male,kid_refer_other_male],\
            ['<span class="ml-4">Female</span>',kid_encounter_female, kid_exo_female, kid_art_female, kid_seal_female, kid_sdf_female, kid_sdf_whole_mouth_female, kid_fv_female, kid_health_post_female, kid_refer_hyg_female, kid_refer_dent_female, kid_refer_dr_female ,kid_refer_other_female],\
            ["Adults"],\
            ['<span class="ml-4">Male</span>',adult_encounter_male, adult_exo_male, adult_art_male, adult_seal_male, adult_sdf_male, adult_sdf_whole_mouth_male, adult_fv_male, adult_health_post_male, adult_refer_hyg_male, adult_refer_dent_male, adult_refer_dr_male, adult_refer_other_male],\
            ['<span class="ml-4">Female</span>',adult_encounter_female, adult_exo_female, adult_art_female, adult_seal_female, adult_sdf_female, adult_sdf_whole_mouth_female, adult_fv_female, adult_health_post_female, adult_refer_hyg_female, adult_refer_dent_female, adult_refer_dr_female, adult_refer_other_female],\
            ["Older Adults"],\
            ['<span class="ml-4">Male</span>',old_encounter_male, old_exo_male,old_art_male, old_seal_male,old_sdf_male, old_sdf_whole_mouth_male, old_fv_male, old_health_post_male, old_refer_hyg_male, old_refer_dent_male, old_refer_dr_male,old_refer_other_male],\
            ['<span class="ml-4">Female</span>',old_encounter_female, old_exo_female,old_art_female, old_seal_female,old_sdf_female, old_sdf_whole_mouth_female,old_fv_female,old_health_post_female, old_refer_hyg_female, old_refer_dent_female, old_refer_dr_female,old_refer_other_female],\
            ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf, total_sdf_whole_mouth, total_fv,total_health_post, total_refer_hyg,total_refer_dent, total_refer_dr,total_refer_other]])
        return Response({"treatment_obj":"do not have a permission"},status=400)


    def post(self, request, format=None):
        serializer = OverViewVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']
            health_post = serializer.validated_data['health_post']
            seminar = serializer.validated_data['seminar']
            outreach = serializer.validated_data['outreach']
            training = serializer.validated_data['training']

            total_encounter = Visualization.objects.filter(created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_exo = Visualization.objects.filter(exo=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_art = Visualization.objects.filter(art=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_seal = Visualization.objects.filter(seal=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_sdf = Visualization.objects.filter(sdf=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_fv = Visualization.objects.filter(fv=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_health_post = Visualization.objects.filter(refer_hp=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_refer_hyg = Visualization.objects.filter(refer_hyg=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_refer_dent = Visualization.objects.filter(refer_dent=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_refer_dr = Visualization.objects.filter(refer_dr=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_refer_other = Visualization.objects.filter(refer_other=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            total_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,created_at__range=[start_date,end_date],geography_id=location).filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


            kid_encounter_male = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_encounter_female = Visualization.objects.filter(age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_exo_male = Visualization.objects.filter(exo=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_exo_female = Visualization.objects.filter(exo=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_art_male = Visualization.objects.filter(art=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_art_female = Visualization.objects.filter(art=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_seal_male = Visualization.objects.filter(seal=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_seal_female = Visualization.objects.filter(seal=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_sdf_male = Visualization.objects.filter(sdf=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_sdf_female = Visualization.objects.filter(sdf=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_fv_male = Visualization.objects.filter(fv=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_fv_female = Visualization.objects.filter(fv=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_health_post_male = Visualization.objects.filter(refer_hp=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_health_post_female = Visualization.objects.filter(refer_hp=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_refer_hyg_male = Visualization.objects.filter(refer_hyg=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_refer_hyg_female = Visualization.objects.filter(refer_hyg=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_refer_dent_male = Visualization.objects.filter(refer_dent=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_refer_dent_female = Visualization.objects.filter(refer_dent=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_refer_dr_male = Visualization.objects.filter(refer_dr=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_refer_dr_female = Visualization.objects.filter(refer_dr=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_refer_other_male = Visualization.objects.filter(refer_other=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_refer_other_female = Visualization.objects.filter(refer_other=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            kid_sdf_whole_mouth_male = Visualization.objects.filter(sdf_whole_mouth=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            kid_sdf_whole_mouth_female = Visualization.objects.filter(sdf_whole_mouth=True,age__lt=18,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_encounter_male = Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_encounter_female = Visualization.objects.filter(age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_exo_male = Visualization.objects.filter(exo=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_exo_female = Visualization.objects.filter(exo=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_art_male = Visualization.objects.filter(art=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_art_female = Visualization.objects.filter(art=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_seal_male = Visualization.objects.filter(seal=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_seal_female = Visualization.objects.filter(seal=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_sdf_male = Visualization.objects.filter(sdf=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_sdf_female = Visualization.objects.filter(sdf=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_fv_male = Visualization.objects.filter(fv=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_fv_female = Visualization.objects.filter(fv=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_health_post_male = Visualization.objects.filter(refer_hp=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_health_post_female = Visualization.objects.filter(refer_hp=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_refer_hyg_male = Visualization.objects.filter(refer_hyg=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_refer_hyg_female = Visualization.objects.filter(refer_hyg=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_refer_dent_male = Visualization.objects.filter(refer_dent=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_refer_dent_female = Visualization.objects.filter(refer_dent=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_refer_dr_male = Visualization.objects.filter(refer_dr=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_refer_dr_female = Visualization.objects.filter(refer_dr=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_refer_other_male = Visualization.objects.filter(refer_other=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_refer_other_female = Visualization.objects.filter(refer_other=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            adult_sdf_whole_mouth_male = Visualization.objects.filter(sdf_whole_mouth=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            adult_sdf_whole_mouth_female = Visualization.objects.filter(sdf_whole_mouth=True,age__range=(18,60),created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()


            old_encounter_male = Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_encounter_female = Visualization.objects.filter(age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_exo_male = Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_exo_female = Visualization.objects.filter(exo=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_art_male = Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_art_female = Visualization.objects.filter(art=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_seal_male = Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_seal_female = Visualization.objects.filter(seal=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_sdf_male = Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_sdf_female = Visualization.objects.filter(sdf=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_fv_male = Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_fv_female = Visualization.objects.filter(fv=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_health_post_male = Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_health_post_female = Visualization.objects.filter(refer_hp=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_refer_hyg_male = Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_refer_hyg_female = Visualization.objects.filter(refer_hyg=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_refer_dent_male = Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_refer_dent_female = Visualization.objects.filter(refer_dent=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_refer_dr_male = Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_refer_dr_female = Visualization.objects.filter(refer_dr=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_refer_other_male = Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_refer_other_female = Visualization.objects.filter(refer_other=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            old_sdf_whole_mouth_male = Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="male").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()
            old_sdf_whole_mouth_female = Visualization.objects.filter(sdf_whole_mouth=True,age__gt=60,created_at__range=[start_date,end_date],geography_id=location,gender="female").filter(Q(activities_id=health_post)|Q(activities_id=seminar)|Q(activities_id=outreach)|Q(activities_id=outreach)).count()

            return Response([["Kids"],\
            ['<span class="ml-4">Male</span>',kid_encounter_male, kid_exo_male, kid_art_male, kid_seal_male, kid_sdf_male, kid_sdf_whole_mouth_male, kid_fv_male, kid_health_post_male, kid_refer_hyg_male, kid_refer_dent_male, kid_refer_dr_male,kid_refer_other_male],\
            ['<span class="ml-4">Female</span>',kid_encounter_female, kid_exo_female, kid_art_female, kid_seal_female, kid_sdf_female, kid_sdf_whole_mouth_female, kid_fv_female, kid_health_post_female, kid_refer_hyg_female, kid_refer_dent_female, kid_refer_dr_female ,kid_refer_other_female],\
            ["Adults"],\
            ['<span class="ml-4">Male</span>',adult_encounter_male, adult_exo_male, adult_art_male, adult_seal_male, adult_sdf_male, adult_sdf_whole_mouth_male, adult_fv_male, adult_health_post_male, adult_refer_hyg_male, adult_refer_dent_male, adult_refer_dr_male, adult_refer_other_male],\
            ['<span class="ml-4">Female</span>',adult_encounter_female, adult_exo_female, adult_art_female, adult_seal_female, adult_sdf_female, adult_sdf_whole_mouth_female, adult_fv_female, adult_health_post_female, adult_refer_hyg_female, adult_refer_dent_female, adult_refer_dr_female, adult_refer_other_female],\
            ["Older Adults"],\
            ['<span class="ml-4">Male</span>',old_encounter_male, old_exo_male,old_art_male, old_seal_male,old_sdf_male, old_sdf_whole_mouth_male, old_fv_male, old_health_post_male, old_refer_hyg_male, old_refer_dent_male, old_refer_dr_male,old_refer_other_male],\
            ['<span class="ml-4">Female</span>',old_encounter_female, old_exo_female,old_art_female, old_seal_female,old_sdf_female, old_sdf_whole_mouth_female,old_fv_female,old_health_post_female, old_refer_hyg_female, old_refer_dent_female, old_refer_dr_female,old_refer_other_female],\
            ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf, total_sdf_whole_mouth, total_fv,total_health_post, total_refer_hyg,total_refer_dent, total_refer_dr,total_refer_other]])
        return Response({"message":serializer.error},status=400)

class TreatmentActivityList(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            health_post_obj = Activity.objects.get(name="Health Post")
            seminar_obj = Activity.objects.get(name="School Seminar")
            outreach_obj = Activity.objects.get(name="Community Outreach")
            training = Activity.objects.get(name="Training")

            health_post_check = Visualization.objects.filter(activities_id=health_post_obj.id).count()
            health_post_exo = Visualization.objects.filter(exo=True,activities_id=health_post_obj.id).count()
            health_post_art = Visualization.objects.filter(art=True,activities_id=health_post_obj.id).count()
            health_post_seal = Visualization.objects.filter(seal=True,activities_id=health_post_obj.id).count()
            health_post_sdf = Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id).count()
            health_post_fv = Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).count()
            health_post_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=health_post_obj.id).count()

            seminar_check = Visualization.objects.filter(activities_id=seminar_obj.id).count()
            seminar_exo = Visualization.objects.filter(exo=True,activities_id=seminar_obj.id).count()
            seminar_art = Visualization.objects.filter(art=True,activities_id=seminar_obj.id).count()
            seminar_seal = Visualization.objects.filter(seal=True,activities_id=seminar_obj.id).count()
            seminar_sdf = Visualization.objects.filter(sdf=True,activities_id=seminar_obj.id).count()
            seminar_fv = Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).count()
            seminar_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=seminar_obj.id).count()

            outreach_check = Visualization.objects.filter(activities_id=outreach_obj.id).count()
            outreach_exo = Visualization.objects.filter(exo=True,activities_id=outreach_obj.id).count()
            outreach_art = Visualization.objects.filter(art=True,activities_id=outreach_obj.id).count()
            outreach_seal = Visualization.objects.filter(seal=True,activities_id=outreach_obj.id).count()
            outreach_sdf = Visualization.objects.filter(sdf=True,activities_id=outreach_obj.id).count()
            outreach_fv = Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).count()
            outreach_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=outreach_obj.id).count()

            training_check = Visualization.objects.filter(activities_id=training.id).count()
            training_exo = Visualization.objects.filter(exo=True,activities_id=training.id).count()
            training_art = Visualization.objects.filter(art=True,activities_id=training.id).count()
            training_seal = Visualization.objects.filter(seal=True,activities_id=training.id).count()
            training_sdf = Visualization.objects.filter(sdf=True,activities_id=training.id).count()
            training_fv = Visualization.objects.filter(fv=True,activities_id=training.id).count()
            training_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True,activities_id=training.id).count()

            return Response([
            ["Clinic",health_post_check, health_post_exo, health_post_art, health_post_seal, health_post_sdf, health_post_fv, 0,0,0,0,0,0], \
            ["Seminar",seminar_check,seminar_exo, seminar_art, seminar_seal, seminar_sdf, seminar_fv, 0,0,0,0,0,0], \
            ["Outreach",outreach_check,outreach_exo, outreach_art, outreach_seal, outreach_sdf, outreach_fv, 0,0,0,0,0,0], \
            ["Training",training_check, training_exo, training_art, training_seal, training_sdf, training_fv, 0,0,0,0,0,0]])
        return Response({"treatment_obj":"do not have a permission"},status=400)



class VisualizationSetting(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id):
            district=['Kids','Teen','Adult', 'Old Adult']
            kid_exo = Visualization.objects.filter(exo=True,age__lt=12).count()
            kid_art = Visualization.objects.filter(art=True,age__lt=12).count()
            kid_seal = Visualization.objects.filter(seal=True,age__lt=12).count()
            kid_sdf = Visualization.objects.filter(sdf=True,age__lt=12).count()
            kid_fv = Visualization.objects.filter(fv=True,age__lt=12).count()

            teen_exo = Visualization.objects.filter(exo=True,age__range=(13,19)).count()
            teen_art = Visualization.objects.filter(art=True,age__range=(13,19)).count()
            teen_seal = Visualization.objects.filter(seal=True,age__range=(13,19)).count()
            teen_sdf = Visualization.objects.filter(sdf=True,age__range=(13,19)).count()
            teen_fv = Visualization.objects.filter(fv=True,age__range=(13,19)).count()

            adult_exo = Visualization.objects.filter(exo=True,age__range=(18,60)).count()
            adult_art = Visualization.objects.filter(art=True,age__range=(18,60)).count()
            adult_seal = Visualization.objects.filter(seal=True,age__range=(18,60)).count()
            adult_sdf = Visualization.objects.filter(sdf=True,age__range=(18,60)).count()
            adult_fv = Visualization.objects.filter(fv=True,age__range=(18,60)).count()

            old_adult_exo = Visualization.objects.filter(exo=True,age__gt=60).count()
            old_adult_art = Visualization.objects.filter(art=True,age__gt=60).count()
            old_adult_seal = Visualization.objects.filter(seal=True,age__gt=60).count()
            old_adult_sdf = Visualization.objects.filter(sdf=True,age__gt=60).count()
            old_adult_fv = Visualization.objects.filter(fv=True,age__gt=60).count()

            exo_data=[kid_exo, teen_exo, adult_exo, old_adult_exo]
            fv_data=[kid_fv, teen_fv, adult_fv, old_adult_fv]
            art_data=[kid_art, teen_art, adult_art, old_adult_art]
            seal_data=[kid_seal, teen_seal, adult_seal, old_adult_seal]
            sdf_data=[kid_sdf, teen_sdf, adult_sdf, old_adult_sdf]



            locationChart = {
            'data': {
            'labels': district,
            'datasets': [{
            'label': "EXO",
            'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            'borderColor': 'rgba(255, 206, 86, 1)',
            'borderWidth': 1,
            'data': exo_data},
            {
            'label': "FV",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': fv_data},
            {
            'label': "ART",
            'backgroundColor': 'rgba(81, 264, 210, 0.2)',
            'borderColor': 'rgba(81, 264, 210, 1)',
            'borderWidth': 1,
            'data': art_data},
            {
            'label': "SEAL",
            'backgroundColor': 'rgba(16, 152, 247, 0.2)',
            'borderColor': 'rgba(16, 152, 247, 1)',
            'borderWidth': 1,
            'data': seal_data},
            {
            'label': "SDF",
            'backgroundColor': 'rgba(87, 50, 200, 0.2)',
            'borderColor': 'rgba(87, 50, 200, 1)',
            'borderWidth': 1,
            'data': sdf_data}]
            },
            'options': {
            'aspectRatio': 1.5,
            'scales': {
            'yAxes': [{
            # 'stacked': 'true',
            'ticks': {
            'beginAtZero':'true'}
            }]
            # 'xAxes': [{
            # 'stacked': 'true',
            # }]
            },
            'title': {
            'display': 'true',
            'text': "Setting-wise treatment distribution",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"
            },
            'legend': {
            'display': 'true',
            'position': 'bottom',
            'labels': {
            'usePointStyle': 'true',
            'padding': 20,
            'fontFamily': "'Maven Pro', sans-serif"
      }
    }
  }
            }
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can create"},status=400)


class VisualizationSettingFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']

            district=['Health Post', 'School Seminar', 'Community Outreach', 'Training']
            health_post_obj = Activity.objects.get(name="Health Post")
            seminar_obj = Activity.objects.get(name="School Seminar")
            outreach_obj = Activity.objects.get(name="Community Outreach")
            training = Activity.objects.get(name="Training")
            if serializer.validated_data['age_group']=="Activity":
                health_post_exo = Visualization.objects.filter(exo=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                health_post_art = Visualization.objects.filter(art=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                health_post_seal = Visualization.objects.filter(seal=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                health_post_sdf = Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                health_post_fv = Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                seminar_exo = Visualization.objects.filter(exo=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                seminar_art = Visualization.objects.filter(art=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                seminar_seal = Visualization.objects.filter(seal=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                seminar_sdf = Visualization.objects.filter(sdf=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                seminar_fv = Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                outreach_exo = Visualization.objects.filter(exo=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                outreach_art = Visualization.objects.filter(art=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                outreach_seal = Visualization.objects.filter(seal=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                outreach_sdf = Visualization.objects.filter(sdf=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                outreach_fv = Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                training_exo = Visualization.objects.filter(exo=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                training_art = Visualization.objects.filter(art=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                training_seal = Visualization.objects.filter(seal=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                training_sdf = Visualization.objects.filter(sdf=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                training_fv = Visualization.objects.filter(fv=True,activities_id=training.id).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                exo_data=[health_post_exo,seminar_exo,outreach_exo,training_exo]
                fv_data=[health_post_fv,seminar_fv,outreach_fv,training_fv]
                art_data=[health_post_art,seminar_art,outreach_art,training_art]
                seal_data=[health_post_seal,seminar_seal,outreach_seal,training_seal]
                sdf_data=[health_post_sdf,seminar_sdf,outreach_sdf,training_sdf]



                locationChart = {
                'data': {
                'labels': district,
                'datasets': [{
                'label': "EXO",
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'borderColor': 'rgba(255, 206, 86, 1)',
                'borderWidth': 1,
                'data': exo_data},
                {
                'label': "FV",
                'backgroundColor': 'rgba(239, 62, 54, 0.2)',
                'borderColor': 'rgba(239, 62, 54, 1)',
                'borderWidth': 1,
                'data': fv_data},
                {
                'label': "ART",
                'backgroundColor': 'rgba(81, 264, 210, 0.2)',
                'borderColor': 'rgba(81, 264, 210, 1)',
                'borderWidth': 1,
                'data': art_data},
                {
                'label': "SEAL",
                'backgroundColor': 'rgba(16, 152, 247, 0.2)',
                'borderColor': 'rgba(16, 152, 247, 1)',
                'borderWidth': 1,
                'data': seal_data},
                {
                'label': "SDF",
                'backgroundColor': 'rgba(87, 50, 200, 0.2)',
                'borderColor': 'rgba(87, 50, 200, 1)',
                'borderWidth': 1,
                'data': sdf_data}]
                },
                'options': {
                'aspectRatio': 1.5,
                'scales': {
                'yAxes': [{
                'ticks': {
                'beginAtZero':'true'}
                }]
                },
                'title': {
                'display': 'true',
                'text': "Setting-wise treatment distribution",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
                },
                'legend': {
                'display': 'true',
                'position': 'bottom',
                'labels': {
                'usePointStyle': 'true',
                'padding': 20,
                'fontFamily': "'Maven Pro', sans-serif"
          }
        }
      }
                }
                return JsonResponse({"locationChart":locationChart})
            elif serializer.validated_data['age_group']=="Age Group":
                district=['Kids','Teen','Adult', 'Old Adult']
                kid_exo = Visualization.objects.filter(exo=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                kid_art = Visualization.objects.filter(art=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                kid_seal = Visualization.objects.filter(seal=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                kid_sdf = Visualization.objects.filter(sdf=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                kid_fv = Visualization.objects.filter(fv=True,age__lt=12).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                teen_exo = Visualization.objects.filter(exo=True,age__range=(13,19)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                teen_art = Visualization.objects.filter(art=True,age__range=(13,19)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                teen_seal = Visualization.objects.filter(seal=True,age__range=(13,19)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                teen_sdf = Visualization.objects.filter(sdf=True,age__range=(13,19)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                teen_fv = Visualization.objects.filter(fv=True,age__range=(13,19)).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                adult_exo = Visualization.objects.filter(exo=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                adult_art = Visualization.objects.filter(art=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                adult_seal = Visualization.objects.filter(seal=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                adult_sdf = Visualization.objects.filter(sdf=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                adult_fv = Visualization.objects.filter(fv=True,age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                old_adult_exo = Visualization.objects.filter(exo=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                old_adult_art = Visualization.objects.filter(art=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                old_adult_seal = Visualization.objects.filter(seal=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                old_adult_sdf = Visualization.objects.filter(sdf=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()
                old_adult_fv = Visualization.objects.filter(fv=True,age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).count()

                exo_data=[kid_exo, teen_exo, adult_exo, old_adult_exo]
                fv_data=[kid_fv, teen_fv, adult_fv, old_adult_fv]
                art_data=[kid_art, teen_art, adult_art, old_adult_art]
                seal_data=[kid_seal, teen_seal, adult_seal, old_adult_seal]
                sdf_data=[kid_sdf, teen_sdf, adult_sdf, old_adult_sdf]



                locationChart = {
                'data': {
                'labels': district,
                'datasets': [{
                'label': "EXO",
                'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                'borderColor': 'rgba(255, 206, 86, 1)',
                'borderWidth': 1,
                'data': exo_data},
                {
                'label': "FV",
                'backgroundColor': 'rgba(239, 62, 54, 0.2)',
                'borderColor': 'rgba(239, 62, 54, 1)',
                'borderWidth': 1,
                'data': fv_data},
                {
                'label': "ART",
                'backgroundColor': 'rgba(81, 264, 210, 0.2)',
                'borderColor': 'rgba(81, 264, 210, 1)',
                'borderWidth': 1,
                'data': art_data},
                {
                'label': "SEAL",
                'backgroundColor': 'rgba(16, 152, 247, 0.2)',
                'borderColor': 'rgba(16, 152, 247, 1)',
                'borderWidth': 1,
                'data': seal_data},
                {
                'label': "SDF",
                'backgroundColor': 'rgba(87, 50, 200, 0.2)',
                'borderColor': 'rgba(87, 50, 200, 1)',
                'borderWidth': 1,
                'data': sdf_data}]
                },
                'options': {
                'aspectRatio': 1.5,
                'scales': {
                'yAxes': [{
                # 'stacked': 'true',
                'ticks': {
                'beginAtZero':'true'}
                }]
                # 'xAxes': [{
                # 'stacked': 'true',
                # }]
                },
                'title': {
                'display': 'true',
                'text': "Setting-wise treatment distribution",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
                },
                'legend': {
                'display': 'true',
                'position': 'bottom',
                'labels': {
                'usePointStyle': 'true',
                'padding': 20,
                'fontFamily': "'Maven Pro', sans-serif"
          }
        }
      }
                }
                return JsonResponse({"locationChart":locationChart})
        return Response(serializer.error)




class TreatmentbyWardList(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        list_data=[]
        for war_obj in Ward.objects.filter(status=True):
            loop_data=[]
            check = Visualization.objects.filter(geography_id=war_obj.id).count()
            exo = Visualization.objects.filter(geography_id=war_obj.id,exo=True).count()
            art = Visualization.objects.filter(geography_id=war_obj.id,art=True).count()
            seal = Visualization.objects.filter(geography_id=war_obj.id,seal=True).count()
            sdf = Visualization.objects.filter(geography_id=war_obj.id,sdf=True).count()
            fv = Visualization.objects.filter(geography_id=war_obj.id,fv=True).count()
            sdf_whole_mouth = Visualization.objects.filter(geography_id=war_obj.id,sdf_whole_mouth=True).count()
            refer_hp = Visualization.objects.filter(geography_id=war_obj.id,refer_hp=True).count()
            refer_hyg = Visualization.objects.filter(geography_id=war_obj.id,refer_hyg=True).count()
            refer_dent = Visualization.objects.filter(geography_id=war_obj.id,refer_dent=True).count()
            refer_dr = Visualization.objects.filter(geography_id=war_obj.id,refer_dr=True).count()
            refer_other = Visualization.objects.filter(geography_id=war_obj.id,refer_other=True).count()
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



class PieChartVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        kids=[]
        teen=[]
        adult=[]
        old_adult=[]
        kids_count = Visualization.objects.filter(age__lt=12).count()
        teen_count = Visualization.objects.filter(age__range=(13,19)).count()
        adult_count = Visualization.objects.filter(age__range=(20,60)).count()
        old_adult_count =Visualization.objects.filter(age__gt=60).count()
        kids.append(kids_count)
        teen.append(teen_count)
        adult.append(adult_count)
        old_adult.append(old_adult_count)
        locationChart = {
        'data': {
        'labels': ['Kids', 'Teens', 'Adult', 'Old Adult'],
        'datasets': [
        {
        'label': "Female",
        'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)'],
        'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)'],
        'borderWidth': 1,
        'data': [kids, teen, adult, old_adult]
        }]},
        'options': {
        'aspectRatio': 1.5,
        'title': {
        'display': 'true',
        'text': "Activity Distribution Chart",
        'fontSize': 18,
        'fontFamily': "'Palanquin', sans-serif"},
        'legend': {
        'display': 'true',
        'position': 'bottom',
        'labels': {
        'usePointStyle': 'true',
        'padding': 20,
        'fontFamily': "'Maven Pro', sans-serif"}
        }}}
        return JsonResponse({"locationChart":locationChart})


class PieChartVisualizationFilter(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatMentBarGraphVisualization
    def post(self, request, format=None):
        serializer = TreatMentBarGraphVisualization(data=request.data,context={'request': request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
            end_date = str(NepaliDate.from_date(serializer.validated_data['end_date']))
            location = serializer.validated_data['location']
            if serializer.validated_data['age_group']=="Age Group":
                kids=[]
                teen=[]
                adult=[]
                old_adult=[]
                kids_count = Visualization.objects.filter(age__lt=12).count()
                teen_count = Visualization.objects.filter(age__range=(13,19)).count()
                adult_count = Visualization.objects.filter(age__range=(20,60)).count()
                old_adult_count =Visualization.objects.filter(age__gt=60).count()
                kids.append(kids_count)
                teen.append(teen_count)
                adult.append(adult_count)
                old_adult.append(old_adult_count)
                locationChart = {
                'data': {
                'labels': ['Kids', 'Teens', 'Adult', 'Old Adult'],
                'datasets': [
                {
                'label': "Female",
                'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)'],
                'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)'],
                'borderWidth': 1,
                'data': [kids, teen, adult, old_adult]
                }]},
                'options': {
                'aspectRatio': 1.5,
                'title': {
                'display': 'true',
                'text': "Activity Distribution Chart",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"},
                'legend': {
                'display': 'true',
                'position': 'bottom',
                'labels': {
                'usePointStyle': 'true',
                'padding': 20,
                'fontFamily': "'Maven Pro', sans-serif"}
                }}}
                return JsonResponse({"locationChart":locationChart})
            elif serializer.validated_data['age_group']=="Treatment Type":
                exo=[]
                art=[]
                seal=[]
                sdf=[]
                fv=[]
                exo_count = Visualization.objects.filter(exo=True).count()
                art_count = Visualization.objects.filter(art=True).count()
                seal_count = Visualization.objects.filter(seal=True).count()
                sdf_count =Visualization.objects.filter(sdf=True).count()
                fv_count =Visualization.objects.filter(fv=True).count()
                exo.append(exo_count)
                art.append(art_count)
                seal.append(seal_count)
                sdf.append(sdf_count)
                fv.append(fv_count)
                locationChart = {
                'data': {
                'labels': ['EXO', 'ART', 'SEAL', 'SDF','FV'],
                'datasets': [
                {
                'label': "Female",
                'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)','rgba(92, 151, 45, 0.5)'],
                'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)','rgba(105, 153, 45, 1)'],
                'borderWidth': 1,
                'data': [exo, art, seal, sdf,fv]
                }]},
                'options': {
                'aspectRatio': 1.5,
                'title': {
                'display': 'true',
                'text': "Activity Distribution Chart",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"},
                'legend': {
                'display': 'true',
                'position': 'bottom',
                'labels': {
                'usePointStyle': 'true',
                'padding': 20,
                'fontFamily': "'Maven Pro', sans-serif"}
                }}}
                return JsonResponse({"locationChart":locationChart})
