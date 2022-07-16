import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from patientapp.models import Patient

from rest_framework import filters
from userapp.models import User
import os
from django.http import JsonResponse
from treatmentapp.models import Treatment
from encounterapp.models import Encounter
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class LoginVisualization(APIView):
      def get(self, request, format=None):
            health_post=[]
            school_seminar=[]
            community=[]
            training=[]
            health_count = Patient.objects.select_related('activity_area').filter(activity_area__name='Health Post').count()
            school_count = Patient.objects.select_related('activity_area').filter(activity_area__name='School Seminar').count()
            community_count = Patient.objects.select_related('activity_area').filter(activity_area__name='Community Outreach').count()
            training_count = Patient.objects.select_related('activity_area').filter(activity_area__name='Training').count()
            health_post.append(health_count)
            school_seminar.append(school_count)
            community.append(community_count)
            training.append(training_count)
            locationChart = {
            'data': {
            'labels': ['Health Post', 'School Seminar', 'Community Outreach', 'Training'],
            'datasets': [
            {
            'label': "Female",
            'backgroundColor': ['rgba(84, 184, 209, 0.5)', 'rgba(91, 95, 151, 0.5)', 'rgba(255, 193, 69, 0.5)', 'rgba(96, 153, 45, 0.5)'],
            'borderColor': ['rgba(84, 184, 209, 1)', 'rgba(91, 95, 151, 1)', 'rgba(255, 193, 69, 1)', 'rgba(96, 153, 45, 1)'],
            'borderWidth': 1,
            'data': [health_post, school_seminar, community, training]
            }]},
            'options': {
            'aspectRatio': 1.5,
            # 'scales': {
            # 'yAxes': [{
            # 'ticks': {
            # 'beginAtZero':'true'}
            # }]},
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
            return Response({"locationChart":locationChart})


class LoginVisualization1(APIView):
    def get(self, request, format=None):
        total_encounter = Encounter.objects.all().count()
        total_patient = Patient.objects.all().count()
        tooth18 = Treatment.objects.filter(tooth18="ART").count()
        tooth17 = Treatment.objects.filter(tooth17="ART").count()
        tooth16 = Treatment.objects.filter(tooth16="ART").count()
        tooth15 = Treatment.objects.filter(tooth15="ART").count()
        tooth14 = Treatment.objects.filter(tooth14="ART").count()
        tooth13 = Treatment.objects.filter(tooth13="ART").count()
        tooth12 = Treatment.objects.filter(tooth12="ART").count()
        tooth11 = Treatment.objects.filter(tooth11="ART").count()
        tooth21 = Treatment.objects.filter(tooth21="ART").count()
        tooth22 = Treatment.objects.filter(tooth22="ART").count()
        tooth23 = Treatment.objects.filter(tooth23="ART").count()
        tooth24 = Treatment.objects.filter(tooth24="ART").count()
        tooth25 = Treatment.objects.filter(tooth25="ART").count()
        tooth26 = Treatment.objects.filter(tooth26="ART").count()
        tooth27 = Treatment.objects.filter(tooth27="ART").count()
        tooth28 = Treatment.objects.filter(tooth28="ART").count()
        tooth48 = Treatment.objects.filter(tooth48="ART").count()
        tooth47 = Treatment.objects.filter(tooth47="ART").count()
        tooth46 = Treatment.objects.filter(tooth46="ART").count()
        tooth45 = Treatment.objects.filter(tooth45="ART").count()
        tooth44 = Treatment.objects.filter(tooth44="ART").count()
        tooth43 = Treatment.objects.filter(tooth43="ART").count()
        tooth42 = Treatment.objects.filter(tooth42="ART").count()
        tooth41 = Treatment.objects.filter(tooth41="ART").count()
        tooth31 = Treatment.objects.filter(tooth31="ART").count()
        tooth32 = Treatment.objects.filter(tooth32="ART").count()
        tooth33 = Treatment.objects.filter(tooth33="ART").count()
        tooth34 = Treatment.objects.filter(tooth34="ART").count()
        tooth35 = Treatment.objects.filter(tooth35="ART").count()
        tooth36 = Treatment.objects.filter(tooth36="ART").count()
        tooth37 = Treatment.objects.filter(tooth37="ART").count()
        tooth38 = Treatment.objects.filter(tooth38="ART").count()
        tooth55 = Treatment.objects.filter(tooth55="ART").count()
        tooth54 = Treatment.objects.filter(tooth54="ART").count()
        tooth53 = Treatment.objects.filter(tooth53="ART").count()
        tooth52 = Treatment.objects.filter(tooth52="ART").count()
        tooth51 = Treatment.objects.filter(tooth51="ART").count()
        tooth61 = Treatment.objects.filter(tooth61="ART").count()
        tooth62 = Treatment.objects.filter(tooth62="ART").count()
        tooth63 = Treatment.objects.filter(tooth63="ART").count()
        tooth64 = Treatment.objects.filter(tooth64="ART").count()
        tooth65 = Treatment.objects.filter(tooth65="ART").count()
        tooth85 = Treatment.objects.filter(tooth85="ART").count()
        tooth84 = Treatment.objects.filter(tooth84="ART").count()
        tooth83 = Treatment.objects.filter(tooth83="ART").count()
        tooth82 = Treatment.objects.filter(tooth82="ART").count()
        tooth81 = Treatment.objects.filter(tooth81="ART").count()
        tooth71 = Treatment.objects.filter(tooth71="ART").count()
        tooth72 = Treatment.objects.filter(tooth72="ART").count()
        tooth73 = Treatment.objects.filter(tooth73="ART").count()
        tooth74 = Treatment.objects.filter(tooth74="ART").count()
        tooth75 = Treatment.objects.filter(tooth75="ART").count()
        cavities_restored = tooth18 + tooth17 + tooth16 + tooth15 + tooth14 +\
         tooth13 + tooth12 +tooth11 + tooth21 + tooth22 + tooth23 + tooth24 +\
         tooth25 + tooth26 + tooth27 + tooth28 + tooth48 + tooth47 + tooth46 +\
         tooth45 + tooth44 + tooth43 + tooth42 + tooth41 + tooth31 + tooth32 +\
         tooth31 + tooth34 + tooth35 + tooth36 + tooth37 + tooth38 + tooth55 +\
         tooth54 + tooth53 + tooth52 + tooth51 + tooth61 + tooth62 + tooth63 +\
         tooth64 + tooth65 + tooth85 + tooth84 + tooth83 + tooth82 + tooth81 +\
         tooth71 + tooth72 + tooth73 + tooth74 + tooth75
        return Response({'total_encounter':total_encounter,'total_patient':total_patient,'cavities_restored':cavities_restored})
