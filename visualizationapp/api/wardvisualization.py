import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from patientapp.models import Patient
from treatmentapp.serializers.visualization import VisualizatioSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.conf import settings
from dental.settings import MEDIA_ROOT
import os
from django.http import JsonResponse
from nepali.datetime import NepaliDate
import datetime
from django.db.models import Q
from treatmentapp.models import Treatment
from encounterapp.models import Encounter, History, Refer, Screeing
from visualizationapp.serializers.ward import WardFilterVisualization,ContactAgeGenderVisualization

from visualizationapp.models import Visualization
from django.db.models import Count
from addressapp.models import Activity

# np_date = NepaliDate()
# d=datetime.date(np_date.npYear(),np_date.npMonth(),np_date.npDay())
# lessthan18 = d - datetime.timedelta(days=365+18)
# greaterthan60 = d - datetime.timedelta(days=365+60)


import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


date = datetime.date.today()
np_date = NepaliDate.from_date(date)
item = np_date.month


class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

# 10.2 Contacts by Age & Gender
class BarGraphView(APIView):
    serializer_class = ContactAgeGenderVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        if CustomUser.objects.select_related("role").filter(
            id=request.user.id, role__name="warduser"
        ):
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            district = ["Kids ≤ 18", "Adult", "Older Adults"]
            total = []
            total_male = []
            total_female = []

            for i in customuser_obj.location.all():
                kid_total = Visualization.objects.filter(active=True,
                    geography_id=i.id, age__lt=18
                ).count()
                kid_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, gender="male", age__lt=18
                ).count()
                kid_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, gender="female", age__lt=18
                ).count()

                adult_total = Visualization.objects.filter(active=True,
                    geography_id=i.id,age__range=(19, 60)
                ).count()
                adult_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, gender="male", age__range=(19, 60)
                ).count()
                adult_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, gender="female", age__range=(19, 60)
                ).count()

                old_total = Visualization.objects.filter(active=True,
                    geography_id=i.id, age__gt=60
                ).count()
                old_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, gender="male", age__gt=60
                ).count()
                old_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, gender="female", age__gt=60
                ).count()

                total.append(kid_total)
                total.append(adult_total)
                total.append(old_total)

                total_male.append(kid_male)
                total_male.append(adult_male)
                total_male.append(old_male)

                total_female.append(kid_female)
                total_female.append(adult_female)
                total_female.append(old_female)

            locationChart = {
                "data": {
                    "labels": district,
                    "datasets": [
                        {
                            "label": "Total",
                            "backgroundColor": "rgba(255, 206, 86, 0.2)",
                            "borderColor": "rgba(255, 206, 86, 1)",
                            "borderWidth": 1,
                            "data": total,
                        },
                        {
                            "label": "Male",
                            "backgroundColor": "rgba(239, 62, 54, 0.2)",
                            "borderColor": "rgba(239, 62, 54, 1)",
                            "borderWidth": 1,
                            "data": total_male,
                        },
                        {
                            "label": "Female",
                            "backgroundColor": "rgba(64, 224, 208, 0.2)",
                            "borderColor": "rgba(64, 224, 208, 1)",
                            "borderWidth": 1,
                            "data": total_female,
                        }
                    ],
                },
                "options": {
                    "aspectRatio": 1.5,
                    "scales": {"yAxes": [{"ticks": {"beginAtZero": "true"}}]},
                    "title": {
                        "display": "true",
                        # 'text': "Age-wise Gender Distribution",
                        "fontSize": 18,
                        "fontFamily": "'Palanquin', sans-serif",
                    },
                    "legend": {
                        "display": "true",
                        "position": "bottom",
                        "labels": {
                            "usePointStyle": "true",
                            "padding": 20,
                            "fontFamily": "'Maven Pro', sans-serif",
                        },
                    },
                },
            }
            return Response({"locationChart": locationChart})
        return Response({"message": "only ward user can see"}, status=400)

    def post(self, request, format=None):
        serializer = ContactAgeGenderVisualization(data=request.data, context={"request": request})

        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data["start_date"]))
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))

            if CustomUser.objects.select_related("role").filter(id=request.user.id, role__name="warduser"):
                customuser_obj = CustomUser.objects.get(id=request.user.id)
                if end_date > start_date:
                    district = ["Kids", "Adults", "Older Adults"]
                    total = []
                    total_male = []
                    total_female = []


                    for i in customuser_obj.location.all():
                        kid_total = Visualization.objects.filter(active=True,
                            geography_id=i.id, age__lt=18,created_at__range=[start_date, end_date]
                        ).count()
                        kid_male = Visualization.objects.filter(active=True,
                            geography_id=i.id, gender="male", age__lt=18,created_at__range=[start_date, end_date]
                        ).count()
                        kid_female = Visualization.objects.filter(active=True,
                            geography_id=i.id, gender="female", age__lt=18,created_at__range=[start_date, end_date]
                        ).count()

                        adult_total = Visualization.objects.filter(active=True,
                            geography_id=i.id,age__range=(19, 60),created_at__range=[start_date, end_date]
                        ).count()
                        adult_male = Visualization.objects.filter(active=True,
                            geography_id=i.id, gender="male", age__range=(19, 60),created_at__range=[start_date, end_date]
                        ).count()
                        adult_female = Visualization.objects.filter(active=True,
                            geography_id=i.id, gender="female", age__range=(19, 60),created_at__range=[start_date, end_date]
                        ).count()

                        old_total = Visualization.objects.filter(active=True,
                            geography_id=i.id, age__gt=60,created_at__range=[start_date, end_date]
                        ).count()
                        old_male = Visualization.objects.filter(active=True,
                            geography_id=i.id, gender="male", age__gt=60,created_at__range=[start_date, end_date]
                        ).count()
                        old_female = Visualization.objects.filter(active=True,
                            geography_id=i.id, gender="female", age__gt=60,created_at__range=[start_date, end_date]
                        ).count()

                        total.append(kid_total)
                        total.append(adult_total)
                        total.append(old_total)

                        total_male.append(kid_male)
                        total_male.append(adult_male)
                        total_male.append(old_male)

                        total_female.append(kid_female)
                        total_female.append(adult_female)
                        total_female.append(old_female)

                    locationChart = {
                        "data": {
                            "labels": district,
                            "datasets": [
                                {
                                    "label": "Total",
                                    "backgroundColor": "rgba(255, 206, 86, 0.2)",
                                    "borderColor": "rgba(255, 206, 86, 1)",
                                    "borderWidth": 1,
                                    "data": total,
                                },
                                {
                                    "label": "Male",
                                    "backgroundColor": "rgba(239, 62, 54, 0.2)",
                                    "borderColor": "rgba(239, 62, 54, 1)",
                                    "borderWidth": 1,
                                    "data": total_male,
                                },
                                {
                                    "label": "Female",
                                    "backgroundColor": "rgba(64, 224, 208, 0.2)",
                                    "borderColor": "rgba(64, 224, 208, 1)",
                                    "borderWidth": 1,
                                    "data": total_female,
                                }
                            ],
                        },
                        "options": {
                            "aspectRatio": 1.5,
                            "scales": {"yAxes": [{"ticks": {"beginAtZero": "true"}}]},
                            "title": {
                                "display": "true",
                                # 'text': "Age-wise Gender Distribution",
                                "fontSize": 18,
                                "fontFamily": "'Palanquin', sans-serif",
                            },
                            "legend": {
                                "display": "true",
                                "position": "bottom",
                                "labels": {
                                    "usePointStyle": "true",
                                    "padding": 20,
                                    "fontFamily": "'Maven Pro', sans-serif",
                                },
                            },
                        },
                    }
                    return Response({"locationChart": locationChart})
                return Response({"message": "End date must be greater than Start Date"}, status=400)
            return Response({"message": "only ward user can see"}, status=400)
        return Response({"message": serializer.errors}, status=400)


