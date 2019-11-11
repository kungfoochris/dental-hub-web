
import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userapp.models import User
from django.http import JsonResponse

from rest_framework import filters

from addressapp.models import Ward, Geography
from patientapp.models import Patient
from django.db.models.functions import TruncMonth
from django.db.models import Count
import random


class WardlineVisualization(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Patient.objects.filter(geography__id=i.id).exists():
                        total_patient = Patient.objects.filter(geography__id=i.id,created_at__month=x).count()
                        v.append(total_patient)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)"]
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 2.2,
            'title': {
            'display': 'true',
            'text': "Month-wise contact distribution",
            'fontSize': 18,
            'fontFamily': "'Palanquin', sans-serif"
            },
            'legend': {
            'position': "bottom"
            },
            'labels':{
            'usePointStyle': 'true'
            },
            'scales': {
            'yAxes': [{
            'ticks': {
            'fontColor': "rgba(0,0,0,0.5)",
            'fontStyle': "bold",
            'beginAtZero': 'false',
            'maxTicksLimit': 6,
            'padding': 20
            },
            'gridLines': {
            'drawTicks': 'true',
            'display': 'true'
            }
            }],
            'xAxes': [{
            'gridLines': {
            'zeroLineColor': "transparent"
            },
            'ticks': {
            'padding': 20,
            'fontColor': "rgba(0,0,0,0.5)",
            'fontStyle': "bold"
            }}]}}
            }
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)
