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

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class Visualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id,admin=True):
            other=[]
            male=[]
            female=[]
            female_count = Patient.objects.filter(gender='female').count()
            male_count = Patient.objects.filter(gender='male').count()
            other_count = Patient.objects.filter(gender='other').count()
            female.append(female_count)
            male.append(male_count)
            other.append(other_count)
            locationChart = {
            'data': {
            'labels': ['Female', 'Male', 'Other'],
            'datasets': [{
            'label': "Total",
            'backgroundColor': ['rgba(239, 62, 54, 0.2)', 'rgba(64, 224, 208, 0.2)', 'rgba(182, 198, 73, 0.2)'],
            'borderColor': ['rgba(239, 62, 54, 1)', 'rgba(64, 224, 208, 1)', 'rgba(182, 198, 73, 1)'],
            'borderWidth': 1,
            'data': [female,male,other]},
            ]},
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
            'text': "Gender-wise Patients Distribution",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"
            },
            'legend': {
            'display': 'true',
            'position': 'bottom',
            'labels': {
            'usePointStyle': 'true',
            'padding': 20,
            'fontFamily': "'Maven Pro', sans-serif"}
                    }
                }
            }
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can create"},status=400)



class Visualization1(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, format=None):
        if User.objects.get(id=request.user.id,admin=True):
            district=['Kids', 'Adults', 'Other Adults']
            total=[]
            male=[]
            female=[]
            patient_objlist=Patient.objects.all()
            # for patient_obj in patient_objlist:
            #     district.append(patient_obj.city)
            # district = list(dict.fromkeys(district))
            female_count = Patient.objects.filter(gender='female').count()
            male_count = Patient.objects.filter(gender='male').count()
            total_patient = Patient.objects.all().count()
            female.append(female_count)
            male.append(male_count)
            total.append(total_patient)
            female_count = Patient.objects.filter(gender='female').count()
            male_count = Patient.objects.filter(gender='male').count()
            total_patient = Patient.objects.all().count()
            female.append(female_count)
            male.append(male_count)
            total.append(total_patient)
            female_count = Patient.objects.filter(gender='female').count()
            male_count = Patient.objects.filter(gender='male').count()
            total_patient = Patient.objects.all().count()
            female.append(female_count)
            male.append(male_count)
            total.append(total_patient)

            locationChart = {
            'data': {
            'labels': district,
            'datasets': [{
            'label': "Total",
            'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            'borderColor': 'rgba(255, 206, 86, 1)',
            'borderWidth': 1,
            'data': total},
            {
            'label': "Female",
            'backgroundColor': 'rgba(239, 62, 54, 0.2)',
            'borderColor': 'rgba(239, 62, 54, 1)',
            'borderWidth': 1,
            'data': female},
            {
            'label': "Male",
            'backgroundColor': 'rgba(64, 224, 208, 0.2)',
            'borderColor': 'rgba(64, 224, 208, 1)',
            'borderWidth': 1,
            'data': male}]
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
            'text': "Age-wise Gender Distribution",
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


# class Visualization(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = VisualizatioSerializer

#     def get(self, request, format=None):
#         if request.user.admin:
#             district=[]
#             total=[]
#             male=[]
#             female=[]
#             patient_objlist=Patient.objects.all()
#             for patient_obj in patient_objlist:
#                 female_count = Patient.objects.filter(gender='female',city=patient_obj.city).count()
#                 male_count = Patient.objects.filter(gender='male',city=patient_obj.city).count()
#                 total_patient = Patient.objects.filter(city=patient_obj.city).count()
#                 district.append(patient_obj.city)
#                 female.append(female_count)
#                 male.append(male_count)
#                 total.append(total_patient)
#             # width of the bars
#             district = list(dict.fromkeys(district))
#             barWidth = 0.3
#             bars1 = male
#             bars2 = female
#             # The x position of bars
#             r1 = np.arange(len(bars1))
#             r2 = [x + barWidth for x in r1]
#             # Create blue bars
#             plt.bar(r1, bars1, width = barWidth, color = 'blue', edgecolor = 'black', capsize=7, label='male')
#             # Create cyan bars
#             plt.bar(r2, bars2, width = barWidth, color = 'cyan', edgecolor = 'black', capsize=7, label='female')
#             # general layout
#             plt.xticks([r + barWidth for r in range(len(bars1))], district)
#             plt.ylabel('height')
#             plt.legend()
#             # plt.tight_layout()
#             plt.savefig(os.path.join('media/location.png'), bbox_inches='tight')
#             return Response({"message":"data created"},status=200)
#         return Response({"message":"only admin can create"},status=400)



# class Visualization1(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     def get(self, request, format=None):
#         if request.user.admin:
#             district=['Kids', 'Teens', 'Adults', 'Other Adults']
#             total=[5, 3, 8, 6]
#             male=[3, 1, 4, 1]
#             female=[2, 2, 4, 5]
#             other=[]
#             patient_objlist=Patient.objects.all()
#             for patient_obj in patient_objlist:
#                 district.append(patient_obj.city)
#             district = list(dict.fromkeys(district))
#             for dist in district:
#                 female_count = Patient.objects.filter(gender='female',city=dist).count()
#                 male_count = Patient.objects.filter(gender='male',city=dist).count()
#                 other_count = Patient.objects.filter(gender='other',city=dist).count()
#                 total_patient = Patient.objects.filter(city=dist).count()
#                 female.append(female_count)
#                 male.append(male_count)
#                 total.append(total_patient)
#                 other.append(other_count)

#             locationChart = {
#             'data': {
#             'labels': district,
#             'datasets': [{
#             'label': "Total",
#             'backgroundColor': 'rgba(255, 206, 86, 0.2)',
#             'borderColor': 'rgba(255, 206, 86, 1)',
#             'borderWidth': 1,
#             'data': total},
#             {
#             'label': "Female",
#             'backgroundColor': 'rgba(239, 62, 54, 0.2)',
#             'borderColor': 'rgba(239, 62, 54, 1)',
#             'borderWidth': 1,
#             'data': female},
#             {
#             'label': "Male",
#             'backgroundColor': 'rgba(64, 224, 208, 0.2)',
#             'borderColor': 'rgba(64, 224, 208, 1)',
#             'borderWidth': 1,
#             'data': male},
#             {
#             'label': "Other",
#             'backgroundColor': 'rgba(182, 198, 73, 0.2)',
#             'borderColor': 'rgba(182, 198, 73, 1)',
#             'borderWidth': 1,
#             'data': other}]
#             },
#             'options': {
#             'aspectRatio': 1.5,
#             'scales': {
#             'yAxes': [{
#             'ticks': {
#             'beginAtZero':'true'}
#             }]
#             },
#             'title': {
#             'display': 'true',
#             'text': "Age-wise Gender Distribution",
#             'fontSize': 18,
#             'fontFamily': "'Palanquin', sans-serif"
#             },
#             'legend': {
#             'display': 'true',
#             'position': 'bottom',
#             'labels': {
#             'usePointStyle': 'true',
#             'padding': 20,
#             'fontFamily': "'Maven Pro', sans-serif"
#       }
#     }
#   }
#             }
#             return JsonResponse({"locationChart":locationChart})
#         return Response({"message":"only admin can create"},status=400)