# i think we dont need this api
class BarGraphFilterView(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def post(self, request, format=None):
        serializer = WardFilterVisualization(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    district = ["Kids ≤ 18", "Adults", "Other Adults"]
                    total = []
                    male = []
                    female = []
                    for i in customuser_obj.location.all():
                        for activities in activities_list:
                            female_child = Visualization.objects.filter(active=True,
                                activities_id=activities.id,
                                geography_id=i.id,
                                gender="female",
                                age__lt=18,
                                created_at__range=[start_date, end_date],
                            ).count()
                            female_adult = Visualization.objects.filter(active=True,
                                activities_id=activities.id,
                                geography_id=i.id,
                                gender="female",
                                age__range=(19, 60),
                                created_at__range=[start_date, end_date],
                            ).count()
                            male_adult = Visualization.objects.filter(active=True,
                                activities_id=activities.id,
                                geography_id=i.id,
                                gender="male",
                                age__range=(19, 60),
                                created_at__range=[start_date, end_date],
                            ).count()
                            male_child = Visualization.objects.filter(active=True,
                                activities_id=activities.id,
                                geography_id=i.id,
                                gender="male",
                                age__lt=18,
                                created_at__range=[start_date, end_date],
                            ).count()
                            old_male = Visualization.objects.filter(active=True,
                                activities_id=activities.id,
                                geography_id=i.id,
                                gender="male",
                                age__gt=60,
                                created_at__range=[start_date, end_date],
                            ).count()
                            old_female = Visualization.objects.filter(active=True,
                                activities_id=activities.id,
                                geography_id=i.id,
                                gender="female",
                                age__gt=60,
                                created_at__range=[start_date, end_date],
                            ).count()
                            male.append(male_child)
                            male.append(male_adult)
                            male.append(old_male)
                            female.append(female_child)
                            female.append(female_adult)
                            female.append(old_female)
                            total.append(female_child + male_child)
                            total.append(female_adult + male_adult)
                            total.append(old_female + old_male)
                        locationChart = {
                            "data": {
                                "labels": district,
                                "datasets": [
                                    {
                                        "label": "Total",
                                        "backgroundColor": "rgba(255, 206, 86, 0.2)",
                                        "borderColor": "rgba(255, 206, 86, 1)",
                                        "borderWidth": 1,
                                        "data": [sum(total)],
                                    },
                                    {
                                        "label": "Female",
                                        "backgroundColor": "rgba(239, 62, 54, 0.2)",
                                        "borderColor": "rgba(239, 62, 54, 1)",
                                        "borderWidth": 1,
                                        "data": [sum(female)],
                                    },
                                    {
                                        "label": "Male",
                                        "backgroundColor": "rgba(64, 224, 208, 0.2)",
                                        "borderColor": "rgba(64, 224, 208, 1)",
                                        "borderWidth": 1,
                                        "data": [sum(male)],
                                    },
                                ],
                            },
                            "options": {
                                "aspectRatio": 1.5,
                                "scales": {
                                    "yAxes": [{"ticks": {"beginAtZero": "true"}}]
                                },
                                "title": {
                                    "display": "true",
                                    # 'text': "Age-wise Gender Distribution",
                                    "fontSize": 18,
                                    "fontFamily": "'Palanquin', sans-serif",
                                },
                                "legend": {
                                    "display": "true",
                                    "position": "bottom",
                                    "labels": {
                                        "usePointStyle": "true",
                                        "padding": 20,
                                        "fontFamily": "'Maven Pro', sans-serif",
                                    },
                                },
                            },
                        }
                    return Response({"locationChart": locationChart})
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)


# Basic Data  
class WardTreatmentTableVisualization1(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        if (
            CustomUser.objects.select_related("role")
            .filter(id=request.user.id, role__name="warduser")
            .exists()
        ):
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                total_treatment = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,geography_id=i.id)
                    .count()
                )
                treatment_male = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,gender="male", geography_id=i.id)
                    .count()
                )
                treatment_female = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,gender="female", geography_id=i.id)
                    .count()
                )
                treatment_child = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,age__lt=12, geography_id=i.id)
                    .count()
                )
                treatment_teen = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,age__range=(13, 18), geography_id=i.id)
                    .count()
                )
                treatment_adult = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,age__range=(19, 60), geography_id=i.id)
                    .count()
                )
                treatment_old = (
                    Visualization.objects.values("encounter_id")
                    .annotate(Count("encounter_id"))
                    .filter(active=True,age__gt=60, geography_id=i.id)
                    .count()
                )

                
                male_patients_receiving_FV = Visualization.objects.filter(active=True,
                    gender="male", fv=True, geography_id=i.id
                ).count()
                female_patients_receiving_FV = Visualization.objects.filter(active=True,
                    gender="female", fv=True, geography_id=i.id
                ).count()
                child__patients_receiving_FV = Visualization.objects.filter(active=True,
                    age__lt=12, fv=True, geography_id=i.id
                ).count()
                teen__patients_receiving_FV = Visualization.objects.filter(active=True,
                    age__range=(13, 18), fv=True, geography_id=i.id
                ).count()
                adult__patients_receiving_FV = Visualization.objects.filter(active=True,
                    age__range=(19, 60), fv=True, geography_id=i.id
                ).count()
                old__patients_receiving_FV = Visualization.objects.filter(active=True,
                    age__gt=60, fv=True, geography_id=i.id
                ).count()

                sealant_male = Visualization.objects.filter(active=True,
                    gender="male", need_sealant=True, geography_id=i.id
                ).count()
                sealant_female = Visualization.objects.filter(active=True,
                    gender="female", need_sealant=True, geography_id=i.id
                ).count()
                sealant_child = Visualization.objects.filter(active=True,
                    age__lt=12, need_sealant=True, geography_id=i.id
                ).count()
                sealant_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), need_sealant=True, geography_id=i.id
                ).count()
                sealant_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), need_sealant=True, geography_id=i.id
                ).count()
                sealant_old = Visualization.objects.filter(active=True,
                    age__gt=60, need_sealant=True, geography_id=i.id
                ).count()

                cavities_prevented_male = (
                    0.2 * male_patients_receiving_FV + 0.1 * sealant_male
                )
                cavities_prevented_female = (
                    0.2 * female_patients_receiving_FV + 0.1 * sealant_female
                )
                cavities_prevented_child = (
                    0.2 * child__patients_receiving_FV + 0.1 * sealant_child
                )
                cavities_prevented_teen = (
                    0.2 * teen__patients_receiving_FV + 0.1 * sealant_teen
                )
                cavities_prevented_adult = (
                    0.2 * adult__patients_receiving_FV + 0.1 * sealant_adult
                )
                cavities_prevented_old = (
                    0.2 * old__patients_receiving_FV + 0.1 * sealant_old
                )
                total_cavities = cavities_prevented_male + cavities_prevented_female
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
                            round(treatment_male, 2),
                            round(treatment_female, 2),
                            round(treatment_child, 2),
                            round(treatment_teen, 2),
                            round(treatment_adult, 2),
                            round(treatment_old, 2),
                            round(total_treatment, 2),
                        ],
                    ]
                )
        return Response({"treatment_obj": "do not have a permission"}, status=400)

    def post(self, request, format=None):
        serializer = WardFilterVisualization(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    total_treatment = []
                    treatment_male = []
                    treatment_female = []
                    treatment_child = []
                    treatment_teen = []
                    treatment_adult = []
                    treatment_old = []

                    female_patients_receiving_FV = []
                    male_patients_receiving_FV = []
                    child__patients_receiving_FV = []
                    teen__patients_receiving_FV = []
                    adult__patients_receiving_FV = []
                    old__patients_receiving_FV = []

                    sealant_male = []
                    sealant_female = []
                    sealant_child = []
                    sealant_teen = []
                    sealant_adult = []
                    sealant_old = []

                    for activities in activities_list:
                        for i in customuser_obj.location.all():
                            total_treatment.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )
                            treatment_male.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    gender="male",
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )
                            treatment_female.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    gender="female",
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )
                            treatment_child.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    age__lt=12,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )
                            treatment_teen.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    age__range=(13, 18),
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )
                            treatment_adult.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    age__range=(19, 60),
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )
                            treatment_old.append(
                                Visualization.objects.values("encounter_id")
                                .annotate(Count("encounter_id"))
                                .filter(active=True,
                                    age__gt=60,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                )
                                .count()
                            )

                            female_patients_receiving_FV.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            male_patients_receiving_FV.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            child__patients_receiving_FV.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            teen__patients_receiving_FV.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            adult__patients_receiving_FV.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            old__patients_receiving_FV.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            sealant_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    need_sealant=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            sealant_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    need_sealant=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            sealant_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    need_sealant=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            sealant_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    need_sealant=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            sealant_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    need_sealant=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            sealant_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    need_sealant=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                    cavities_prevented_male = (
                        0.2 * sum(male_patients_receiving_FV) + 0.1 * sum(sealant_male)
                    )
                    cavities_prevented_female = (
                        0.2
                        * sum(female_patients_receiving_FV)
                        + 0.1
                        * sum(sealant_female)
                    )
                    cavities_prevented_child = (
                        0.2
                        * sum(child__patients_receiving_FV)
                        + 0.1
                        * sum(sealant_child)
                    )
                    cavities_prevented_teen = (
                        0.2
                        * sum(teen__patients_receiving_FV)
                        + 0.1
                        * sum(sealant_teen)
                    )
                    cavities_prevented_adult = (
                        0.2
                        * sum(adult__patients_receiving_FV)
                        + 0.1
                        * sum(sealant_adult)
                    )
                    cavities_prevented_old = (
                        0.2 * sum(old__patients_receiving_FV) + 0.1 * sum(sealant_old)
                    )
                    total_cavities = cavities_prevented_male + cavities_prevented_female
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
                                round(sum(treatment_male), 2),
                                round(sum(treatment_female), 2),
                                round(sum(treatment_child), 2),
                                round(sum(treatment_teen), 2),
                                round(sum(treatment_adult), 2),
                                round(sum(treatment_old), 2),
                                round(sum(total_treatment), 2),
                            ],
                        ]
                    )
                return Response(
                    {"treatment_obj": "do not have a permission"}, status=400
                )
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)



