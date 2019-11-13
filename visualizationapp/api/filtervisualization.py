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
greaterthan60 = d - datetime.timedelta(days=365*60)


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class OverviewVisualization(APIView):
      permission_classes = (IsPostOrIsAuthenticated,)
      def get(self, request,start_date,end_date,location_id,format=None):
            if User.objects.filter(id=request.user.id).exists():
                if start_date=="null" and end_date == "null" and location_id=="null":
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

                    return Response([["Kids",kid_encounter, kid_exo, kid_art, kid_seal, kid_sdf, kid_fv, kid_health_post, kid_refer_hyg, kid_refer_dent, kid_refer_dr ,kid_refer_other],\
                        ["Adults",adult_encounter, adult_exo, adult_art, adult_seal, adult_sdf, adult_fv, adult_health_post, adult_refer_hyg, adult_refer_dent, adult_refer_dr, adult_refer_other],\
                        ["Older Adults",old_encounter, old_exo,old_art,old_seal,old_sdf,old_fv,old_health_post, old_refer_hyg, old_refer_dent, old_refer_dr,old_refer_other],\
                        ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf,total_fv,total_health_post, total_refer_hyg,total_refer_dent, total_refer_dr,total_refer_other]])
                else:
                    print(location_id)
                    print(type(location_id))
                    total_encounter = Visualization.objects.filter(created_at__range=[start_date,end_date],geography_id=location_id).count()
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

                    return Response([["Kids",kid_encounter, kid_exo, kid_art, kid_seal, kid_sdf, kid_fv, kid_health_post, kid_refer_hyg, kid_refer_dent, kid_refer_dr ,kid_refer_other],\
                        ["Adults",adult_encounter, adult_exo, adult_art, adult_seal, adult_sdf, adult_fv, adult_health_post, adult_refer_hyg, adult_refer_dent, adult_refer_dr, adult_refer_other],\
                        ["Older Adults",old_encounter, old_exo,old_art,old_seal,old_sdf,old_fv,old_health_post, old_refer_hyg, old_refer_dent, old_refer_dr,old_refer_other],\
                        ["Total",total_encounter,total_exo,total_art,total_seal,total_sdf,total_fv,total_health_post, total_refer_hyg,total_refer_dent, total_refer_dr,total_refer_other]])

                return Response({"treatment_obj":"do not have a permission"},status=400)
