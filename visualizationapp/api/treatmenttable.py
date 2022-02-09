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
from encounterapp.models import Screeing, Encounter
from visualizationapp.models import Visualization
from nepali.datetime import NepaliDate
from django.db.models import DurationField, F, ExpressionWrapper
from visualizationapp.serializers.visualization import (
    TreatMentBarGraphVisualization,
    TreatmentStrategicDataSerializer,
)
from django.db.models import Q
from django.db.models import Count
import datetime

# from datetime import datetime
# from datetime import timedelta
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

np_date = NepaliDate()
# d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
# lessthan18 = d - datetime.timedelta(days=365+18)
# greaterthan60 = d - datetime.timedelta(days=365+60)

today_date = datetime.date.today()
last_30_days = datetime.date.today() + datetime.timedelta(-30)

today_date_obj = str(NepaliDate.from_date(today_date))
last_30_days_obj = str(NepaliDate.from_date(last_30_days))


class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


# 2.1 2.1 Preventative Overview
class TreatmentTableBasicData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatmentStrategicDataSerializer

    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():

            total_male_fsdf_fv = []
            total_female_fsdf_fv = []
            total_child_fsdf_fv = []
            total_teen_fsdf_fv = []
            total_adult_fsdf_fv = []
            total_old_fsdf_fv = []

            treatment_obj = Treatment.objects.all().count()
            treatment_male = Visualization.objects.filter(active=True,
                gender="male", created_at__range=[last_30_days_obj, today_date_obj]
            ).count()
            treatment_female = Visualization.objects.filter(active=True,
                gender="female", created_at__range=[last_30_days_obj, today_date_obj]
            ).count()
            treatment_child = Visualization.objects.filter(active=True,
                age__lt=13, created_at__range=[last_30_days_obj, today_date_obj]
            ).count()
            treatment_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            treatment_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            treatment_old = Visualization.objects.filter(active=True,
                age__gt=60, created_at__range=[last_30_days_obj, today_date_obj]
            ).count()

            # F-SDF FV
            male_fsdf_fv = Visualization.objects.filter(
                active=True,
                gender="male",
                sdf_whole_mouth=True,fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            )
            total_male_fsdf_fv.append(male_fsdf_fv.count())
            for i in male_fsdf_fv:
                total_male_fsdf_fv.append(Visualization.objects.filter(
                    active=True,
                    gender="male",
                    created_at__range=[last_30_days_obj, today_date_obj],
                ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).exclude(id=i.id).count())

            female_fsdf_fv = Visualization.objects.filter(
                active=True,
                gender="female",
                sdf_whole_mouth=True,fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            )
            total_female_fsdf_fv.append(female_fsdf_fv.count())
            for i in female_fsdf_fv:
                total_female_fsdf_fv.append(Visualization.objects.filter(
                    active=True,
                    gender="female",
                    created_at__range=[last_30_days_obj, today_date_obj],
                ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).exclude(id=i.id).count())
            
            child_fsdf_fv = Visualization.objects.filter(
                age__lt=13,
                active=True,
                sdf_whole_mouth=True,fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            )
            total_child_fsdf_fv.append(child_fsdf_fv.count())
            for i in child_fsdf_fv:
                total_child_fsdf_fv.append(Visualization.objects.filter(
                    age__lt=13,
                    active=True,
                    created_at__range=[last_30_days_obj, today_date_obj],
                ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).exclude(id=i.id).count())
            
            teen_fsdf_fv = Visualization.objects.filter(
                age__range=(13, 18),
                active=True,
                sdf_whole_mouth=True,fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            )
            total_teen_fsdf_fv.append(teen_fsdf_fv.count())
            for i in teen_fsdf_fv:
                total_teen_fsdf_fv.append(Visualization.objects.filter(
                    age__range=(13, 18),
                    active=True,
                    created_at__range=[last_30_days_obj, today_date_obj],
                ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).exclude(id=i.id).count())
            
            adult_fsdf_fv = Visualization.objects.filter(
                age__range=(19, 60),
                active=True,
                sdf_whole_mouth=True,fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            )
            total_adult_fsdf_fv.append(adult_fsdf_fv.count())
            for i in adult_fsdf_fv:
                total_adult_fsdf_fv.append(Visualization.objects.filter(
                    age__range=(19, 60),
                    active=True,
                    created_at__range=[last_30_days_obj, today_date_obj],
                ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).exclude(id=i.id).count())
            
            old_fsdf_fv = Visualization.objects.filter(
                age__gt=60,
                active=True,
                sdf_whole_mouth=True,fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            )
            total_old_fsdf_fv.append(old_fsdf_fv.count())
            for i in old_fsdf_fv:
                total_old_fsdf_fv.append(Visualization.objects.filter(
                    age__gt=60,
                    active=True,
                    created_at__range=[last_30_days_obj, today_date_obj],
                ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).exclude(id=i.id).count())
            



            # SEAL
            sealant_male = Visualization.objects.filter(active=True,
                gender="male",
                need_sealant=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            sealant_female = Visualization.objects.filter(active=True,
                gender="female",
                need_sealant=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            sealant_child = Visualization.objects.filter(active=True,
                age__lt=13,
                need_sealant=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            sealant_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                need_sealant=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            sealant_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                need_sealant=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            sealant_old = Visualization.objects.filter(active=True,
                age__gt=60,
                need_sealant=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            

            cavities_prevented_male = (
                0.2 * sum(total_male_fsdf_fv) + 0.1 * sealant_male
            )
            cavities_prevented_female = (
                0.2 * sum(total_female_fsdf_fv) + 0.1 * sealant_female
            )
            cavities_prevented_child = (
                0.2 * sum(total_child_fsdf_fv) + 0.1 * sealant_child
            )
            cavities_prevented_teen = (
                0.2 * sum(total_teen_fsdf_fv) + 0.1 * sealant_teen
            )
            cavities_prevented_adult = (
                0.2 * sum(total_adult_fsdf_fv) + 0.1 * sealant_adult
            )
            cavities_prevented_old = (
                0.2 * sum(total_old_fsdf_fv) + 0.1 * sealant_old
            )
            total_cavities = cavities_prevented_male + cavities_prevented_female

            total_contact = treatment_male + treatment_female

            return Response(
                [
                    [
                        "Number of Cavities Prevented",
                        round(cavities_prevented_male, 2),
                        round(cavities_prevented_female, 2),
                        round(cavities_prevented_child, 2),
                        round(cavities_prevented_teen, 2),
                        round(cavities_prevented_adult, 2),
                        round(cavities_prevented_old, 2),
                        round(total_cavities, 2),
                    ],
                    [
                        "Contacts",
                        treatment_male,
                        treatment_female,
                        treatment_child,
                        treatment_teen,
                        treatment_adult,
                        treatment_old,
                        total_contact,
                    ],
                ]
            )
        return Response({"treatment_obj": "do not have a permission"}, status=400)

    def post(self, request, format=None):
        serializer = TreatmentStrategicDataSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            location_list = serializer.validated_data["location"]
            health_post = serializer.validated_data["health_post"]
            seminar = serializer.validated_data["seminar"]
            outreach = serializer.validated_data["outreach"]
            training = serializer.validated_data["training"]

            if end_date > start_date:
                treatment_male_list = []
                treatment_female_list = []
                treatment_child_list = []
                treatment_teen_list = []
                treatment_adult_list = []
                treatment_old_list = []

                total_male_fsdf_fv = []
                total_female_fsdf_fv = []
                total_child_fsdf_fv = []
                total_teen_fsdf_fv = []
                total_adult_fsdf_fv = []
                total_old_fsdf_fv = []

                sealant_male_list = []
                sealant_female_list = []
                sealant_teen_list = []
                sealant_child_list = []
                sealant_adult_list = []
                sealant_old_list = []
                for location in location_list:
                    treatment_male_list.append(
                        Visualization.objects.filter(active=True,
                            gender="male",
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    treatment_female_list.append(
                        Visualization.objects.filter(active=True,
                            gender="female",
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    treatment_child_list.append(
                        Visualization.objects.filter(active=True,
                            age__lt=13,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    treatment_teen_list.append(
                        Visualization.objects.filter(active=True,
                            age__range=(13, 18),
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    treatment_adult_list.append(
                        Visualization.objects.filter(active=True,
                            age__range=(19, 60),
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    treatment_old_list.append(
                        Visualization.objects.filter(active=True,
                            age__gt=60,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )


                    # F-SDF FV
                    male_fsdf_fv = Visualization.objects.filter(
                        active=True,
                        gender="male",
                        sdf_whole_mouth=True,fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    ).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                    total_male_fsdf_fv.append(male_fsdf_fv.count())
                    for i in male_fsdf_fv:
                        total_male_fsdf_fv.append(Visualization.objects.filter(
                            active=True,
                            gender="male",
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        ).exclude(id=i.id).count())

                    female_fsdf_fv = Visualization.objects.filter(
                        active=True,
                        gender="female",
                        sdf_whole_mouth=True,fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    ).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                    total_female_fsdf_fv.append(female_fsdf_fv.count())
                    for i in female_fsdf_fv:
                        total_female_fsdf_fv.append(Visualization.objects.filter(
                            active=True,
                            gender="female",
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        ).exclude(id=i.id).count())
                    
                    child_fsdf_fv = Visualization.objects.filter(
                        age__lt=13,
                        active=True,
                        sdf_whole_mouth=True,fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    ).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                    total_child_fsdf_fv.append(child_fsdf_fv.count())
                    for i in child_fsdf_fv:
                        total_child_fsdf_fv.append(Visualization.objects.filter(
                            age__lt=13,
                            active=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        ).exclude(id=i.id).count())
                    
                    teen_fsdf_fv = Visualization.objects.filter(
                        age__range=(13, 18),
                        active=True,
                        sdf_whole_mouth=True,fv=True,
                        created_at__range=[start_date, end_date],
                            geography_id=location.id,
                    ).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                    total_teen_fsdf_fv.append(teen_fsdf_fv.count())
                    for i in teen_fsdf_fv:
                        total_teen_fsdf_fv.append(Visualization.objects.filter(
                            age__range=(13, 18),
                            active=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        ).exclude(id=i.id).count())
                    
                    adult_fsdf_fv = Visualization.objects.filter(
                        age__range=(19, 60),
                        active=True,
                        sdf_whole_mouth=True,fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    ).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                    total_adult_fsdf_fv.append(adult_fsdf_fv.count())
                    for i in adult_fsdf_fv:
                        total_adult_fsdf_fv.append(Visualization.objects.filter(
                            age__range=(19, 60),
                            active=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        ).exclude(id=i.id).count())
                    
                    old_fsdf_fv = Visualization.objects.filter(
                        age__gt=60,
                        active=True,
                        sdf_whole_mouth=True,fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    ).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                    total_old_fsdf_fv.append(old_fsdf_fv.count())
                    for i in old_fsdf_fv:
                        total_old_fsdf_fv.append(Visualization.objects.filter(
                            age__gt=60,
                            active=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        ).filter(Q(fv=True)|Q(sdf_whole_mouth=True)).filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        ).exclude(id=i.id).count())
                        
                    # SEAL
                    sealant_male_list.append(
                        Visualization.objects.filter(active=True,
                            gender="male",
                            need_sealant=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    sealant_female_list.append(
                        Visualization.objects.filter(active=True,
                            gender="female",
                            need_sealant=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    sealant_child_list.append(
                        Visualization.objects.filter(active=True,
                            age__lt=13,
                            need_sealant=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    sealant_teen_list.append(
                        Visualization.objects.filter(active=True,
                            age__range=(13, 18),
                            need_sealant=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    sealant_adult_list.append(
                        Visualization.objects.filter(active=True,
                            age__range=(19, 60),
                            need_sealant=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    sealant_old_list.append(
                        Visualization.objects.filter(active=True,
                            age__gt=60,
                            need_sealant=True,
                            created_at__range=[start_date, end_date],
                            geography_id=location.id,
                        )
                        .filter(
                            Q(activities_id=health_post)
                            | Q(activities_id=seminar)
                            | Q(activities_id=outreach)
                            | Q(activities_id=outreach)
                        )
                        .count()
                    )
                    
                treatment_male = sum(treatment_male_list)
                treatment_female = sum(treatment_female_list)
                treatment_child = sum(treatment_child_list)
                treatment_teen = sum(treatment_teen_list)
                treatment_adult = sum(treatment_adult_list)
                treatment_old = sum(treatment_old_list)

                sealant_male = sum(sealant_male_list)
                sealant_female = sum(sealant_female_list)
                sealant_child = sum(sealant_child_list)
                sealant_teen = sum(sealant_teen_list)
                sealant_adult = sum(sealant_adult_list)
                sealant_old = sum(sealant_old_list)

                cavities_prevented_male = (
                    0.2 * sum(total_male_fsdf_fv) + 0.1 * sealant_male
                )
                cavities_prevented_female = (
                    0.2 * sum(total_female_fsdf_fv) + 0.1 * sealant_female
                )
                cavities_prevented_child = (
                    0.2 * sum(total_child_fsdf_fv) + 0.1 * sealant_child
                )
                cavities_prevented_teen = (
                    0.2 * sum(total_teen_fsdf_fv) + 0.1 * sealant_teen
                )
                cavities_prevented_adult = (
                    0.2 * sum(total_adult_fsdf_fv) + 0.1 * sealant_adult
                )
                cavities_prevented_old = (
                    0.2 * sum(total_old_fsdf_fv) + 0.1 * sealant_old
                )

                total_cavities = cavities_prevented_male + cavities_prevented_female
                total_contact = treatment_male + treatment_female
                return Response(
                    [
                        [
                            "Number of Cavities Prevented",
                            round(cavities_prevented_male, 2),
                            round(cavities_prevented_female, 2),
                            round(cavities_prevented_child, 2),
                            round(cavities_prevented_teen, 2),
                            round(cavities_prevented_adult, 2),
                            round(cavities_prevented_old, 2),
                            round(total_cavities, 2),
                        ],
                        [
                            "Contacts",
                            treatment_male,
                            treatment_female,
                            treatment_child,
                            treatment_teen,
                            treatment_adult,
                            treatment_old,
                            total_contact,
                        ],
                    ]
                )
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)

# 2.2 Strategic Data
class TreatmentStrategicData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = TreatmentStrategicDataSerializer

    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            encounter_male = (
                Visualization.objects.values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(active=True,
                    gender="male", created_at__range=[last_30_days_obj, today_date_obj]
                )
                .count()
            )
            encounter_female = (
                Visualization.objects.values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(active=True,
                    gender="female",
                    created_at__range=[last_30_days_obj, today_date_obj],
                )
                .count()
            )
            encounter_child = (
                Visualization.objects.values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(active=True,
                    age__lt=13, created_at__range=[last_30_days_obj, today_date_obj]
                )
                .count()
            )
            encounter_teen = (
                Visualization.objects.values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(active=True,
                    age__range=(13, 18),
                    created_at__range=[last_30_days_obj, today_date_obj],
                )
                .count()
            )
            encounter_adult = (
                Visualization.objects.values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(active=True,
                    age__range=(19, 60),
                    created_at__range=[last_30_days_obj, today_date_obj],
                )
                .count()
            )
            encounter_old = (
                Visualization.objects.values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(active=True,
                    age__gt=60, created_at__range=[last_30_days_obj, today_date_obj]
                )
                .count()
            )

            refer_male = Visualization.objects.filter(active=True,
                gender="male",
                refer_hp=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            refer_female = Visualization.objects.filter(active=True,
                gender="female",
                refer_hp=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            refer_child = Visualization.objects.filter(active=True,
                age__lt=13,
                refer_hp=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            refer_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                refer_hp=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            refer_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                refer_hp=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            refer_old = Visualization.objects.filter(active=True,
                age__gt=60,
                refer_hp=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()

            total_seal_male = Visualization.objects.filter(active=True,
                gender="male",
                seal=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_seal_female = Visualization.objects.filter(active=True,
                gender="female",
                seal=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_seal_child = Visualization.objects.filter(active=True,
                age__lt=13,
                seal=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_seal_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                seal=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_seal_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                seal=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_seal_old = Visualization.objects.filter(active=True,
                age__gt=60,
                seal=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()

            totalfv_male = Visualization.objects.filter(active=True,
                gender="male",
                fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            totalfv_female = Visualization.objects.filter(active=True,
                gender="female",
                fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            totalfv_child = Visualization.objects.filter(active=True,
                age__lt=13,
                fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            totalfv_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            totalfv_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            totalfv_old = Visualization.objects.filter(active=True,
                age__gt=60,
                fv=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()

            total_exo_male = Visualization.objects.filter(active=True,
                gender="male",
                exo=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_exo_female = Visualization.objects.filter(active=True,
                gender="female",
                exo=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_exo_child = Visualization.objects.filter(active=True,
                age__lt=13,
                exo=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_exo_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                exo=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_exo_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                exo=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_exo_old = Visualization.objects.filter(active=True,
                age__gt=60,
                exo=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()

            total_art_male = Visualization.objects.filter(active=True,
                gender="male",
                art=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_art_female = Visualization.objects.filter(active=True,
                gender="female",
                art=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_art_child = Visualization.objects.filter(active=True,
                age__lt=13,
                art=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_art_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                art=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_art_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                art=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_art_old = Visualization.objects.filter(active=True,
                age__gt=60,
                art=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()

            total_sdf_male = Visualization.objects.filter(active=True,
                gender="male",
                sdf=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_sdf_female = Visualization.objects.filter(active=True,
                gender="female",
                sdf=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_sdf_child = Visualization.objects.filter(active=True,
                age__lt=13,
                sdf=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_sdf_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                sdf=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_sdf_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                sdf=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_sdf_old = Visualization.objects.filter(active=True,
                age__gt=60,
                sdf=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()

            total_fsdf_male = Visualization.objects.filter(active=True,
                gender="male",
                sdf_whole_mouth=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_fsdf_female = Visualization.objects.filter(active=True,
                gender="female",
                sdf_whole_mouth=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_fsdf_child = Visualization.objects.filter(active=True,
                age__lt=13,
                sdf_whole_mouth=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_fsdf_teen = Visualization.objects.filter(active=True,
                age__range=(13, 18),
                sdf_whole_mouth=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_fsdf_adult = Visualization.objects.filter(active=True,
                age__range=(19, 60),
                sdf_whole_mouth=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()
            total_fsdf_old = Visualization.objects.filter(active=True,
                age__gt=60,
                sdf_whole_mouth=True,
                created_at__range=[last_30_days_obj, today_date_obj],
            ).count()


            # Preventive Ratio
            try:
                preventive_ratio_male = (total_seal_male + totalfv_male + total_fsdf_male) / (
                    total_exo_male + total_art_male + total_sdf_male
                )
            except:
                preventive_ratio_male = 0
            try:
                preventive_ratio_female = (total_seal_female + totalfv_female + total_fsdf_female) / (
                    total_exo_female + total_art_female + total_sdf_female
                )
            except:
                preventive_ratio_female = 0
            try:
                preventive_ratio_child = (total_seal_child + totalfv_child + total_fsdf_child) / (
                    total_exo_child + total_art_child + total_sdf_child
                )
            except:
                preventive_ratio_child = 0
            
            try:
                preventive_ratio_teen = (total_seal_teen + totalfv_teen + total_fsdf_teen) / (
                    total_exo_teen + total_art_teen + total_sdf_teen
                )
            except:
                preventive_ratio_teen = 0

            try:
                preventive_ratio_adult = (total_seal_adult + totalfv_adult + total_fsdf_adult) / (
                    total_exo_adult + total_art_adult + total_sdf_adult
                )
            except:
                preventive_ratio_adult = 0
            try:
                preventive_ratio_old = (total_seal_old + totalfv_old + total_fsdf_old) / (
                    total_exo_old + total_art_old + total_sdf_old
                )
            except:
                preventive_ratio_old = 0

            preventive_ratio_total = preventive_ratio_male + preventive_ratio_female


            # Recal Percentage
            try:
                recall_percent_male = (refer_male / encounter_male) * 100
            except:
                recall_percent_male = 0

            try:
                recall_percent_female = (refer_female / encounter_female) * 100
            except:
                recall_percent_female = 0

            try:
                recall_percent_child = (refer_child / encounter_child) * 100
            except:
                recall_percent_child = 0
            
            try:
                recall_percent_teen = (refer_teen / encounter_teen) * 100
            except:
                recall_percent_teen = 0

            try:
                recall_percent_adult = (refer_adult / encounter_adult) * 100
            except:
                recall_percent_adult = 0

            try:
                recall_percent_old = (refer_old / encounter_old) * 100
            except:
                recall_percent_old = 0

            recall_percent_total = recall_percent_male + recall_percent_female

            # Prevention
            prevention_male_number = total_fsdf_male + total_seal_male + totalfv_male  
            try:
                prevention_male = (prevention_male_number * 100)/ (
                    encounter_male
                )
            except:
                prevention_male = 0
            
            prevention_female_number = total_fsdf_female + total_seal_female + totalfv_female
            try:
                prevention_female = (prevention_female_number * 100 ) / (
                    encounter_female
                )
            except:
                prevention_female = 0
            
            prevention_child_number = total_fsdf_child + total_seal_child + totalfv_child 
            try:
                prevention_child = (prevention_child_number * 100) / (
                    encounter_child
                )
            except:
                prevention_child = 0
            
            prevention_teen_number = total_fsdf_teen + total_seal_teen + totalfv_teen
            try:
                prevention_teen = (prevention_teen_number * 100) / (
                    encounter_teen
                )
            except:
                prevention_teen = 0
            
            prevention_adult_number = total_fsdf_adult + total_seal_adult + totalfv_adult 
            try:
                prevention_adult = (prevention_adult_number * 100) / (
                    encounter_adult
                )
            except:
                prevention_adult = 0
            
            prevention_old_number = total_fsdf_old + total_seal_old + totalfv_old 
            try:
                prevention_old = (prevention_old_number * 100) / (
                    encounter_old
                )
            except:
                prevention_old = 0            

            # Early Intervention Ratio
            try:
                early_intervention_ratio_male = (
                    total_art_male + total_sdf_male
                ) / total_exo_male
            except:
                early_intervention_ratio_male = 0

            try:
                early_intervention_ratio_female = (
                    total_art_female + total_sdf_female
                ) / total_exo_female
            except:
                early_intervention_ratio_female = 0

            try:
                early_intervention_ratio_child = (
                    total_art_child + total_sdf_child
                ) / total_exo_child
            except:
                early_intervention_ratio_child = 0
            
            try:
                early_intervention_ratio_teen = (
                    total_art_teen + total_sdf_teen
                ) / total_exo_teen
            except:
                early_intervention_ratio_teen = 0

            try:
                early_intervention_ratio_adult = (
                    total_art_adult + total_sdf_adult
                ) / total_exo_adult
            except:
                early_intervention_ratio_adult = 0

            try:
                early_intervention_ratio_old = (
                    total_art_old + total_sdf_old
                ) / total_exo_old
            except:
                early_intervention_ratio_old = 0

            early_intervention_ratio_total = (
                early_intervention_ratio_male + early_intervention_ratio_female
            )
            

            # Early intervention  
            early_intervention_male_number = total_art_male + total_sdf_male
            try:
                early_intervention_male = (early_intervention_male_number * 100) / (
                    encounter_male
                )
            except:
                early_intervention_male = 0
            
            early_intervention_female_number = total_art_female + total_sdf_female 
            try:
                early_intervention_female = (early_intervention_female_number * 100) / (
                    encounter_female
                )
            except:
                early_intervention_female = 0
            
            early_intervention_child_number = total_art_child + total_sdf_child
            try:
                early_intervention_child = (early_intervention_child_number * 100) / (
                    encounter_child
                )
            except:
                early_intervention_child = 0
            
            early_intervention_teen_number = total_art_teen + total_sdf_teen 
            try:
                early_intervention_teen = (early_intervention_teen_number * 100) / (
                    encounter_teen
                )
            except:
                early_intervention_teen = 0
            
            early_intervention_adult_number = total_art_adult + total_sdf_adult 
            try:
                early_intervention_adult = (early_intervention_adult_number * 100 ) / (
                    encounter_adult
                )
            except:
                early_intervention_adult = 0
            
            early_intervention_old_number = total_art_old + total_sdf_old
            try:
                early_intervention_old = (early_intervention_old_number * 100) / (
                    encounter_old
                )
            except:
                early_intervention_old = 0
            
            # Surgical intervention  
            surgical_intervention_male_number = total_art_male + total_exo_male + total_sdf_male
            try:
                surgical_intervention_male = (surgical_intervention_male_number * 100) / (
                    encounter_male
                )
            except:
                surgical_intervention_male = 0
            
            surgical_intervention_female_number = total_art_female + total_exo_female + total_sdf_female 
            try:
                surgical_intervention_female = (surgical_intervention_female_number * 100 ) / (
                    encounter_female
                )
            except:
                surgical_intervention_female = 0
            
            surgical_intervention_child_number = total_art_child + total_exo_child + total_sdf_child
            try:
                surgical_intervention_child = (surgical_intervention_child_number * 100) / (
                    encounter_child
                )
            except:
                surgical_intervention_child = 0
            
            surgical_intervention_teen_number = total_art_teen + total_exo_teen + total_sdf_teen 
            try:
                surgical_intervention_teen = (surgical_intervention_teen_number * 100) / (
                    encounter_teen
                )
            except:
                surgical_intervention_teen = 0
            
            surgical_intervention_adult_number = total_art_adult + total_exo_adult + total_sdf_adult 
            try:
                surgical_intervention_adult = (surgical_intervention_adult_number * 100) / (
                    encounter_adult
                )
            except:
                surgical_intervention_adult = 0
            
            surgical_intervention_old_number = total_art_old + total_exo_old + total_sdf_old
            try:
                surgical_intervention_old = (surgical_intervention_old_number * 100) / (
                    encounter_old
                )
            except:
                surgical_intervention_old = 0
            
            surgical_intervention_total = surgical_intervention_male + surgical_intervention_female
            

            prevention_total_number = prevention_male_number + prevention_female_number
            surgical_intervention_total_number = surgical_intervention_male_number + surgical_intervention_female_number
            early_intervention_total_number = early_intervention_male_number + early_intervention_female_number

            total_encounter = encounter_male + encounter_female
            if total_encounter == 0:
                total_encounter = 1
            prevention_total = (prevention_total_number * 100)/total_encounter
            surgical_intervention_total = (surgical_intervention_total_number * 100)/total_encounter
            early_intervention_total = (early_intervention_total_number * 100)/total_encounter
            try:
                preventive_ratio_total = prevention_total_number / surgical_intervention_total_number
            except:
                preventive_ratio_total = 0

            
            return Response(
                [   
                    [
                        "Prevention",
                        str(prevention_male_number) + "(" + str(round(prevention_male, 1)) + "%)",
                        str(prevention_female_number) + "(" + str(round(prevention_female, 1)) + "%)",
                        str(prevention_child_number ) + "(" + str(round(prevention_child, 1)) + "%)",
                        str(prevention_teen_number) + "(" + str(round(prevention_teen, 1)) + "%)",
                        str(prevention_adult_number) + "(" + str(round(prevention_adult, 1)) + "%)",
                        str(prevention_old_number) + "(" + str(round(prevention_old, 1)) + "%)",
                        str(prevention_total_number) + "(" + str(round(prevention_total, 1)) + "%)",
                        
                    ],
                    [
                        "Surgical Intervention",
                        str(surgical_intervention_male_number) + "(" + str(round(surgical_intervention_male, 1)) + "%)",
                        str(surgical_intervention_female_number) + "(" + str(round(surgical_intervention_female, 1)) + "%)",
                        str(surgical_intervention_child_number) + "(" + str(round(surgical_intervention_child, 1)) + "%)",
                        str(surgical_intervention_teen_number) + "(" + str(round(surgical_intervention_teen, 1)) + "%)",
                        str(surgical_intervention_adult_number) + "(" + str(round(surgical_intervention_adult, 1)) + "%)",
                        str(surgical_intervention_old_number) + "(" + str(round(surgical_intervention_old, 1)) + "%)",
                        str(surgical_intervention_total_number) + "(" + str(round(surgical_intervention_total ,1)) + "%)",
                        
                    ],
            
                    [
                        "Preventive Ratio",
                        round(preventive_ratio_male, 1),
                        round(preventive_ratio_female, 1),
                        round(preventive_ratio_child, 1),
                        round(preventive_ratio_teen, 1),
                        round(preventive_ratio_adult, 1),
                        round(preventive_ratio_old, 1),
                        round(preventive_ratio_total, 1),
                    ],
                    
                    [
                        "Early Intervention",
                        str(early_intervention_male_number) + "(" + str(round(early_intervention_male, 1)) + "%)",
                        str(early_intervention_female_number) + "(" + str(round(early_intervention_female, 1)) + "%)",
                        str(early_intervention_child_number) + "(" + str(round(early_intervention_child, 1)) + "%)",
                        str(early_intervention_teen_number) + "(" + str(round(early_intervention_teen, 1)) + "%)",
                        str(early_intervention_adult_number) + "(" + str(round(early_intervention_adult, 1)) + "%)",
                        str(early_intervention_old_number) + "(" + str(round(early_intervention_old, 1)) + "%)",
                        str(early_intervention_total_number) + "(" + str(round(early_intervention_total, 1)) + "%)",
                    ],
                    [
                        "Early Intervention Ratio",
                        round(early_intervention_ratio_male, 1),
                        round(early_intervention_ratio_female, 1),
                        round(early_intervention_ratio_child, 1),
                        round(early_intervention_ratio_teen, 1),
                        round(early_intervention_ratio_adult, 1),
                        round(early_intervention_ratio_old, 1),
                        round(early_intervention_ratio_total, 1),
                    ],
                    [
                        "% Recall",
                        str(round(recall_percent_male, 1)) + "%",
                        str(round(recall_percent_female, 1)) + "%",
                        str(round(recall_percent_child, 1)) + "%",
                        str(round(recall_percent_teen, 1)) + "%",
                        str(round(recall_percent_adult, 1)) + "%",
                        str(round(recall_percent_old, 1)) + "%",
                        str(round(recall_percent_total, 1)) + "%",
                    ],
                ]
            )
        return Response({"treatment_obj": "do not have a permission"}, status=400)

    def post(self, request, format=None):
        serializer = TreatmentStrategicDataSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data["start_date"]))
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            location_list = serializer.validated_data["location"]
            health_post = serializer.validated_data["health_post"]
            seminar = serializer.validated_data["seminar"]
            outreach = serializer.validated_data["outreach"]
            training = serializer.validated_data["training"]

            encounter_male = []
            encounter_female = []
            encounter_child = []
            encounter_teen = []
            encounter_adult = []
            encounter_old = []

            refer_male = []
            refer_female = []
            refer_child = []
            refer_teen = []
            refer_adult = []
            refer_old = []
            total_refer = []

            total_seal_male = []
            total_seal_female = []
            total_seal_child = []
            total_seal_teen = []
            total_seal_adult = []
            total_seal_old = []

            totalfv_male = []
            totalfv_female = []
            totalfv_child = []
            totalfv_teen = []
            totalfv_adult = []
            totalfv_old = []

            total_exo_male = []
            total_exo_female = []
            total_exo_child = []
            total_exo_teen = []
            total_exo_adult = []
            total_exo_old = []

            total_art_male = []
            total_art_female = []
            total_art_child = []
            total_art_teen = []
            total_art_adult = []
            total_art_old = []

            total_sdf_male = []
            total_sdf_female = []
            total_sdf_child = []
            total_sdf_teen = []
            total_sdf_adult = []
            total_sdf_old = []

            total_fsdf_male = []
            total_fsdf_female = []
            total_fsdf_child = []
            total_fsdf_teen = []
            total_fsdf_adult = []
            total_fsdf_old = []

            for location in location_list:
                encounter_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                encounter_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                encounter_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=outreach)
                    )
                    .count()
                )
                encounter_teen.append(
                Visualization.objects.filter(active=True,
                    age__range=(13, 18),
                    created_at__range=[start_date, end_date],
                    geography_id=location.id,
                )
                .values("encounter_id")
                .annotate(Count("encounter_id"))
                .filter(
                    Q(activities_id=health_post)
                    | Q(activities_id=seminar)
                    | Q(activities_id=outreach)
                    | Q(activities_id=training)
                )
                .count()
                )
                encounter_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
               
                encounter_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                refer_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                refer_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                refer_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                refer_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                refer_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                refer_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_refer.append(
                    Visualization.objects.filter(active=True,
                        refer_hp=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    ).count()
                )

                total_seal_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        seal=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                
                total_seal_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        seal=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_seal_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        seal=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_seal_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        seal=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_seal_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        seal=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_seal_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        seal=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                totalfv_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
            
                totalfv_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                totalfv_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                totalfv_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                totalfv_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                totalfv_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        fv=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                total_exo_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        exo=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_exo_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        exo=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_exo_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        exo=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_exo_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        exo=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_exo_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        exo=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                
                total_exo_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        exo=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                total_art_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        art=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_art_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        art=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_art_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        art=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_art_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        art=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_art_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        art=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_art_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        art=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                total_sdf_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        sdf=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                
                total_sdf_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        sdf=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_sdf_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        sdf=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_sdf_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        sdf=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_sdf_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        sdf=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_sdf_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        sdf=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                total_fsdf_male.append(
                    Visualization.objects.filter(active=True,
                        gender="male",
                        sdf_whole_mouth=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                
                total_fsdf_female.append(
                    Visualization.objects.filter(active=True,
                        gender="female",
                        sdf_whole_mouth=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_fsdf_child.append(
                    Visualization.objects.filter(active=True,
                        age__lt=13,
                        sdf_whole_mouth=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_fsdf_teen.append(
                    Visualization.objects.filter(active=True,
                        age__range=(13, 18),
                        sdf_whole_mouth=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_fsdf_adult.append(
                    Visualization.objects.filter(active=True,
                        age__range=(19, 60),
                        sdf_whole_mouth=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )
                total_fsdf_old.append(
                    Visualization.objects.filter(active=True,
                        age__gt=60,
                        sdf_whole_mouth=True,
                        created_at__range=[start_date, end_date],
                        geography_id=location.id,
                    )
                    .filter(
                        Q(activities_id=health_post)
                        | Q(activities_id=seminar)
                        | Q(activities_id=outreach)
                        | Q(activities_id=training)
                    )
                    .count()
                )

                # Preventive Ratio
                try:
                    preventive_ratio_male = (
                        sum(total_seal_male) + sum(totalfv_male) + sum(total_fsdf_male)
                    ) / (
                        sum(total_exo_male)
                        + sum(total_art_male)
                        + sum(total_sdf_male)
                    )
                except:
                    preventive_ratio_male = 0
                try:
                    preventive_ratio_female = (
                        sum(total_seal_female) + sum(totalfv_female) + sum(total_fsdf_female)
                    ) / (
                        sum(total_exo_female)
                        + sum(total_art_female)
                        + sum(total_sdf_female)
                    )
                except:
                    preventive_ratio_female = 0
                try:
                    preventive_ratio_child = (
                        sum(total_seal_child) + sum(totalfv_child) + sum(total_fsdf_child)
                    ) / (
                        sum(total_exo_child)
                        + sum(total_art_child)
                        + sum(total_sdf_child)
                    )
                except:
                    preventive_ratio_child = 0
                try:
                    preventive_ratio_teen = (
                        sum(total_seal_teen) + sum(totalfv_teen) + sum(total_fsdf_teen)
                    ) / (
                        sum(total_exo_teen)
                        + sum(total_art_teen)
                        + sum(total_sdf_teen)
                    )
                except:
                    preventive_ratio_teen = 0
                try:
                    preventive_ratio_adult = (
                        sum(total_seal_adult) + sum(totalfv_adult) + sum(total_fsdf_adult)
                    ) / (
                        sum(total_exo_adult)
                        + sum(total_art_adult)
                        + sum(total_sdf_adult)
                    )
                except:
                    preventive_ratio_adult = 0
                try:
                    preventive_ratio_old = (
                        sum(total_seal_old) + sum(totalfv_old) + sum(total_fsdf_old)
                    ) / (
                        sum(total_exo_old) + sum(total_art_old) + sum(total_sdf_old)
                    )
                except:
                    preventive_ratio_old = 0

                # Early Intervention Ratio
                try:
                    early_intervention_ratio_male = (
                        sum(total_art_male) + sum(total_sdf_male)
                    ) / sum(total_exo_male)
                except:
                    early_intervention_ratio_male = 0

                try:
                    early_intervention_ratio_female = (
                        sum(total_art_female) + sum(total_sdf_female)
                    ) / sum(total_exo_female)
                except:
                    early_intervention_ratio_female = 0

                try:
                    early_intervention_ratio_child = (
                        sum(total_art_child) + sum(total_sdf_child)
                    ) / sum(total_exo_child)
                except:
                    early_intervention_ratio_child = 0
                
                try:
                    early_intervention_ratio_teen = (
                        sum(total_art_teen) + sum(total_sdf_teen)
                    ) / sum(total_exo_teen)
                except:
                    early_intervention_ratio_teen = 0

                try:
                    early_intervention_ratio_adult = (
                        sum(total_art_adult) + sum(total_sdf_adult)
                    ) / sum(total_exo_adult)
                except:
                    early_intervention_ratio_adult = 0

                try:
                    early_intervention_ratio_old = (
                        sum(total_art_old) + sum(total_sdf_old)
                    ) / sum(total_exo_old)
                except:
                    early_intervention_ratio_old = 0

                early_intervention_ratio_total = early_intervention_ratio_male + early_intervention_ratio_female 

                # Recall %
                try:
                    recall_percent_male = (
                        sum(refer_male) / sum(encounter_male)
                    ) * 100
                except:
                    recall_percent_male = 0

                try:
                    recall_percent_female = (
                        sum(refer_female) / sum(encounter_female)
                    ) * 100
                except:
                    recall_percent_female = 0

                try:
                    recall_percent_child = (
                        sum(refer_child) / sum(encounter_child)
                    ) * 100
                except:
                    recall_percent_child = 0
                
                try:
                    recall_percent_teen = (
                        sum(refer_teen) / sum(encounter_teen)
                    ) * 100
                except:
                    recall_percent_teen = 0

                try:
                    recall_percent_adult = (
                        sum(refer_adult) / sum(encounter_adult)
                    ) * 100
                except:
                    recall_percent_adult = 0

                try:
                    recall_percent_old = (sum(refer_old) / sum(encounter_old)) * 100
                except:
                    recall_percent_old = 0

                recall_percent_total = recall_percent_male + recall_percent_female

                # Prevention  
                prevention_male_number = sum(total_fsdf_male) + sum(total_seal_male) + sum(totalfv_male) 
                try:
                    prevention_male = (prevention_male_number * 100) / (
                        sum(encounter_male)
                    )
                except:
                    prevention_male = 0
                
                prevention_female_number = sum(total_fsdf_female) + sum(total_seal_female) + sum(totalfv_female) 
                try:
                    prevention_female = (prevention_female_number * 100) / (
                        sum(encounter_female)
                    )
                except:
                    prevention_female = 0
                
                prevention_child_number = sum(total_fsdf_child) + sum(total_seal_child) + sum(totalfv_child) 
                try:
                    prevention_child = (prevention_child_number *100 ) / (
                        sum(encounter_child)
                    )
                except:
                    prevention_child = 0
                
                prevention_teen_number = sum(total_fsdf_teen) + sum(total_seal_teen) + sum(totalfv_teen) 
                try:
                    prevention_teen = (prevention_teen_number * 100) / (
                        sum(encounter_teen)
                    )
                except:
                    prevention_teen = 0
                
                prevention_adult_number = sum(total_fsdf_adult) + sum(total_seal_adult) + sum(totalfv_adult) 
                try:
                    prevention_adult = (prevention_adult_number * 100) / (
                        sum(encounter_adult)
                    )
                except:
                    prevention_adult = 0
                
                prevention_old_number = sum(total_fsdf_old) + sum(total_seal_old) + sum(totalfv_old) 
                try:
                    prevention_old = (prevention_old_number * 100 ) / (
                        sum(encounter_old)
                    )
                except:
                    prevention_old = 0
                
                # Early intervention  
                early_intervention_male_number = sum(total_art_male) + sum(total_sdf_male)
                try:
                    early_intervention_male = (early_intervention_male_number * 100) / (
                        sum(encounter_male)
                    )
                except:
                    early_intervention_male = 0
                
                early_intervention_female_number = sum(total_art_female) + sum(total_sdf_female) 
                try:
                    early_intervention_female = (early_intervention_female_number * 100 ) / (
                        sum(encounter_female)
                    )
                except:
                    early_intervention_female = 0
                
                early_intervention_child_number = sum(total_art_child) + sum(total_sdf_child)
                try:
                    early_intervention_child = (early_intervention_child_number * 100) / (
                        sum(encounter_child)
                    )
                except:
                    early_intervention_child = 0
                
                early_intervention_teen_number = sum(total_art_teen) + sum(total_sdf_teen) 
                try:
                    early_intervention_teen = (early_intervention_teen_number * 100) / (
                        sum(encounter_teen)
                    )
                except:
                    early_intervention_teen = 0
                
                early_intervention_adult_number = sum(total_art_adult) + sum(total_sdf_adult)
                try:
                    early_intervention_adult = (early_intervention_adult_number * 100) / (
                        sum(encounter_adult)
                    )
                except:
                    early_intervention_adult = 0
                
                early_intervention_old_number = sum(total_art_old) + sum(total_sdf_old)
                try:
                    early_intervention_old = (early_intervention_old_number) / (
                        sum(encounter_old)
                    )
                except:
                    early_intervention_old = 0
                
                # Surgical intervention  
                surgical_intervention_male_number = sum(total_art_male) + sum(total_exo_male) + sum(total_sdf_male)
                try:
                    surgical_intervention_male = (surgical_intervention_male_number *100) / (
                        sum(encounter_male)
                    )
                except:
                    surgical_intervention_male = 0
                
                surgical_intervention_female_number = sum(total_art_female) + sum(total_exo_female) + sum(total_sdf_female) 
                try:
                    surgical_intervention_female = (surgical_intervention_female_number * 100) / (
                        sum(encounter_female)
                    )
                except:
                    surgical_intervention_female = 0
                
                surgical_intervention_child_number = sum(total_art_child) + sum(total_exo_child) + sum(total_sdf_child)
                try:
                    surgical_intervention_child = (surgical_intervention_child_number * 100) / (
                        sum(encounter_child)
                    )
                except:
                    surgical_intervention_child = 0
                
                surgical_intervention_teen_number = sum(total_art_teen) + sum(total_exo_teen) + sum(total_sdf_teen)
                try:
                    surgical_intervention_teen = (surgical_intervention_teen_number * 100 ) / (
                        sum(encounter_teen)
                    )
                except:
                    surgical_intervention_teen = 0
                
                surgical_intervention_adult_number = sum(total_art_adult) + sum(total_exo_adult) + sum(total_sdf_adult) 
                try:
                    surgical_intervention_adult = (surgical_intervention_adult_number * 100) / (
                        sum(encounter_adult)
                    )
                except:
                    surgical_intervention_adult = 0
                
                surgical_intervention_old_number = sum(total_art_old) + sum(total_exo_old) + sum(total_sdf_old)
                try:
                    surgical_intervention_old = (surgical_intervention_old_number * 100) / (
                        sum(encounter_old)
                    )
                except:
                    surgical_intervention_old = 0
                
            total_encounter = sum(encounter_male) + sum(encounter_female)
            if total_encounter == 0:
                total_encounter = 1

            prevention_total_number = prevention_male_number + prevention_female_number
            surgical_intervention_total_number = surgical_intervention_male_number + surgical_intervention_female_number
            early_intervention_total_number = early_intervention_male_number + early_intervention_female_number

            prevention_total = (prevention_total_number * 100)/total_encounter
            surgical_intervention_total = (surgical_intervention_total_number * 100)/total_encounter
            early_intervention_total = (early_intervention_total_number * 100)/total_encounter
            try:
                preventive_ratio_total = prevention_total_number / surgical_intervention_total_number
            except:
                preventive_ratio_total = 0
            return Response(
                [   
                    [
                        "Prevention",
                        str(prevention_male_number) + "(" + str(round(prevention_male, 1)) + "%)",
                        str(prevention_female_number) + "(" + str(round(prevention_female, 1)) + "%)",
                        str(prevention_child_number ) + "(" + str(round(prevention_child, 1)) + "%)",
                        str(prevention_teen_number) + "(" + str(round(prevention_teen, 1)) + "%)",
                        str(prevention_adult_number) + "(" + str(round(prevention_adult, 1)) + "%)",
                        str(prevention_old_number) + "(" + str(round(prevention_old, 1)) + "%)",
                        str(prevention_total_number) + "(" + str(round(prevention_total, 1)) + "%)",
                        
                    ],
                    [
                        "Surgical Intervention",
                        str(surgical_intervention_male_number) + "(" + str(round(surgical_intervention_male, 1)) + "%)",
                        str(surgical_intervention_female_number) + "(" + str(round(surgical_intervention_female, 1)) + "%)",
                        str(surgical_intervention_child_number) + "(" + str(round(surgical_intervention_child, 1)) + "%)",
                        str(surgical_intervention_teen_number) + "(" + str(round(surgical_intervention_teen, 1)) + "%)",
                        str(surgical_intervention_adult_number) + "(" + str(round(surgical_intervention_adult, 1)) + "%)",
                        str(surgical_intervention_old_number) + "(" + str(round(surgical_intervention_old, 1)) + "%)",
                        str(surgical_intervention_total_number) + "(" + str(round(surgical_intervention_total ,1)) + "%)",
                    ],
            
                    [
                        "Preventive Ratio",
                        round(preventive_ratio_male, 1),
                        round(preventive_ratio_female, 1),
                        round(preventive_ratio_child, 1),
                        round(preventive_ratio_teen, 1),
                        round(preventive_ratio_adult, 1),
                        round(preventive_ratio_old, 1),
                        round(preventive_ratio_total, 1),
                    ],
                    
                    [
                        "Early Invertention",
                        str(early_intervention_male_number) + "(" + str(round(early_intervention_male, 1)) + "%)",
                        str(early_intervention_female_number) + "(" + str(round(early_intervention_female, 1)) + "%)",
                        str(early_intervention_child_number) + "(" + str(round(early_intervention_child, 1)) + "%)",
                        str(early_intervention_teen_number) + "(" + str(round(early_intervention_teen, 1)) + "%)",
                        str(early_intervention_adult_number) + "(" + str(round(early_intervention_adult, 1)) + "%)",
                        str(early_intervention_old_number) + "(" + str(round(early_intervention_old, 1)) + "%)",
                        str(early_intervention_total_number) + "(" + str(round(early_intervention_total, 1)) + "%)",
                    ],
                    [
                        "Early Intervention Ratio",
                        round(early_intervention_ratio_male, 1),
                        round(early_intervention_ratio_female, 1),
                        round(early_intervention_ratio_child, 1),
                        round(early_intervention_ratio_teen, 1),
                        round(early_intervention_ratio_adult, 1),
                        round(early_intervention_ratio_old, 1),
                        round(early_intervention_ratio_total, 1),
                    ],
                    [
                        "% Recall",
                        str(round(recall_percent_male, 1)) + "%",
                        str(round(recall_percent_female, 1)) + "%",
                        str(round(recall_percent_child, 1)) + "%",
                        str(round(recall_percent_teen, 1)) + "%",
                        str(round(recall_percent_adult, 1)) + "%",
                        str(round(recall_percent_old, 1)) + "%",
                        str(round(recall_percent_total, 1)) + "%",
                    ],
                ]
            )
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)