# Overview
class WardTableVisualization2(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        if (CustomUser.objects.select_related("role").filter(id=request.user.id, role__name="warduser").exists()):
            total_male = []
            total_exo_male = []
            total_art_male = []
            total_seal_male = []
            total_sdf_male = []
            total_fv_male = []
            total_fm_sdf_male = []
            total_ref_hp_male = []
            total_ref_other_male = []

            total_female = []
            total_exo_female = []
            total_art_female = []
            total_seal_female = []
            total_sdf_female = []
            total_fv_female = []
            total_fm_sdf_female = []
            total_ref_hp_female = []
            total_ref_other_female = []

            total_children = []
            total_exo_child = []
            total_art_child = []
            total_seal_child = []
            total_sdf_child = []
            total_fv_child = []
            total_fm_sdf_child = []
            total_ref_hp_child = []
            total_ref_other_child = []

            total_teen = []
            total_exo_teen = []
            total_art_teen = []
            total_seal_teen = []
            total_sdf_teen = []
            total_fv_teen = []
            total_fm_sdf_teen = []
            total_ref_hp_teen = []
            total_ref_other_teen = []

            total_adult = []
            total_exo_adult = []
            total_art_adult = []
            total_seal_adult = []
            total_sdf_adult = []
            total_fv_adult = []
            total_fm_sdf_adult = []
            total_ref_hp_adult = []
            total_ref_other_adult = []

            total_older_adult = []
            total_exo_old = []
            total_art_old = []
            total_seal_old = []
            total_sdf_old = []
            total_fv_old = []
            total_fm_sdf_old = []
            total_ref_hp_old = []
            total_ref_other_old = []

            total_encounter = []
            total_exo = []
            total_art = []
            total_seal = []
            total_sdf = []
            total_fv = []
            total_fm_sdf = []
            total_ref_hp = []
            total_ref_other = []


            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                male = Visualization.objects.filter(active=True,
                    gender="male",geography_id=i.id
                ).count()
                total_male.append(male)
                female = Visualization.objects.filter(active=True,
                    gender="female",geography_id=i.id
                ).count()
                total_female.append(female)
                children = Visualization.objects.filter(active=True,
                    age__lt=13,geography_id=i.id
                ).count()
                total_children.append(children)
                teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18),geography_id=i.id
                ).count()
                total_teen.append(teen)
                adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60),geography_id=i.id
                ).count()
                total_adult.append(adult)
                older_adult = Visualization.objects.filter(active=True,
                    age__gt=60,geography_id=i.id
                ).count()
                total_older_adult.append(older_adult)
                encounter = male + female
                total_encounter.append(encounter)

                sdf = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True
                ).count()
                total_sdf.append(sdf)
                sdf_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, gender="male"
                ).count()
                total_sdf_male.append(sdf_male)
                sdf_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, gender="female"
                ).count()
                total_sdf_female.append(sdf_female)
                sdf_child = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, age__lt=13
                ).count()
                total_sdf_child.append(sdf_child)
                sdf_teen = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, age__range=(13, 18)
                ).count()
                total_sdf_teen.append(sdf_teen)
                sdf_adult = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, age__range=(19, 60)
                ).count()
                total_sdf_adult.append(sdf_adult)
                sdf_old = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, age__gt=60
                ).count()
                total_sdf_old.append(sdf_old)

                seal = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True
                ).count()
                total_seal.append(seal)
                seal_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, gender="male"
                ).count()
                total_seal_male.append(seal_male)
                seal_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, gender="female"
                ).count()
                total_seal_female.append(seal_female)
                seal_child = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, age__lt=13
                ).count()
                total_seal_child.append(seal_child)
                seal_teen = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, age__range=(13, 18)
                ).count()
                total_seal_teen.append(seal_teen)
                seal_adult = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, age__range=(19, 60)
                ).count()
                total_seal_adult.append(seal_adult)
                seal_old = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, age__gt=60
                ).count()
                total_seal_old.append(seal_old)

                art = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True
                ).count()
                total_art.append(art)
                art_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, gender="male"
                ).count()
                total_art_male.append(art_male)
                art_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, gender="female"
                ).count()
                total_art_female.append(art_female)
                art_child = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, age__lt=13
                ).count()
                total_art_child.append(art_child)
                art_teen = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, age__range=(13, 18)
                ).count()
                total_art_teen.append(art_teen)
                art_adult = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, age__range=(19, 60)
                ).count()
                total_art_adult.append(art_adult)
                art_old = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, age__gt=60
                ).count()
                total_art_old.append(art_old)

                exo = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True
                ).count()
                total_exo.append(exo)
                exo_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, gender="male"
                ).count()
                total_exo_male.append(exo_male)
                exo_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, gender="female"
                ).count()
                total_exo_female.append(exo_female)
                exo_child = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, age__lt=13
                ).count()
                total_exo_child.append(exo_child)
                exo_teen = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, age__range=(13, 18)
                ).count()
                total_exo_teen.append(exo_teen)
                exo_adult = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, age__range=(19, 60)
                ).count()
                total_exo_adult.append(exo_adult)
                exo_old = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, age__gt=60
                ).count()
                total_exo_old.append(exo_old)

                fv = Visualization.objects.filter(active=True,
                    fv=True, geography_id=i.id
                ).count()
                total_fv.append(fv)
                fv_male = Visualization.objects.filter(active=True,
                    gender="male", fv=True, geography_id=i.id
                ).count()
                total_fv_male.append(fv_male)
                fv_female = Visualization.objects.filter(active=True,
                    gender="female", fv=True, geography_id=i.id
                ).count()
                total_fv_female.append(fv_female)
                fv_child = Visualization.objects.filter(active=True,
                    age__lt=13, fv=True, geography_id=i.id
                ).count()
                total_fv_child.append(fv_child)
                fv_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), fv=True, geography_id=i.id
                ).count()
                total_fv_teen.append(fv_teen)
                fv_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), fv=True, geography_id=i.id
                ).count()
                total_fv_adult.append(fv_adult)
                fv_old = Visualization.objects.filter(active=True,
                    age__gt=60, fv=True, geography_id=i.id
                ).count()
                total_fv_old.append(fv_old)

                fm_sdf = Visualization.objects.filter(active=True,
                    sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf.append(fm_sdf)
                fm_sdf_male = Visualization.objects.filter(active=True,
                    gender="male", sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf_male.append(fm_sdf_male)
                fm_sdf_female = Visualization.objects.filter(active=True,
                    gender="female", sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf_female.append(fm_sdf_female)
                fm_sdf_child = Visualization.objects.filter(active=True,
                    age__lt=13, sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf_child.append(fm_sdf_child)
                fm_sdf_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 60), sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf_teen.append(fm_sdf_teen)
                fm_sdf_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf_adult.append(fm_sdf_adult)
                fm_sdf_old = Visualization.objects.filter(active=True,
                    age__gt=60, sdf_whole_mouth=True, geography_id=i.id
                ).count()
                total_fm_sdf_old.append(fm_sdf_old)

                ref_hp = Visualization.objects.filter(active=True,
                    refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp.append(ref_hp)
                ref_hp_male = Visualization.objects.filter(active=True,
                    gender="male", refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp_male.append(ref_hp_male)
                ref_hp_female = Visualization.objects.filter(active=True,
                    gender="female", refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp_female.append(ref_hp_female)
                ref_hp_child = Visualization.objects.filter(active=True,
                    age__lt=13, refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp_child.append(ref_hp_child)
                ref_hp_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp_teen.append(ref_hp_teen)
                ref_hp_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp_adult.append(ref_hp_adult)
                ref_hp_old = Visualization.objects.filter(active=True,
                    age__gt=60, refer_hp=True, geography_id=i.id
                ).count()
                total_ref_hp_old.append(ref_hp_old)


                ref_other = Visualization.objects.filter(active=True,
                    refer_other=True, geography_id=i.id
                ).count()
                total_ref_other.append(ref_other)
                ref_other_male = Visualization.objects.filter(active=True,
                    gender="male", refer_other=True, geography_id=i.id
                ).count()
                total_ref_other_male.append(ref_other_male)
                ref_other_female = Visualization.objects.filter(active=True,
                    gender="female", refer_other=True, geography_id=i.id
                ).count()
                total_ref_other_female.append(ref_other_female)
                ref_other_child = Visualization.objects.filter(active=True,
                    age__lt=13, refer_other=True, geography_id=i.id
                ).count()
                total_ref_other_child.append(ref_other_child)
                ref_other_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), refer_other=True, geography_id=i.id
                ).count()
                total_ref_other_teen.append(ref_other_teen)
                ref_other_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), refer_other=True, geography_id=i.id
                ).count()
                total_ref_other_adult.append(ref_other_adult)
                ref_other_old = Visualization.objects.filter(active=True,
                    age__gt=60, refer_other=True, geography_id=i.id
                ).count()
                total_ref_other_old.append(ref_other_old)


            return Response(
                [
                    {   
                        "isActive": "true",
                        "type":"Total",
                        "Check":sum(total_encounter),
                        "EXO":sum(total_exo),
                        "ART":sum(total_art),
                        "SEAL":sum(total_seal),
                        "SDF":sum(total_sdf),
                        "FM-SDF":sum(total_fm_sdf),
                        "FV":sum(total_fv),
                        "Ref_HP":sum(total_ref_hp),
                        "Ref_Other":sum(total_ref_other)
                    },
                    
                    {   
                        "isActive": "true",
                        "type":"Child ≤ 12Y",
                        "Check":sum(total_children),
                        "EXO":sum(total_exo_child),
                        "ART":sum(total_art_child),
                        "SEAL":sum(total_seal_child),
                        "SDF":sum(total_sdf_child),
                        "FM-SDF":sum(total_fm_sdf_child),
                        "FV":sum(total_fv_child),
                        "Ref_HP":sum(total_ref_hp_child),
                        "Ref_Other":sum(total_ref_other_child),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        },
                    },

                    {   
                        "isActive": "true",
                        "type":"Teen 13-18 Y",
                        "Check":sum(total_teen),
                        "EXO":sum(total_exo_teen),
                        "ART":sum(total_art_teen),
                        "SEAL":sum(total_seal_teen),
                        "SDF":sum(total_sdf_teen),
                        "FM-SDF":sum(total_fm_sdf_teen),
                        "FV":sum(total_fv_teen),
                        "Ref_HP":sum(total_ref_hp_teen),
                        "Ref_Other":sum(total_ref_other_teen),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        }
                        
                    },
                    
                    {   
                        "isActive": "true",
                        "type":"Adult 19 - 60 Y",
                        "Check":sum(total_adult),
                        "EXO":sum(total_exo_adult),
                        "ART":sum(total_art_adult),
                        "SEAL":sum(total_seal_adult),
                        "SDF":sum(total_sdf_adult),
                        "FM-SDF":sum(total_fm_sdf_adult),
                        "FV":sum(total_fv_adult),
                        "Ref_HP":sum(total_ref_hp_adult),
                        "Ref_Other":sum(total_ref_other_adult),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        }
                        
                    },
                    {   
                        "isActive": "true",
                        "type":"Older Adult ≥ 61 Y",
                        "Check":sum(total_older_adult),
                        "EXO":sum(total_exo_old),
                        "ART":sum(total_art_old),
                        "SEAL":sum(total_seal_old),
                        "SDF":sum(total_sdf_old),
                        "FM-SDF":sum(total_fm_sdf_old),
                        "FV":sum(total_fv_old),
                        "Ref_HP":sum(total_ref_hp_old),
                        "Ref_Other":sum(total_ref_other_old),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        }
                    },

                    {
                        "isActive": "true",
                        "type":"Male",
                        "Check":sum(total_male),
                        "EXO":sum(total_exo_male),
                        "ART":sum(total_art_male),
                        "SEAL":sum(total_seal_male),
                        "SDF":sum(total_sdf_male),
                        "FM-SDF":sum(total_fm_sdf_male),
                        "FV":sum(total_fv_male),
                        "Ref_HP":sum(total_ref_hp_male),
                        "Ref_Other":sum(total_ref_other_male),
                        "_cellVariants": {
                                "Check": "info",
                                "EXO": "info",
                                "ART": "info",
                                "SEAL": "info",
                                "SDF": "info",
                                "FM-SDF": "info",
                                "FV": "info",
                                "Ref_HP": "info",
                                "Ref_Other": "info",
                            }
                    },
                    {   
                        "isActive": "true",
                        "type":"Female",
                        "Check":sum(total_female),
                        "EXO":sum(total_exo_female),
                        "ART":sum(total_art_female),
                        "SEAL":sum(total_seal_female),
                        "SDF":sum(total_sdf_female),
                        "FM-SDF":sum(total_fm_sdf_female),
                        "FV":sum(total_fv_female),
                        "Ref_HP":sum(total_ref_hp_female),
                        "Ref_Other":sum(total_ref_other_female),
                        "_cellVariants": {
                                "Check": "info",
                                "EXO": "info",
                                "ART": "info",
                                "SEAL": "info",
                                "SDF": "info",
                                "FM-SDF": "info",
                                "FV": "info",
                                "Ref_HP": "info",
                                "Ref_Other": "info",
                        }
                    }
                ]
            )
        return Response({"treatment_obj": "do not have a permission"}, status=400)

    def post(self, request, format=None):
        serializer = WardFilterVisualization(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            print("+++++++++++++++++++++++==")
            print(start_date)
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            print(end_date)
            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)

                    total_male = []
                    total_exo_male = []
                    total_art_male = []
                    total_seal_male = []
                    total_sdf_male = []
                    total_fv_male = []
                    total_fm_sdf_male = []
                    total_ref_hp_male = []
                    total_ref_other_male = []

                    total_female = []
                    total_exo_female = []
                    total_art_female = []
                    total_seal_female = []
                    total_sdf_female = []
                    total_fv_female = []
                    total_fm_sdf_female = []
                    total_ref_hp_female = []
                    total_ref_other_female = []

                    total_children = []
                    total_exo_child = []
                    total_art_child = []
                    total_seal_child = []
                    total_sdf_child = []
                    total_fv_child = []
                    total_fm_sdf_child = []
                    total_ref_hp_child = []
                    total_ref_other_child = []

                    total_teen = []
                    total_exo_teen = []
                    total_art_teen = []
                    total_seal_teen = []
                    total_sdf_teen = []
                    total_fv_teen = []
                    total_fm_sdf_teen = []
                    total_ref_hp_teen = []
                    total_ref_other_teen = []

                    total_adult = []
                    total_exo_adult = []
                    total_art_adult = []
                    total_seal_adult = []
                    total_sdf_adult = []
                    total_fv_adult = []
                    total_fm_sdf_adult = []
                    total_ref_hp_adult = []
                    total_ref_other_adult = []

                    total_older_adult = []
                    total_exo_old = []
                    total_art_old = []
                    total_seal_old = []
                    total_sdf_old = []
                    total_fv_old = []
                    total_fm_sdf_old = []
                    total_ref_hp_old = []
                    total_ref_other_old = []

                    total_encounter = []
                    total_exo = []
                    total_art = []
                    total_seal = []
                    total_sdf = []
                    total_fv = []
                    total_fm_sdf = []
                    total_ref_hp = []
                    total_ref_other = []

                    for i in customuser_obj.location.all():
                        for activities in activities_list:
                            male = Visualization.objects.filter(active=True,
                                gender="male",geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_male.append(male)
                            female = Visualization.objects.filter(active=True,
                                gender="female",geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_female.append(female)
                            children = Visualization.objects.filter(active=True,
                                age__lt=13,geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_children.append(children)
                            teen = Visualization.objects.filter(active=True,
                                age__range=(13, 18),geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_teen.append(teen)
                            adult = Visualization.objects.filter(active=True,
                                age__range=(19, 60),geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_adult.append(adult)
                            older_adult = Visualization.objects.filter(active=True,
                                age__gt=60,geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_older_adult.append(older_adult)
                            encounter = male + female
                            total_encounter.append(encounter)

                            sdf = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf.append(sdf)
                            sdf_male = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True, gender="male",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf_male.append(sdf_male)
                            sdf_female = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True, gender="female",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf_female.append(sdf_female)
                            sdf_child = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True, age__lt=13,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf_child.append(sdf_child)
                            sdf_teen = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True, age__range=(13, 18),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf_teen.append(sdf_teen)
                            sdf_adult = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True, age__range=(19, 60),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf_adult.append(sdf_adult)
                            sdf_old = Visualization.objects.filter(active=True,
                                geography_id=i.id, sdf=True, age__gt=60,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_sdf_old.append(sdf_old)

                            seal = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal.append(seal)
                            seal_male = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True, gender="male",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal_male.append(seal_male)
                            seal_female = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True, gender="female",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal_female.append(seal_female)
                            seal_child = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True, age__lt=13,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal_child.append(seal_child)
                            seal_teen = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True, age__range=(13, 18),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal_teen.append(seal_teen)
                            seal_adult = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True, age__range=(19, 60),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal_adult.append(seal_adult)
                            seal_old = Visualization.objects.filter(active=True,
                                geography_id=i.id, seal=True, age__gt=60,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_seal_old.append(seal_old)

                            art = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art.append(art)
                            art_male = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True, gender="male",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art_male.append(art_male)
                            art_female = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True, gender="female",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art_female.append(art_female)
                            art_child = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True, age__lt=13,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art_child.append(art_child)
                            art_teen = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True, age__range=(13, 18),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art_teen.append(art_teen)
                            art_adult = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True, age__range=(19, 60),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art_adult.append(art_adult)
                            art_old = Visualization.objects.filter(active=True,
                                geography_id=i.id, art=True, age__gt=60,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_art_old.append(art_old)

                            exo = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo.append(exo)
                            exo_male = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True, gender="male",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo_male.append(exo_male)
                            exo_female = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True, gender="female",
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo_female.append(exo_female)
                            exo_child = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True, age__lt=13,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo_child.append(exo_child)
                            exo_teen = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True, age__range=(13, 18),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo_teen.append(exo_teen)
                            exo_adult = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True, age__range=(19, 60),
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo_adult.append(exo_adult)
                            exo_old = Visualization.objects.filter(active=True,
                                geography_id=i.id, exo=True, age__gt=60,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_exo_old.append(exo_old)

                            fv = Visualization.objects.filter(active=True,
                                fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv.append(fv)
                            fv_male = Visualization.objects.filter(active=True,
                                gender="male", fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv_male.append(fv_male)
                            fv_female = Visualization.objects.filter(active=True,
                                gender="female", fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv_female.append(fv_female)
                            fv_child = Visualization.objects.filter(active=True,
                                age__lt=13, fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv_child.append(fv_child)
                            fv_teen = Visualization.objects.filter(active=True,
                                age__range=(13, 18), fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv_teen.append(fv_teen)
                            fv_adult = Visualization.objects.filter(active=True,
                                age__range=(19, 60), fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv_adult.append(fv_adult)
                            fv_old = Visualization.objects.filter(active=True,
                                age__gt=60, fv=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fv_old.append(fv_old)

                            fm_sdf = Visualization.objects.filter(active=True,
                                sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf.append(fm_sdf)
                            fm_sdf_male = Visualization.objects.filter(active=True,
                                gender="male", sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf_male.append(fm_sdf_male)
                            fm_sdf_female = Visualization.objects.filter(active=True,
                                gender="female", sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf_female.append(fm_sdf_female)
                            fm_sdf_child = Visualization.objects.filter(active=True,
                                age__lt=13, sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf_child.append(fm_sdf_child)
                            fm_sdf_teen = Visualization.objects.filter(active=True,
                                age__range=(13, 18), sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf_teen.append(fm_sdf_teen)
                            fm_sdf_adult = Visualization.objects.filter(active=True,
                                age__range=(19, 60), sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf_adult.append(fm_sdf_adult)
                            fm_sdf_old = Visualization.objects.filter(active=True,
                                age__gt=60, sdf_whole_mouth=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_fm_sdf_old.append(fm_sdf_old)

                            ref_hp = Visualization.objects.filter(active=True,
                                refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp.append(ref_hp)
                            ref_hp_male = Visualization.objects.filter(active=True,
                                gender="male", refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp_male.append(ref_hp_male)
                            ref_hp_female = Visualization.objects.filter(active=True,
                                gender="female", refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp_female.append(ref_hp_female)
                            ref_hp_child = Visualization.objects.filter(active=True,
                                age__lt=13, refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp_child.append(ref_hp_child)
                            ref_hp_teen = Visualization.objects.filter(active=True,
                                age__range=(13, 18), refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp_teen.append(ref_hp_teen)
                            ref_hp_adult = Visualization.objects.filter(active=True,
                                age__range=(19, 60), refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp_adult.append(ref_hp_adult)
                            ref_hp_old = Visualization.objects.filter(active=True,
                                age__gt=60, refer_hp=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_hp_old.append(ref_hp_old)


                            ref_other = Visualization.objects.filter(active=True,
                                refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other.append(ref_other)
                            ref_other_male = Visualization.objects.filter(active=True,
                                gender="male", refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other_male.append(ref_other_male)
                            ref_other_female = Visualization.objects.filter(active=True,
                                gender="female", refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other_female.append(ref_other_female)
                            ref_other_child = Visualization.objects.filter(active=True,
                                age__lt=13, refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other_child.append(ref_other_child)
                            ref_other_teen = Visualization.objects.filter(active=True,
                                age__range=(13, 18), refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other_teen.append(ref_other_teen)
                            ref_other_adult = Visualization.objects.filter(active=True,
                                age__range=(19, 60), refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other_adult.append(ref_other_adult)
                            ref_other_old = Visualization.objects.filter(active=True,
                                age__gt=60, refer_other=True, geography_id=i.id,
                                activities_id=activities.id,
                                created_at__range=[start_date, end_date]
                            ).count()
                            total_ref_other_old.append(ref_other_old)

                        return Response(
                [
                    {   
                        "isActive": "true",
                        "type":"Total",
                        "Check":sum(total_encounter),
                        "EXO":sum(total_exo),
                        "ART":sum(total_art),
                        "SEAL":sum(total_seal),
                        "SDF":sum(total_sdf),
                        "FM-SDF":sum(total_fm_sdf),
                        "FV":sum(total_fv),
                        "Ref_HP":sum(total_ref_hp),
                        "Ref_Other":sum(total_ref_other)
                    },
                    
                    {   
                        "isActive": "true",
                        "type":"Child ≤ 12Y",
                        "Check":sum(total_children),
                        "EXO":sum(total_exo_child),
                        "ART":sum(total_art_child),
                        "SEAL":sum(total_seal_child),
                        "SDF":sum(total_sdf_child),
                        "FM-SDF":sum(total_fm_sdf_child),
                        "FV":sum(total_fv_child),
                        "Ref_HP":sum(total_ref_hp_child),
                        "Ref_Other":sum(total_ref_other_child),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        },
                    },

                    {   
                        "isActive": "true",
                        "type":"Teen 13-18 Y",
                        "Check":sum(total_teen),
                        "EXO":sum(total_exo_teen),
                        "ART":sum(total_art_teen),
                        "SEAL":sum(total_seal_teen),
                        "SDF":sum(total_sdf_teen),
                        "FM-SDF":sum(total_fm_sdf_teen),
                        "FV":sum(total_fv_teen),
                        "Ref_HP":sum(total_ref_hp_teen),
                        "Ref_Other":sum(total_ref_other_teen),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        }
                        
                    },
                    
                    {   
                        "isActive": "true",
                        "type":"Adult 19 - 60 Y",
                        "Check":sum(total_adult),
                        "EXO":sum(total_exo_adult),
                        "ART":sum(total_art_adult),
                        "SEAL":sum(total_seal_adult),
                        "SDF":sum(total_sdf_adult),
                        "FM-SDF":sum(total_fm_sdf_adult),
                        "FV":sum(total_fv_adult),
                        "Ref_HP":sum(total_ref_hp_adult),
                        "Ref_Other":sum(total_ref_other_adult),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        }
                        
                    },
                    {   
                        "isActive": "true",
                        "type":"Older Adult ≥ 61 Y",
                        "Check":sum(total_older_adult),
                        "EXO":sum(total_exo_old),
                        "ART":sum(total_art_old),
                        "SEAL":sum(total_seal_old),
                        "SDF":sum(total_sdf_old),
                        "FM-SDF":sum(total_fm_sdf_old),
                        "FV":sum(total_fv_old),
                        "Ref_HP":sum(total_ref_hp_old),
                        "Ref_Other":sum(total_ref_other_old),
                        "_cellVariants": {
                            "Check": "success",
                            "EXO": "success",
                            "ART": "success",
                            "SEAL": "success",
                            "SDF": "success",
                            "FM-SDF": "success",
                            "FV": "success",
                            "Ref_HP": "success",
                            "Ref_Other": "success",
                        }
                    },

                    {
                        "isActive": "true",
                        "type":"Male",
                        "Check":sum(total_male),
                        "EXO":sum(total_exo_male),
                        "ART":sum(total_art_male),
                        "SEAL":sum(total_seal_male),
                        "SDF":sum(total_sdf_male),
                        "FM-SDF":sum(total_fm_sdf_male),
                        "FV":sum(total_fv_male),
                        "Ref_HP":sum(total_ref_hp_male),
                        "Ref_Other":sum(total_ref_other_male),
                        "_cellVariants": {
                                "Check": "info",
                                "EXO": "info",
                                "ART": "info",
                                "SEAL": "info",
                                "SDF": "info",
                                "FM-SDF": "info",
                                "FV": "info",
                                "Ref_HP": "info",
                                "Ref_Other": "info",
                            }
                    },
                    {   
                        "isActive": "true",
                        "type":"Female",
                        "Check":sum(total_female),
                        "EXO":sum(total_exo_female),
                        "ART":sum(total_art_female),
                        "SEAL":sum(total_seal_female),
                        "SDF":sum(total_sdf_female),
                        "FM-SDF":sum(total_fm_sdf_female),
                        "FV":sum(total_fv_female),
                        "Ref_HP":sum(total_ref_hp_female),
                        "Ref_Other":sum(total_ref_other_female),
                        "_cellVariants": {
                                "Check": "info",
                                "EXO": "info",
                                "ART": "info",
                                "SEAL": "info",
                                "SDF": "info",
                                "FM-SDF": "info",
                                "FV": "info",
                                "Ref_HP": "info",
                                "Ref_Other": "info",
                        }
                    }
                ]
            )
            return Response(
                {"message": "End date must be greater then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)



# Overview
# class WardTableVisualization2(APIView):
#     serializer_class = WardFilterVisualization
#     permission_classes = (IsPostOrIsAuthenticated,)

#     def get(self, request, format=None):
#         if (
#             CustomUser.objects.select_related("role")
#             .filter(id=request.user.id, role__name="warduser")
#             .exists()
#         ):
#             customuser_obj = CustomUser.objects.get(id=request.user.id)
#             for i in customuser_obj.location.all():
#                 total_sdf = Visualization.objects.filter(
#                     geography_id=i.id, sdf=True
#                 ).count()
#                 total_sdf_male = Visualization.objects.filter(
#                     geography_id=i.id, sdf=True, gender="male"
#                 ).count()
#                 total_sdf_female = Visualization.objects.filter(
#                     geography_id=i.id, sdf=True, gender="female"
#                 ).count()
#                 total_sdf_child = Visualization.objects.filter(
#                     geography_id=i.id, sdf=True, age__lt=18
#                 ).count()
#                 total_sdf_adult = Visualization.objects.filter(
#                     geography_id=i.id, sdf=True, age__range=(18, 60)
#                 ).count()
#                 total_sdf_old = Visualization.objects.filter(
#                     geography_id=i.id, sdf=True, age__gt=60
#                 ).count()

#                 total_seal = Visualization.objects.filter(
#                     geography_id=i.id, seal=True
#                 ).count()
#                 total_seal_male = Visualization.objects.filter(
#                     geography_id=i.id, seal=True, gender="male"
#                 ).count()
#                 total_seal_female = Visualization.objects.filter(
#                     geography_id=i.id, seal=True, gender="female"
#                 ).count()
#                 total_seal_child = Visualization.objects.filter(
#                     geography_id=i.id, seal=True, age__lt=18
#                 ).count()
#                 total_seal_adult = Visualization.objects.filter(
#                     geography_id=i.id, seal=True, age__range=(18, 60)
#                 ).count()
#                 total_seal_old = Visualization.objects.filter(
#                     geography_id=i.id, seal=True, age__gt=60
#                 ).count()

#                 total_art = Visualization.objects.filter(
#                     geography_id=i.id, art=True
#                 ).count()
#                 total_art_male = Visualization.objects.filter(
#                     geography_id=i.id, art=True, gender="male"
#                 ).count()
#                 total_art_female = Visualization.objects.filter(
#                     geography_id=i.id, art=True, gender="female"
#                 ).count()
#                 total_art_child = Visualization.objects.filter(
#                     geography_id=i.id, art=True, age__lt=18
#                 ).count()
#                 total_art_adult = Visualization.objects.filter(
#                     geography_id=i.id, art=True, age__range=(18, 60)
#                 ).count()
#                 total_art_old = Visualization.objects.filter(
#                     geography_id=i.id, art=True, age__gt=60
#                 ).count()

#                 total_exo = Visualization.objects.filter(
#                     geography_id=i.id, exo=True
#                 ).count()
#                 total_exo_male = Visualization.objects.filter(
#                     geography_id=i.id, exo=True, gender="male"
#                 ).count()
#                 total_exo_female = Visualization.objects.filter(
#                     geography_id=i.id, exo=True, gender="female"
#                 ).count()
#                 total_exo_child = Visualization.objects.filter(
#                     geography_id=i.id, exo=True, age__lt=18
#                 ).count()
#                 total_exo_adult = Visualization.objects.filter(
#                     geography_id=i.id, exo=True, age__range=(18, 60)
#                 ).count()
#                 total_exo_old = Visualization.objects.filter(
#                     geography_id=i.id, exo=True, age__gt=60
#                 ).count()

#                 total_fv = Visualization.objects.filter(
#                     fv=True, geography_id=i.id
#                 ).count()
#                 totalfv_male = Visualization.objects.filter(
#                     gender="male", fv=True, geography_id=i.id
#                 ).count()
#                 totalfv_female = Visualization.objects.filter(
#                     gender="female", fv=True, geography_id=i.id
#                 ).count()
#                 totalfv_child = Visualization.objects.filter(
#                     age__lt=18, fv=True, geography_id=i.id
#                 ).count()
#                 totalfv_adult = Visualization.objects.filter(
#                     age__range=(18, 60), fv=True, geography_id=i.id
#                 ).count()
#                 totalfv_old = Visualization.objects.filter(
#                     age__gt=60, fv=True, geography_id=i.id
#                 ).count()

#                 total_fm_sdf = Visualization.objects.filter(
#                     sdf_whole_mouth=True, geography_id=i.id
#                 ).count()
#                 total_fm_sdf_male = Visualization.objects.filter(
#                     gender="male", sdf_whole_mouth=True, geography_id=i.id
#                 ).count()
#                 total_fm_sdf_female = Visualization.objects.filter(
#                     gender="female", sdf_whole_mouth=True, geography_id=i.id
#                 ).count()
#                 total_fm_sdf_child = Visualization.objects.filter(
#                     age__lt=18, sdf_whole_mouth=True, geography_id=i.id
#                 ).count()
#                 total_fm_sdf_adult = Visualization.objects.filter(
#                     age__range=(18, 60), sdf_whole_mouth=True, geography_id=i.id
#                 ).count()
#                 total_fm_sdf_old = Visualization.objects.filter(
#                     age__gt=60, sdf_whole_mouth=True, geography_id=i.id
#                 ).count()

#                 total_ref_hp = Visualization.objects.filter(
#                     refer_hp=True, geography_id=i.id
#                 ).count()
#                 total_ref_hp_male = Visualization.objects.filter(
#                     gender="male", refer_hp=True, geography_id=i.id
#                 ).count()
#                 total_ref_hp_female = Visualization.objects.filter(
#                     gender="female", refer_hp=True, geography_id=i.id
#                 ).count()
#                 total_ref_hp_child = Visualization.objects.filter(
#                     age__lt=18, refer_hp=True, geography_id=i.id
#                 ).count()
#                 total_ref_hp_adult = Visualization.objects.filter(
#                     age__range=(18, 60), refer_hp=True, geography_id=i.id
#                 ).count()
#                 total_ref_hp_old = Visualization.objects.filter(
#                     age__gt=60, refer_hp=True, geography_id=i.id
#                 ).count()


#                 total_ref_other = Visualization.objects.filter(
#                     refer_other=True, geography_id=i.id
#                 ).count()
#                 total_ref_other_male = Visualization.objects.filter(
#                     gender="male", refer_other=True, geography_id=i.id
#                 ).count()
#                 total_ref_other_female = Visualization.objects.filter(
#                     gender="female", refer_other=True, geography_id=i.id
#                 ).count()
#                 total_ref_other_child = Visualization.objects.filter(
#                     age__lt=18, refer_other=True, geography_id=i.id
#                 ).count()
#                 total_ref_other_adult = Visualization.objects.filter(
#                     age__range=(18, 60), refer_other=True, geography_id=i.id
#                 ).count()
#                 total_ref_other_old = Visualization.objects.filter(
#                     age__gt=60, refer_other=True, geography_id=i.id
#                 ).count()

#             return Response(
#                 [
#                     [
#                         "EXO",
#                         total_exo_male,
#                         total_exo_female,
#                         total_exo_child,
#                         total_exo_adult,
#                         total_exo_old,
#                         total_exo,
#                     ],
#                     [
#                         "ART",
#                         total_art_male,
#                         total_art_female,
#                         total_art_child,
#                         total_art_adult,
#                         total_art_old,
#                         total_art,
#                     ],
#                     [
#                         "SEAL",
#                         total_seal_male,
#                         total_seal_female,
#                         total_seal_child,
#                         total_seal_adult,
#                         total_seal_old,
#                         total_seal,
#                     ],
#                     [
#                         "SDF",
#                         total_sdf_male,
#                         total_sdf_female,
#                         total_sdf_child,
#                         total_sdf_adult,
#                         total_sdf_old,
#                         total_sdf,
#                     ],
#                     [
#                         "FV",
#                         totalfv_male,
#                         totalfv_female,
#                         totalfv_child,
#                         totalfv_adult,
#                         totalfv_old,
#                         total_fv,
#                     ],
#                     [
#                         "SDF Whole Mouth",
#                         total_fm_sdf_male,
#                         total_fm_sdf_female,
#                         total_fm_sdf_child,
#                         total_fm_sdf_adult,
#                         total_fm_sdf_old,
#                         total_fm_sdf
#                     ],
#                     [
#                         "Ref HP",
#                         total_ref_hp_male,
#                         total_ref_hp_female,
#                         total_ref_hp_child,
#                         total_ref_hp_adult,
#                         total_ref_hp_old,
#                         total_ref_hp
#                     ],
#                     [
#                         "Ref Other",
#                         total_ref_other_male,
#                         total_ref_other_female,
#                         total_ref_other_child,
#                         total_ref_other_adult,
#                         total_ref_other_old,
#                         total_ref_other
#                     ],
#                 ]
#             )
#         return Response({"treatment_obj": "do not have a permission"}, status=400)

#     def post(self, request, format=None):
#         serializer = WardFilterVisualization(
#             data=request.data, context={"request": request}
#         )
#         if serializer.is_valid():
#             start_date = str(
#                 NepaliDate.from_date(serializer.validated_data["start_date"])
#             )
#             end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
#             activities_list = serializer.validated_data["activities"]
#             if end_date > start_date:
#                 if CustomUser.objects.select_related("role").filter(
#                     id=request.user.id, role__name="warduser"
#                 ):
#                     customuser_obj = CustomUser.objects.get(id=request.user.id)
#                     total_sdf = []
#                     total_sdf_male = []
#                     total_sdf_female = []
#                     total_sdf_child = []
#                     total_sdf_adult = []
#                     total_sdf_old = []

#                     total_seal = []
#                     total_seal_male = []
#                     total_seal_female = []
#                     total_seal_child = []
#                     total_seal_adult = []
#                     total_seal_old = []

#                     total_art = []
#                     total_art_male = []
#                     total_art_female = []
#                     total_art_child = []
#                     total_art_adult = []
#                     total_art_old = []

#                     total_exo = []
#                     total_exo_male = []
#                     total_exo_female = []
#                     total_exo_child = []
#                     total_exo_adult = []
#                     total_exo_old = []

#                     total_fv = []
#                     totalfv_male = []
#                     totalfv_female = []
#                     totalfv_child = []
#                     totalfv_adult = []
#                     totalfv_old = []

#                     for i in customuser_obj.location.all():
#                         for activities in activities_list:
#                             total_sdf.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     sdf=True,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_sdf_male.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     sdf=True,
#                                     gender="male",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_sdf_female.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     sdf=True,
#                                     gender="female",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_sdf_child.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     sdf=True,
#                                     age__lt=18,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_sdf_adult.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     sdf=True,
#                                     age__range=(18, 60),
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_sdf_old.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     sdf=True,
#                                     age__gt=60,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )

#                             total_seal.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id, seal=True
#                                 ).count()
#                             )
#                             total_seal_male.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     seal=True,
#                                     gender="male",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_seal_female.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     seal=True,
#                                     gender="female",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_seal_child.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     seal=True,
#                                     age__lt=18,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_seal_adult.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     seal=True,
#                                     age__range=(18, 60),
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_seal_old.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     seal=True,
#                                     age__gt=60,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )

#                             total_art.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     art=True,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_art_male.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     art=True,
#                                     gender="male",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_art_female.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     art=True,
#                                     gender="female",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_art_child.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     art=True,
#                                     age__lt=18,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_art_adult.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     art=True,
#                                     age__range=(18, 60),
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_art_old.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     art=True,
#                                     age__gt=60,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )

#                             total_exo.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     exo=True,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_exo_male.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     exo=True,
#                                     gender="male",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_exo_female.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     exo=True,
#                                     gender="female",
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_exo_child.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     exo=True,
#                                     age__lt=18,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_exo_adult.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     exo=True,
#                                     age__range=(18, 60),
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             total_exo_old.append(
#                                 Visualization.objects.filter(
#                                     geography_id=i.id,
#                                     exo=True,
#                                     age__gt=60,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )

#                             total_fv.append(
#                                 Visualization.objects.filter(
#                                     fv=True,
#                                     geography_id=i.id,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             totalfv_male.append(
#                                 Visualization.objects.filter(
#                                     gender="male",
#                                     fv=True,
#                                     geography_id=i.id,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             totalfv_female.append(
#                                 Visualization.objects.filter(
#                                     gender="female",
#                                     fv=True,
#                                     geography_id=i.id,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             totalfv_child.append(
#                                 Visualization.objects.filter(
#                                     age__lt=18,
#                                     fv=True,
#                                     geography_id=i.id,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             totalfv_adult.append(
#                                 Visualization.objects.filter(
#                                     age__range=(18, 60),
#                                     fv=True,
#                                     geography_id=i.id,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )
#                             totalfv_old.append(
#                                 Visualization.objects.filter(
#                                     age__gt=60,
#                                     fv=True,
#                                     geography_id=i.id,
#                                     activities_id=activities.id,
#                                     created_at__range=[start_date, end_date],
#                                 ).count()
#                             )

#                     return Response(
#                         [
#                             [
#                                 "EXO",
#                                 sum(total_exo_male),
#                                 sum(total_exo_female),
#                                 sum(total_exo_child),
#                                 sum(total_exo_adult),
#                                 sum(total_exo_old),
#                                 sum(total_exo),
#                             ],
#                             [
#                                 "ART",
#                                 sum(total_art_male),
#                                 sum(total_art_female),
#                                 sum(total_art_child),
#                                 sum(total_art_adult),
#                                 sum(total_art_old),
#                                 sum(total_art),
#                             ],
#                             [
#                                 "SEAL",
#                                 sum(total_seal_male),
#                                 sum(total_seal_female),
#                                 sum(total_seal_child),
#                                 sum(total_seal_adult),
#                                 sum(total_seal_old),
#                                 sum(total_seal),
#                             ],
#                             [
#                                 "SDF",
#                                 sum(total_sdf_male),
#                                 sum(total_sdf_female),
#                                 sum(total_sdf_child),
#                                 sum(total_sdf_adult),
#                                 sum(total_sdf_old),
#                                 sum(total_sdf),
#                             ],
#                             [
#                                 "FV",
#                                 sum(totalfv_male),
#                                 sum(totalfv_female),
#                                 sum(totalfv_child),
#                                 sum(totalfv_adult),
#                                 sum(totalfv_old),
#                                 sum(total_fv),
#                             ],
#                         ]
#                     )
#             return Response(
#                 {"message": "End date must be greater then Start Date"}, status=400
#             )
#         return Response({"message": serializer.errors}, status=400)



# 10.4 Contacts by Setting
class WardSettingVisualization(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if (
            CustomUser.objects.select_related("role")
            .filter(id=request.user.id, role__name="warduser")
            .exists()
        ):
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            activities_data = []
            activities_name = []
            for activities in Activity.objects.all():
                activities_name.append(activities.name)
                count_list = []
                for i in customuser_obj.location.all():
                    count_list.append(
                        Visualization.objects.filter(active=True,
                            activities_id=activities.id, geography_id=i.id
                        ).count()
                    )
                activities_data.append(count_list)
                locationChart = {
                    "data": {
                        "labels": activities_name,
                        "datasets": [
                            {
                                "label": "All",
                                "backgroundColor": [
                                    "rgba(84, 184, 209, 0.5)",
                                    "rgba(91, 95, 151, 0.5)",
                                    "rgba(255, 193, 69, 0.5)",
                                    "rgba(96, 153, 45, 0.5)",
                                ],
                                "borderColor": [
                                    "rgba(84, 184, 209, 1)",
                                    "rgba(91, 95, 151, 1)",
                                    "rgba(255, 193, 69, 1)",
                                    "rgba(96, 153, 45, 1)",
                                ],
                                "borderWidth": 1,
                                "data": activities_data,
                            }
                        ],
                    },
                    "options": {
                        "responsive": "true",
                        "maintainAspectRatio": "false",
                        "aspectRatio": 1.5,
                        "title": {
                            "display": "true",
                            # 'text': "Activity Distribution Chart",
                            "fontSize": 18,
                            "fontFamily": "'Palanquin', sans-serif",
                        },
                        "legend": {
                            "display": "true",
                            "position": "bottom",
                            "labels": {
                                "usePointStyle": "true",
                                "padding": 20,
                                "fontFamily": "'Maven Pro', sans-serif",
                            },
                        },
                    },
                }
            return Response({"locationChart": locationChart})
        return Response({"message": "only ward user can see"}, status=400)
    
    def post(self, request, format=None):
        serializer = WardFilterVisualization(data=request.data, context={"request": request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data["start_date"]))
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))

            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    activities_data = []
                    activities_name = []
                    for activities in activities_list:
                        activities_name.append(activities.name)
                        count_list = []
                        for i in customuser_obj.location.all():
                            count_list.append(
                                Visualization.objects.filter(active=True,
                                    activities_id=activities.id,
                                    geography_id=i.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                        activities_data.append(count_list)
                        locationChart = {
                            "data": {
                                "labels": activities_name,
                                "datasets": [
                                    {
                                        "label": "All",
                                        "backgroundColor": [
                                            "rgba(84, 184, 209, 0.5)",
                                            "rgba(91, 95, 151, 0.5)",
                                            "rgba(255, 193, 69, 0.5)",
                                            "rgba(96, 153, 45, 0.5)",
                                        ],
                                        "borderColor": [
                                            "rgba(84, 184, 209, 1)",
                                            "rgba(91, 95, 151, 1)",
                                            "rgba(255, 193, 69, 1)",
                                            "rgba(96, 153, 45, 1)",
                                        ],
                                        "borderWidth": 1,
                                        "data": activities_data,
                                    }
                                ],
                            },
                            "options": {
                                "responsive": "true",
                                "maintainAspectRatio": "false",
                                "aspectRatio": 1.5,
                                "title": {
                                    "display": "true",
                                    # 'text': "Activity Distribution Chart",
                                    "fontSize": 18,
                                    "fontFamily": "'Palanquin', sans-serif",
                                },
                                "legend": {
                                    "display": "true",
                                    "position": "bottom",
                                    "labels": {
                                        "usePointStyle": "true",
                                        "padding": 20,
                                        "fontFamily": "'Maven Pro', sans-serif",
                                    },
                                },
                            },
                        }
                    return Response({"locationChart": locationChart})
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)


# we dont need this api post done in above api
class WardSettingVisualizationFilter(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def post(self, request, format=None):
        serializer = WardFilterVisualization(data=request.data, context={"request": request})
        if serializer.is_valid():
            start_date = str(NepaliDate.from_date(serializer.validated_data["start_date"]))
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))

            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    activities_data = []
                    activities_name = []
                    for activities in activities_list:
                        activities_name.append(activities.name)
                        count_list = []
                        for i in customuser_obj.location.all():
                            count_list.append(
                                Visualization.objects.filter(active=True,
                                    activities_id=activities.id,
                                    geography_id=i.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                        activities_data.append(count_list)
                        locationChart = {
                            "data": {
                                "labels": activities_name,
                                "datasets": [
                                    {
                                        "label": "All",
                                        "backgroundColor": [
                                            "rgba(84, 184, 209, 0.5)",
                                            "rgba(91, 95, 151, 0.5)",
                                            "rgba(255, 193, 69, 0.5)",
                                            "rgba(96, 153, 45, 0.5)",
                                        ],
                                        "borderColor": [
                                            "rgba(84, 184, 209, 1)",
                                            "rgba(91, 95, 151, 1)",
                                            "rgba(255, 193, 69, 1)",
                                            "rgba(96, 153, 45, 1)",
                                        ],
                                        "borderWidth": 1,
                                        "data": activities_data,
                                    }
                                ],
                            },
                            "options": {
                                "responsive": "true",
                                "maintainAspectRatio": "false",
                                "aspectRatio": 1.5,
                                "title": {
                                    "display": "true",
                                    # 'text': "Activity Distribution Chart",
                                    "fontSize": 18,
                                    "fontFamily": "'Palanquin', sans-serif",
                                },
                                "legend": {
                                    "display": "true",
                                    "position": "bottom",
                                    "labels": {
                                        "usePointStyle": "true",
                                        "padding": 20,
                                        "fontFamily": "'Maven Pro', sans-serif",
                                    },
                                },
                            },
                        }
                    return Response({"locationChart": locationChart})
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)


# 10.3 Treatments by Age & Gender
class WardTreatmentVisualization(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if (
            CustomUser.objects.select_related("role")
            .filter(id=request.user.id, role__name="warduser")
            .exists()
        ):
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            district = ["FV", "SDF", "SEAL", "ART", "EXO"]
            total = []
            male = []
            female = []
            for i in customuser_obj.location.all():
                total_sdf = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True
                ).count()
                total_sdf_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, gender="male"
                ).count()
                total_sdf_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, sdf=True, gender="female"
                ).count()

                total_seal = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True
                ).count()
                total_seal_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, gender="male"
                ).count()
                total_seal_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, seal=True, gender="female"
                ).count()

                total_art = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True
                ).count()
                total_art_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, gender="male"
                ).count()
                total_art_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, art=True, gender="female"
                ).count()

                total_exo = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True
                ).count()
                total_exo_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, gender="male"
                ).count()
                total_exo_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, exo=True, gender="female"
                ).count()

                total_fv = Visualization.objects.filter(active=True,
                    geography_id=i.id, fv=True
                ).count()
                totalfv_male = Visualization.objects.filter(active=True,
                    geography_id=i.id, fv=True, gender="male"
                ).count()
                totalfv_female = Visualization.objects.filter(active=True,
                    geography_id=i.id, fv=True, gender="female"
                ).count()


                male.append(totalfv_male)
                male.append(total_sdf_male)
                male.append(total_seal_male)
                male.append(total_art_male)
                male.append(total_exo_male)
                
                female.append(totalfv_female)
                female.append(total_sdf_female)
                female.append(total_seal_female)
                female.append(total_art_female)
                female.append(total_exo_female)

                total.append(total_fv)
                total.append(total_sdf)
                total.append(total_seal)
                total.append(total_art)
                total.append(total_exo)

            locationChart = {
                "data": {
                    "labels": district,
                    "datasets": [
                        {
                            "label": "Total",
                            "backgroundColor": "rgba(255, 206, 86, 0.2)",
                            "borderColor": "rgba(255, 206, 86, 1)",
                            "borderWidth": 1,
                            "data": total,
                        },
                        {
                            "label": "Female",
                            "backgroundColor": "rgba(239, 62, 54, 0.2)",
                            "borderColor": "rgba(239, 62, 54, 1)",
                            "borderWidth": 1,
                            "data": female,
                        },
                        {
                            "label": "Male",
                            "backgroundColor": "rgba(64, 224, 208, 0.2)",
                            "borderColor": "rgba(64, 224, 208, 1)",
                            "borderWidth": 1,
                            "data": male,
                        },
                    ],
                },
                "options": {
                    "aspectRatio": 1.5,
                    "scales": {"yAxes": [{"ticks": {"beginAtZero": "true"}}]},
                    "title": {
                        "display": "true",
                        # 'text': "Treatment-wise Gender Distribution",
                        "fontSize": 18,
                        "fontFamily": "'Palanquin', sans-serif",
                    },
                    "legend": {
                        "display": "true",
                        "position": "bottom",
                        "labels": {
                            "usePointStyle": "true",
                            "padding": 20,
                            "fontFamily": "'Maven Pro', sans-serif",
                        },
                    },
                },
            }
            return Response({"locationChart": locationChart})
        return Response({"message": "only admin can create"}, status=400)
    
    def post(self, request, format=None):
        serializer = WardFilterVisualization(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    district = ["EXO", "ART", "SEAL", "SDF", "FV"]
                    total = []
                    male = []
                    female = []
                    for activities in activities_list:
                        total_sdf = []
                        total_sdf_male = []
                        total_sdf_female = []

                        total_seal = []
                        total_seal_male = []
                        total_seal_female = []

                        total_art = []
                        total_art_male = []
                        total_art_female = []

                        total_exo = []
                        total_exo_male = []
                        total_exo_female = []

                        total_fv = []
                        totalfv_male = []
                        totalfv_female = []

                        for i in customuser_obj.location.all():
                            total_sdf.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    sdf=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    sdf=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    sdf=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_seal.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    seal=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    seal=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    seal=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_art.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    art=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    art=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    art=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_exo.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    exo=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    exo=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    exo=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_fv.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    fv=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    fv=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    fv=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                        male.append(sum(totalfv_male))
                        male.append(sum(total_sdf_male))
                        male.append(sum(total_seal_male))
                        male.append(sum(total_art_male))
                        male.append(sum(total_exo_male))
                        
                        female.append(sum(totalfv_female))
                        female.append(sum(total_sdf_female))
                        female.append(sum(total_seal_female))
                        female.append(sum(total_art_female))
                        female.append(sum(total_exo_female))
                        
                        total.append(sum(total_fv))
                        total.append(sum(total_sdf))
                        total.append(sum(total_seal))
                        total.append(sum(total_art))
                        total.append(sum(total_exo))
                         
                    locationChart = {
                        "data": {
                            "labels": district,
                            "datasets": [
                                {
                                    "label": "Total",
                                    "backgroundColor": "rgba(255, 206, 86, 0.2)",
                                    "borderColor": "rgba(255, 206, 86, 1)",
                                    "borderWidth": 1,
                                    "data": total,
                                },
                                {
                                    "label": "Female",
                                    "backgroundColor": "rgba(239, 62, 54, 0.2)",
                                    "borderColor": "rgba(239, 62, 54, 1)",
                                    "borderWidth": 1,
                                    "data": female,
                                },
                                {
                                    "label": "Male",
                                    "backgroundColor": "rgba(64, 224, 208, 0.2)",
                                    "borderColor": "rgba(64, 224, 208, 1)",
                                    "borderWidth": 1,
                                    "data": male,
                                },
                            ],
                        },
                        "options": {
                            "aspectRatio": 1.5,
                            "scales": {"yAxes": [{"ticks": {"beginAtZero": "true"}}]},
                            "title": {
                                "display": "true",
                                # 'text': "Treatment-wise Gender Distribution",
                                "fontSize": 18,
                                "fontFamily": "'Palanquin', sans-serif",
                            },
                            "legend": {
                                "display": "true",
                                "position": "bottom",
                                "labels": {
                                    "usePointStyle": "true",
                                    "padding": 20,
                                    "fontFamily": "'Maven Pro', sans-serif",
                                },
                            },
                        },
                    }
                    return Response({"locationChart": locationChart})
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)


# dont need this api, post done in above api
class WardTreatmentVisualizationFilter(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def post(self, request, format=None):
        serializer = WardFilterVisualization(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    district = ["EXO", "ART", "SEAL", "SDF", "FV"]
                    total = []
                    male = []
                    female = []
                    for activities in activities_list:
                        total_sdf = []
                        total_sdf_male = []
                        total_sdf_female = []

                        total_seal = []
                        total_seal_male = []
                        total_seal_female = []

                        total_art = []
                        total_art_male = []
                        total_art_female = []

                        total_exo = []
                        total_exo_male = []
                        total_exo_female = []

                        total_fv = []
                        totalfv_male = []
                        totalfv_female = []

                        for i in customuser_obj.location.all():
                            total_sdf.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    sdf=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    sdf=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    sdf=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_seal.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    seal=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    seal=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    seal=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_art.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    art=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    art=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    art=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_exo.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    exo=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    exo=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    exo=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_fv.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    fv=True,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_male.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    fv=True,
                                    gender="male",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_female.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    fv=True,
                                    gender="female",
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                        male.append(sum(total_exo_male))
                        male.append(sum(total_art_male))
                        male.append(sum(total_seal_male))
                        male.append(sum(total_sdf_male))
                        male.append(sum(totalfv_male))
                        female.append(sum(total_exo_female))
                        female.append(sum(total_art_female))
                        female.append(sum(total_seal_female))
                        female.append(sum(total_sdf_female))
                        female.append(sum(totalfv_female))
                        total.append(sum(total_exo))
                        total.append(sum(total_art))
                        total.append(sum(total_seal))
                        total.append(sum(total_sdf))
                        total.append(sum(total_fv))
                    locationChart = {
                        "data": {
                            "labels": district,
                            "datasets": [
                                {
                                    "label": "Total",
                                    "backgroundColor": "rgba(255, 206, 86, 0.2)",
                                    "borderColor": "rgba(255, 206, 86, 1)",
                                    "borderWidth": 1,
                                    "data": total,
                                },
                                {
                                    "label": "Female",
                                    "backgroundColor": "rgba(239, 62, 54, 0.2)",
                                    "borderColor": "rgba(239, 62, 54, 1)",
                                    "borderWidth": 1,
                                    "data": female,
                                },
                                {
                                    "label": "Male",
                                    "backgroundColor": "rgba(64, 224, 208, 0.2)",
                                    "borderColor": "rgba(64, 224, 208, 1)",
                                    "borderWidth": 1,
                                    "data": male,
                                },
                            ],
                        },
                        "options": {
                            "aspectRatio": 1.5,
                            "scales": {"yAxes": [{"ticks": {"beginAtZero": "true"}}]},
                            "title": {
                                "display": "true",
                                # 'text': "Treatment-wise Gender Distribution",
                                "fontSize": 18,
                                "fontFamily": "'Palanquin', sans-serif",
                            },
                            "legend": {
                                "display": "true",
                                "position": "bottom",
                                "labels": {
                                    "usePointStyle": "true",
                                    "padding": 20,
                                    "fontFamily": "'Maven Pro', sans-serif",
                                },
                            },
                        },
                    }
                    return JsonResponse({"locationChart": locationChart})
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)



# 10.5 Contacts Over Time
class WardUserlineVisualization(APIView):
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            # label_data = [
            #     "Baishakh(Apr/May)",
            #     "Jestha(May/Jun)",
            #     "Asar(Jun/Jul)",
            #     "Shrawan(Jul/Aug)",
            #     "Bhadra(Aug/Sep)",
            #     "Asoj(Sep/Oct)",
            #     "Kartik(Oct/Nov)",
            #     "Mangsir(Nov/Dec)",
            #     "Poush(Dec/Jan)",
            #     "Magh(Jan/Feb)",
            #     "Falgun(Feb/Mar)",
            #     "Chaitra(Mar/Apr)",
            # ]

            label_data = [
                "Q2(Apr/May)",
                "",
                "",
                "Q3(Jul/Aug)",
                "",
                "",
                "Q4(Oct/Nov)",
                "",
                "",
                "Q1(Jan/Feb)",
                "",
                "",
            ]

            next_month = month.index(item) + 1
            month_obj = month[next_month:]
            label_data_obj = label_data[next_month:]
            for i in month[next_month:]:
                a = month.index(i)
                month.pop(a)
                label_data.pop(a)
            x=month_obj[::-1]
            for b in x:
                month.insert(0, b)
            y=label_data_obj[::-1]
            for n in y:
                label_data.insert(0, n)

            # month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            geography = []
            geography_patient = []
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                v = []
                for x in month:
                    if Visualization.objects.filter(active=True,geography_id=i.id).exists():
                        total_patient = Visualization.objects.filter(
                            geography_id=i.id, created_at__month=x
                        ).count()
                        v.append(total_patient)
                geography.append(i.name)
                geography_patient.append(v)
            data_data = []
            datasets1 = []
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)"]
            
            m = 0
            n = 0
            for y in geography:
                a = {
                    "label": y,
                    "backgroundColor": "rgba(255, 255, 255, 0)",
                    "borderColor": cz[m],
                    "borderWidth": 1,
                    "data": geography_patient[n],
                }
                datasets1.append(a)
                m += 1
                n += 1
            locationChart = {
                "data": {
                    "labels": label_data,
                    "datasets": datasets1,
                },
                "options": {
                    "aspectRatio": 2.2,
                    "title": {
                        "display": "true",
                        # 'text': "Month-wise contact distribution",
                        "fontSize": 18,
                        "fontFamily": "'Palanquin', sans-serif",
                    },
                    "legend": {"position": "bottom"},
                    "labels": {"usePointStyle": "true"},
                    "scales": {
                        "yAxes": [
                            {
                                "ticks": {
                                    "fontColor": "rgba(0,0,0,0.5)",
                                    "fontStyle": "bold",
                                    "beginAtZero": "false",
                                    "maxTicksLimit": 6,
                                    "padding": 20,
                                },
                                "gridLines": {"drawTicks": "true", "display": "true"},
                            }
                        ],
                        "xAxes": [
                            {
                                "gridLines": {"zeroLineColor": "transparent"},
                                "ticks": {
                                    "padding": 20,
                                    "fontColor": "rgba(0,0,0,0.5)",
                                    "fontStyle": "bold",
                                },
                            }
                        ],
                    },
                },
            }
            return Response({"locationChart": locationChart})
        return Response({"message": "only admin can see"}, status=400)

# 10.7 Strategic Data
class WardStrategicData(APIView):
    serializer_class = WardFilterVisualization
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        if (
            CustomUser.objects.select_related("role")
            .filter(id=request.user.id, role__name="warduser")
            .exists()
        ):
            customuser_obj = CustomUser.objects.get(id=request.user.id)
            for i in customuser_obj.location.all():
                total_encounter = Visualization.objects.filter(active=True,
                    geography_id=i.id
                ).count()
                encounter_male = Visualization.objects.filter(active=True,
                    gender="male", geography_id=i.id
                ).count()
                encounter_female = Visualization.objects.filter(active=True,
                    gender="female", geography_id=i.id
                ).count()
                encounter_child = Visualization.objects.filter(active=True,
                    age__lt=12, geography_id=i.id
                ).count()
                encounter_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), geography_id=i.id
                ).count()
                encounter_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), geography_id=i.id
                ).count()
                encounter_old = Visualization.objects.filter(active=True,
                    age__gt=60, geography_id=i.id
                ).count()

                total_refer = Visualization.objects.filter(active=True,
                    refer_hp=True, geography_id=i.id
                ).count()
                refer_male = Visualization.objects.filter(active=True,
                    gender="male", refer_hp=True, geography_id=i.id
                ).count()
                refer_female = Visualization.objects.filter(active=True,
                    gender="female", refer_hp=True, geography_id=i.id
                ).count()
                refer_child = Visualization.objects.filter(active=True,
                    age__lt=12, refer_hp=True, geography_id=i.id
                ).count()
                refer_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), refer_hp=True, geography_id=i.id
                ).count()
                refer_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), refer_hp=True, geography_id=i.id
                ).count()
                refer_old = Visualization.objects.filter(active=True,
                    age__gt=60, refer_hp=True, geography_id=i.id
                ).count()

                total_refer = Visualization.objects.filter(active=True,
                    refer_hp=True, geography_id=i.id
                ).count()
                total_seal_male = Visualization.objects.filter(active=True,
                    gender="male", seal=True, geography_id=i.id
                ).count()
                total_seal_female = Visualization.objects.filter(active=True,
                    gender="female", seal=True, geography_id=i.id
                ).count()
                total_seal_child = Visualization.objects.filter(active=True,
                    age__lt=12, seal=True, geography_id=i.id
                ).count()
                total_seal_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), seal=True, geography_id=i.id
                ).count()
                total_seal_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), seal=True, geography_id=i.id
                ).count()
                total_seal_old = Visualization.objects.filter(active=True,
                    age__gt=60, seal=True, geography_id=i.id
                ).count()

                totalfv_male = Visualization.objects.filter(active=True,
                    gender="male", fv=True, geography_id=i.id
                ).count()
                totalfv_female = Visualization.objects.filter(active=True,
                    gender="female", fv=True, geography_id=i.id
                ).count()
                totalfv_child = Visualization.objects.filter(active=True,
                    age__lt=12, fv=True, geography_id=i.id
                ).count()
                totalfv_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), fv=True, geography_id=i.id
                ).count()
                totalfv_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), fv=True, geography_id=i.id
                ).count()
                totalfv_old = Visualization.objects.filter(active=True,
                    age__gt=60, fv=True, geography_id=i.id
                ).count()

                total_exo_male = Visualization.objects.filter(active=True,
                    gender="male", exo=True, geography_id=i.id
                ).count()
                total_exo_female = Visualization.objects.filter(active=True,
                    gender="female", exo=True, geography_id=i.id
                ).count()
                total_exo_child = Visualization.objects.filter(active=True,
                    age__lt=12, exo=True, geography_id=i.id
                ).count()
                total_exo_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), exo=True, geography_id=i.id
                ).count()
                total_exo_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), exo=True, geography_id=i.id
                ).count()
                total_exo_old = Visualization.objects.filter(active=True,
                    age__gt=60, exo=True, geography_id=i.id
                ).count()

                total_art_male = Visualization.objects.filter(active=True,
                    gender="male", art=True, geography_id=i.id
                ).count()
                total_art_female = Visualization.objects.filter(active=True,
                    gender="female", art=True, geography_id=i.id
                ).count()
                total_art_child = Visualization.objects.filter(active=True,
                    age__lt=12, art=True, geography_id=i.id
                ).count()
                total_art_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), art=True, geography_id=i.id
                ).count()
                total_art_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), art=True, geography_id=i.id
                ).count()
                total_art_old = Visualization.objects.filter(active=True,
                    age__gt=60, art=True, geography_id=i.id
                ).count()

                total_sdf_male = Visualization.objects.filter(active=True,
                    gender="male", sdf=True, geography_id=i.id
                ).count()
                total_sdf_female = Visualization.objects.filter(active=True,
                    gender="female", sdf=True, geography_id=i.id
                ).count()
                total_sdf_child = Visualization.objects.filter(active=True,
                    age__lt=12, sdf=True, geography_id=i.id
                ).count()
                total_sdf_teen = Visualization.objects.filter(active=True,
                    age__range=(13, 18), sdf=True, geography_id=i.id
                ).count()
    
                total_sdf_adult = Visualization.objects.filter(active=True,
                    age__range=(19, 60), sdf=True, geography_id=i.id
                ).count()
                total_sdf_old = Visualization.objects.filter(active=True,
                    age__gt=60, sdf=True, geography_id=i.id
                ).count()

                try:
                    preventive_ratio_male = (total_seal_male + totalfv_male) / (
                        total_exo_male + total_art_male + total_sdf_male
                    )
                except:
                    preventive_ratio_male = 0
                try:
                    preventive_ratio_female = (total_seal_female + totalfv_female) / (
                        total_exo_female + total_art_female + total_sdf_female
                    )
                except:
                    preventive_ratio_female = 0
                try:
                    preventive_ratio_child = (total_seal_child + totalfv_child) / (
                        total_exo_child + total_art_child + total_sdf_child
                    )
                except:
                    preventive_ratio_child = 0
                try:
                    preventive_ratio_teen = (total_seal_teen + totalfv_teen) / (
                        total_exo_teen + total_art_teen + total_sdf_teen
                    )
                except:
                    preventive_ratio_teen = 0
                try:
                    preventive_ratio_adult = (total_seal_adult + totalfv_adult) / (
                        total_exo_adult + total_art_adult + total_sdf_adult
                    )
                except:
                    preventive_ratio_adult = 0
                try:
                    preventive_ratio_old = (total_seal_old + totalfv_old) / (
                        total_exo_old + total_art_old + total_sdf_old
                    )
                except:
                    preventive_ratio_old = 0

                preventive_ratio_total = preventive_ratio_male + preventive_ratio_female

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

                try:
                    recall_percent_total = (total_refer / total_encounter) * 100
                except:
                    recall_percent_old = 0

                # recall_percent_total = recall_percent_male+recall_percent_female

            return Response(
                [
                    [
                        "Preventive Ratio",
                        round(preventive_ratio_male, 2),
                        round(preventive_ratio_female, 2),
                        round(preventive_ratio_child, 2),
                        round(preventive_ratio_teen, 2),
                        round(preventive_ratio_adult, 2),
                        round(preventive_ratio_old, 2),
                        round(preventive_ratio_total, 2),
                    ],
                    [
                        "Early Intervention Ratio",
                        round(early_intervention_ratio_male, 2),
                        round(early_intervention_ratio_female, 2),
                        round(early_intervention_ratio_child, 2),
                        round(early_intervention_ratio_teen, 2),
                        round(early_intervention_ratio_adult, 2),
                        round(early_intervention_ratio_old, 2),
                        round(early_intervention_ratio_total, 2),
                    ],
                    [
                        "% Recall",
                        str(round(recall_percent_male, 2)) + "%",
                        str(round(recall_percent_female, 2)) + "%",
                        str(round(recall_percent_child, 2)) + "%",
                        str(round(recall_percent_teen, 2)) + "%",
                        str(round(recall_percent_adult, 2)) + "%",
                        str(round(recall_percent_old, 2)) + "%",
                        str(round(recall_percent_total, 2)) + "%",
                    ],
                ]
            )
        return Response({"treatment_obj": "do not have a permission"}, status=400)

    def post(self, request, format=None):
        serializer = WardFilterVisualization(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            start_date = str(
                NepaliDate.from_date(serializer.validated_data["start_date"])
            )
            end_date = str(NepaliDate.from_date(serializer.validated_data["end_date"]))
            activities_list = serializer.validated_data["activities"]
            if end_date > start_date:
                if CustomUser.objects.select_related("role").filter(
                    id=request.user.id, role__name="warduser"
                ):
                    customuser_obj = CustomUser.objects.get(id=request.user.id)
                    total_encounter = []
                    encounter_male = []
                    encounter_female = []
                    encounter_child = []
                    encounter_teen = []
                    encounter_adult = []
                    encounter_old = []

                    total_refer = []
                    refer_male = []
                    refer_female = []
                    refer_child = []
                    refer_teen = []
                    refer_adult = []
                    refer_old = []

                    total_seal = []
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

                    for i in customuser_obj.location.all():
                        for activities in activities_list:
                            total_encounter.append(
                                Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            encounter_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            encounter_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            encounter_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            encounter_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            encounter_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            encounter_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_refer.append(
                                Visualization.objects.filter(active=True,
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            refer_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            refer_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            refer_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            refer_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            refer_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            refer_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    refer_hp=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_seal.append(
                                Visualization.objects.filter(active=True,
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_seal_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    seal=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            totalfv_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            totalfv_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    fv=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_exo_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    exo=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    exo=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    exo=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    exo=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    exo=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_exo_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    exo=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_art_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    art=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    art=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    art=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    art=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(18, 60),
                                    art=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_art_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    art=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                            total_sdf_male.append(
                                Visualization.objects.filter(active=True,
                                    gender="male",
                                    sdf=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_female.append(
                                Visualization.objects.filter(active=True,
                                    gender="female",
                                    sdf=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_child.append(
                                Visualization.objects.filter(active=True,
                                    age__lt=12,
                                    sdf=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_teen.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(13, 18),
                                    sdf=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_adult.append(
                                Visualization.objects.filter(active=True,
                                    age__range=(19, 60),
                                    sdf=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )
                            total_sdf_old.append(
                                Visualization.objects.filter(active=True,
                                    age__gt=60,
                                    sdf=True,
                                    geography_id=i.id,
                                    activities_id=activities.id,
                                    created_at__range=[start_date, end_date],
                                ).count()
                            )

                    try:
                        preventive_ratio_male = (
                            sum(total_seal_male) + sum(totalfv_male)
                        ) / (
                            sum(total_exo_male)
                            + sum(total_art_male)
                            + sum(total_sdf_male)
                        )
                    except:
                        preventive_ratio_male = 0
                    try:
                        preventive_ratio_female = (
                            sum(total_seal_female) + sum(totalfv_female)
                        ) / (
                            sum(total_exo_female)
                            + sum(total_art_female)
                            + sum(total_sdf_female)
                        )
                    except:
                        preventive_ratio_female = 0
                    try:
                        preventive_ratio_child = (
                            sum(total_seal_child) + sum(totalfv_child)
                        ) / (
                            sum(total_exo_child)
                            + sum(total_art_child)
                            + sum(total_sdf_child)
                        )
                    except:
                        preventive_ratio_child = 0
                    try:
                        preventive_ratio_adult = (
                            sum(total_seal_adult) + sum(totalfv_adult)
                        ) / (
                            sum(total_exo_adult)
                            + sum(total_art_adult)
                            + sum(total_sdf_adult)
                        )
                    except:
                        preventive_ratio_adult = 0
                    
                    try:
                        preventive_ratio_teen = (
                            sum(total_seal_teen) + sum(totalfv_teen)
                        ) / (
                            sum(total_exo_teen)
                            + sum(total_art_teen)
                            + sum(total_sdf_teen)
                        )
                    except:
                        preventive_ratio_teen = 0
                    try:
                        preventive_ratio_old = (
                            sum(total_seal_old) + sum(totalfv_old)
                        ) / (
                            sum(total_exo_old) + sum(total_art_old) + sum(total_sdf_old)
                        )
                    except:
                        preventive_ratio_old = 0

                    preventive_ratio_total = (
                        preventive_ratio_male + preventive_ratio_female
                    )

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
                            sum(total_art_old) + sum(total_sdf_old)
                        ) / sum(total_exo_old)
                    except:
                        early_intervention_ratio_old = 0

                    early_intervention_ratio_total = (
                        early_intervention_ratio_male + early_intervention_ratio_female
                    )

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

                    try:
                        recall_percent_total = (
                            sum(total_refer) / sum(total_encounter)
                        ) * 100
                    except:
                        recall_percent_total = 0

                    # recall_percent_total = recall_percent_male+recall_percent_female
                    return Response(
                        [
                            [
                                "Preventive Ratio",
                                round(preventive_ratio_male, 2),
                                round(preventive_ratio_female, 2),
                                round(preventive_ratio_child, 2),
                                round(preventive_ratio_teen, 2),
                                round(preventive_ratio_adult, 2),
                                round(preventive_ratio_old, 2),
                                round(preventive_ratio_total, 2),
                            ],
                            [
                                "Early Intervention Ratio",
                                round(early_intervention_ratio_male, 2),
                                round(early_intervention_ratio_female, 2),
                                round(early_intervention_ratio_child, 2),
                                round(early_intervention_ratio_teen, 2),
                                round(early_intervention_ratio_adult, 2),
                                round(early_intervention_ratio_old, 2),
                                round(early_intervention_ratio_total, 2),
                            ],
                            [
                                "% Recall",
                                str(round(recall_percent_male, 2)) + "%",
                                str(round(recall_percent_female, 2)) + "%",
                                str(round(recall_percent_child, 2)) + "%",
                                str(round(recall_percent_teen, 2)) + "%",
                                str(round(recall_percent_adult, 2)) + "%",
                                str(round(recall_percent_old, 2)) + "%",
                                str(round(recall_percent_total, 2)) + "%",
                            ],
                        ]
                    )
                return Response(
                    {"treatment_obj": "do not have a permission"}, status=400
                )
            return Response(
                {"message": "End date must be greated then Start Date"}, status=400
            )
        return Response({"message": serializer.errors}, status=400)
