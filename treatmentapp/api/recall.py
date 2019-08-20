import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from patientapp.models import Patient
from treatmentapp.serializers.recall import RecallSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.http import JsonResponse
from encounterapp.models import Refer, Encounter

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class Recall(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request, geography_id ,format=None):
    	if Encounter.objects.select_related('geography').filter(geography__id=geography_id):
    		encounter_obj=Encounter.objects.select_related('geography').filter(geography__id=geography_id)
    		serializer = RecallSerializer(encounter_obj, many=True,context={'request': request})
    		return Response(serializer.data)
    	return Response({"message":"Bad parameter"},status=400)