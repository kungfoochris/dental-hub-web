import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import Refer, Encounter

from visualizationapp.serializers.visualization import DataVisualizationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from visualizationapp.models import Visualization

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class DataVisualization(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = DataVisualizationSerializer


    def get(self, request, format=None):
        visualization_obj = Visualization.objects.all()
        serializer = DataVisualizationSerializer(visualization_obj, many=True, \
        context={'request': request})
        return Response(serializer.data)
