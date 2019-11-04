
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
class WardlineVisualization(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                if Patient.objects.filter(geography__id=i.id).exists():
                    total_patient = Patient.objects.filter(geography__id=i.id).count()
                    geography.append(i.name)
                    geography_patient.append(round(total_patient,2))
            labels_data=["Preventive Ratio","Early Intervention Ratio","% Recall"]
            data_data=[]
            locationChart = {
            'data': {
            'labels': geography,
            'datasets': [
            {
            'label': "Total",
            'backgroundColor': 'rgba(255, 206, 86, 0.2)',
            'borderColor': 'rgba(255, 206, 86, 1)',
            'borderWidth': 1,
            'data': geography_patient
            },]},
            'options': {
            'aspectRatio': 2.2,
            'scales': {
            'yAxes': [{
            'ticks': {
            'beginAtZero': 'true'
            }
            }]},
            'title': {
            'display': 'true',
            #'text': "Location Chart",
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
            }}}}
            return JsonResponse({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)
