import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from treatmentapp.serializers.visualization import VisualizatioSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.db.models import Count
from django.db.models.functions import TruncMonth
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from django.conf import settings
from dental.settings import MEDIA_ROOT
import os
from django.http import JsonResponse
# from pandas import DataFrame

from django.http import HttpResponse
from django.template import Context, loader
import csv
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class BarGraphData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        if request.user.admin:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
            male=[]
            female=[]
            patient_objlist=Patient.objects.all()
            for patient_obj in patient_objlist:
                female_count = Patient.objects.filter(gender='female').count()
                male_count = Patient.objects.filter(gender='male').count()
                female.append(female_count)
                male.append(male_count)
            writer = csv.writer(response)
            writer.writerow(male)
            writer.writerow(female)
            return response
        return Response({"message":"only admin can create"},status=400)

class PICHartGraphData(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request, format=None):
        if request.user.admin:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
            male=[]
            female=[]
            district=[]
            patient_objlist=Patient.objects.all()
            for patient_obj in patient_objlist:
                female_count = Patient.objects.filter(gender='female',city=patient_obj.city).count()
                male_count = Patient.objects.filter(gender='male',city=patient_obj.city).count()
                female.append(female_count)
                male.append(male_count)
                district.append(patient_obj.city)
            writer = csv.writer(response)
            writer.writerow(female)
            writer.writerow(male)
            writer.writerow(district)
            return response
        return Response({"message":"only admin can create"},status=400)




