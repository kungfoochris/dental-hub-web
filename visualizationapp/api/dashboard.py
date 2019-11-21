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


            kid_encounter = Visualization.objects.filter(age__lt=18).count()
            kid_exo = Visualization.objects.filter(age__lt=18,exo=True).count()
            kid_art = Visualization.objects.filter(age__lt=18,art=True).count()
            kid_seal = Visualization.objects.filter(age__lt=18,seal=True).count()
            kid_sdf = Visualization.objects.filter(age__lt=18,sdf=True).count()
            kid_fv = Visualization.objects.filter(age__lt=18,fv=True).count()
            kid_health_post = Visualization.objects.filter(age__lt=18,refer_hp=True).count()
            kid_refer_hyg = Visualization.objects.filter(age__lt=18,refer_hyg=True).count()
            kid_refer_dent = Visualization.objects.filter(age__lt=18,refer_dent=True).count()
            kid_refer_dr = Visualization.objects.filter(age__lt=18,refer_dr=True).count()
            kid_refer_other = Visualization.objects.filter(age__lt=18,refer_other=True).count()
            kid_sdf_whole_mouth = Visualization.objects.filter(age__lt=18,sdf_whole_mouth=True).count()

            adult_encounter = Visualization.objects.filter(age__range=(18,60)).count()
            adult_exo = Visualization.objects.filter(age__range=(18,60),exo=True).count()
            adult_art = Visualization.objects.filter(age__range=(18,60),art=True).count()
            adult_seal = Visualization.objects.filter(age__range=(18,60),seal=True).count()
            adult_sdf = Visualization.objects.filter(age__range=(18,60),sdf=True).count()
            adult_fv = Visualization.objects.filter(age__range=(18,60),fv=True).count()
            adult_health_post = Visualization.objects.filter(age__range=(18,60),refer_hp=True).count()
            adult_refer_hyg = Visualization.objects.filter(age__range=(18,60),refer_hyg=True).count()
            adult_refer_dent = Visualization.objects.filter(age__range=(18,60),refer_dent=True).count()
            adult_refer_dr = Visualization.objects.filter(age__range=(18,60),refer_dr=True).count()
            adult_refer_other = Visualization.objects.filter(age__range=(18,60),refer_other=True).count()
            adult_sdf_whole_mouth = Visualization.objects.filter(age__range=(18,60),sdf_whole_mouth=True).count()


            old_encounter = Visualization.objects.filter(age__gt=60).count()
            old_exo = Visualization.objects.filter(age__gt=60,exo=True).count()
            old_art = Visualization.objects.filter(age__gt=60,art=True).count()
            old_seal = Visualization.objects.filter(age__gt=60,seal=True).count()
            old_sdf = Visualization.objects.filter(age__gt=60,sdf=True).count()
            old_fv = Visualization.objects.filter(age__gt=60,fv=True).count()
            old_health_post = Visualization.objects.filter(age__gt=60,refer_hp=True).count()
            old_refer_hyg = Visualization.objects.filter(age__gt=60,refer_hyg=True).count()
            old_refer_dent = Visualization.objects.filter(age__gt=60,refer_dent=True).count()
            old_refer_dr = Visualization.objects.filter(age__gt=60,refer_dr=True).count()
            old_refer_other = Visualization.objects.filter(age__gt=60,refer_other=True).count()
            old_sdf_whole_mouth = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True).count()

            return Response([["Kids",kid_encounter, kid_exo, kid_art, kid_seal, kid_sdf, kid_sdf_whole_mouth, kid_fv, kid_health_post, kid_refer_hyg, kid_refer_dent, kid_refer_dr ,kid_refer_other],\
                ["Adults",adult_encounter, adult_exo, adult_art, adult_seal, adult_sdf, adult_sdf_whole_mouth, adult_fv, adult_health_post, adult_refer_hyg, adult_refer_dent, adult_refer_dr, adult_refer_other],\
                ["Older Adults",old_encounter, old_exo,old_art,old_seal,old_sdf, old_sdf_whole_mouth,old_fv,old_health_post, old_refer_hyg, old_refer_dent, old_refer_dr,old_refer_other],\
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

            total_encounter = Visualization.objects.filter(created_at__range=[start_date,end_date],geography_id=location).count()
            total_exo = Visualization.objects.filter(exo=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_art = Visualization.objects.filter(art=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_seal = Visualization.objects.filter(seal=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_sdf = Visualization.objects.filter(sdf=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_fv = Visualization.objects.filter(fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_health_post = Visualization.objects.filter(refer_hp=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_refer_hyg = Visualization.objects.filter(refer_hyg=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_refer_dent = Visualization.objects.filter(refer_dent=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_refer_dr = Visualization.objects.filter(refer_dr=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_refer_other = Visualization.objects.filter(refer_other=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            total_sdf_whole_mouth = Visualization.objects.filter(sdf_whole_mouth=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()


            kid_encounter = Visualization.objects.filter(age__lt=18).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_exo = Visualization.objects.filter(age__lt=18,exo=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_art = Visualization.objects.filter(age__lt=18,art=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_seal = Visualization.objects.filter(age__lt=18,seal=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_sdf = Visualization.objects.filter(age__lt=18,sdf=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_fv = Visualization.objects.filter(age__lt=18,fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_health_post = Visualization.objects.filter(age__lt=18,refer_hp=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_refer_hyg = Visualization.objects.filter(age__lt=18,refer_hyg=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_refer_dent = Visualization.objects.filter(age__lt=18,refer_dent=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_refer_dr = Visualization.objects.filter(age__lt=18,refer_dr=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_refer_other = Visualization.objects.filter(age__lt=18,refer_other=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            kid_sdf_whole_mouth = Visualization.objects.filter(age__lt=18,sdf_whole_mouth=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()

            adult_encounter = Visualization.objects.filter(age__range=(18,60)).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_exo = Visualization.objects.filter(age__range=(18,60),exo=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_art = Visualization.objects.filter(age__range=(18,60),art=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_seal = Visualization.objects.filter(age__range=(18,60),seal=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_sdf = Visualization.objects.filter(age__range=(18,60),sdf=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_fv = Visualization.objects.filter(age__range=(18,60),fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_health_post = Visualization.objects.filter(age__range=(18,60),refer_hp=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_refer_hyg = Visualization.objects.filter(age__range=(18,60),refer_hyg=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_refer_dent = Visualization.objects.filter(age__range=(18,60),refer_dent=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_refer_dr = Visualization.objects.filter(age__range=(18,60),refer_dr=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_refer_other = Visualization.objects.filter(age__range=(18,60),refer_other=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            adult_sdf_whole_mouth = Visualization.objects.filter(age__range=(18,60),sdf_whole_mouth=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()


            old_encounter = Visualization.objects.filter(age__gt=60).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_exo = Visualization.objects.filter(age__gt=60,exo=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_art = Visualization.objects.filter(age__gt=60,art=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_seal = Visualization.objects.filter(age__gt=60,seal=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_sdf = Visualization.objects.filter(age__gt=60,sdf=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_fv = Visualization.objects.filter(age__gt=60,fv=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_health_post = Visualization.objects.filter(age__gt=60,refer_hp=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_refer_hyg = Visualization.objects.filter(age__gt=60,refer_hyg=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_refer_dent = Visualization.objects.filter(age__gt=60,refer_dent=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_refer_dr = Visualization.objects.filter(age__gt=60,refer_dr=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_refer_other = Visualization.objects.filter(age__gt=60,refer_other=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()
            old_sdf_whole_mouth = Visualization.objects.filter(age__gt=60,sdf_whole_mouth=True).filter(created_at__range=[start_date,end_date],geography_id=location).filter(activities_id=health_post).filter(activities_id=seminar).filter(activities_id=outreach).filter(activities_id=training).count()

            return Response([["Kids",kid_encounter, kid_exo, kid_art, kid_seal, kid_sdf, kid_sdf_whole_mouth, kid_fv, kid_health_post, kid_refer_hyg, kid_refer_dent, kid_refer_dr ,kid_refer_other],\
                ["Adults",adult_encounter, adult_exo, adult_art, adult_seal, adult_sdf, adult_sdf_whole_mouth, adult_fv, adult_health_post, adult_refer_hyg, adult_refer_dent, adult_refer_dr, adult_refer_other],\
                ["Older Adults",old_encounter, old_exo,old_art,old_seal,old_sdf, old_sdf_whole_mouth, old_fv,old_health_post, old_refer_hyg, old_refer_dent, old_refer_dr,old_refer_other],\
                ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf, total_sdf_whole_mouth, total_fv,total_health_post, total_refer_hyg,total_refer_dent, total_refer_dr,total_refer_other]])
            return Response({"message":"data accept is denied."},status=200)
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
            district=['Health Post', 'School Seminar', 'Community Outreach', 'Training']

            health_post_obj = Activity.objects.get(name="Health Post")
            seminar_obj = Activity.objects.get(name="School Seminar")
            outreach_obj = Activity.objects.get(name="Community Outreach")
            training = Activity.objects.get(name="Training")

            health_post_exo = Visualization.objects.filter(exo=True,activities_id=health_post_obj.id).count()
            health_post_art = Visualization.objects.filter(art=True,activities_id=health_post_obj.id).count()
            health_post_seal = Visualization.objects.filter(seal=True,activities_id=health_post_obj.id).count()
            health_post_sdf = Visualization.objects.filter(sdf=True,activities_id=health_post_obj.id).count()
            health_post_fv = Visualization.objects.filter(fv=True,activities_id=health_post_obj.id).count()

            seminar_exo = Visualization.objects.filter(exo=True,activities_id=seminar_obj.id).count()
            seminar_art = Visualization.objects.filter(art=True,activities_id=seminar_obj.id).count()
            seminar_seal = Visualization.objects.filter(seal=True,activities_id=seminar_obj.id).count()
            seminar_sdf = Visualization.objects.filter(sdf=True,activities_id=seminar_obj.id).count()
            seminar_fv = Visualization.objects.filter(fv=True,activities_id=seminar_obj.id).count()

            outreach_exo = Visualization.objects.filter(exo=True,activities_id=outreach_obj.id).count()
            outreach_art = Visualization.objects.filter(art=True,activities_id=outreach_obj.id).count()
            outreach_seal = Visualization.objects.filter(seal=True,activities_id=outreach_obj.id).count()
            outreach_sdf = Visualization.objects.filter(sdf=True,activities_id=outreach_obj.id).count()
            outreach_fv = Visualization.objects.filter(fv=True,activities_id=outreach_obj.id).count()

            training_exo = Visualization.objects.filter(exo=True,activities_id=training.id).count()
            training_art = Visualization.objects.filter(art=True,activities_id=training.id).count()
            training_seal = Visualization.objects.filter(seal=True,activities_id=training.id).count()
            training_sdf = Visualization.objects.filter(sdf=True,activities_id=training.id).count()
            training_fv = Visualization.objects.filter(fv=True,activities_id=training.id).count()

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
            'stacked': 'true',
            'ticks': {
            'beginAtZero':'true'}
            }],
            'xAxes': [{
            'stacked': 'true',
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
