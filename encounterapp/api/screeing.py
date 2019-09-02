import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import Screeing, Encounter

from patientapp.serializers.patient import PatientSerializer
from encounterapp.serializers.screeing import PatientScreeingSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientScreeingView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientScreeingSerializer


    def get(self, request, encounter_id,format=None):
        if Screeing.objects.select_related('encounter_id').filter(encounter_id__uid=encounter_id).exists():
            screeing_obj = Screeing.objects.select_related('encounter_id').get(encounter_id__uid=encounter_id)
            serializer = PatientScreeingSerializer(screeing_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found"},status=400)


    def post(self, request, encounter_id, format=None):
        serializer = PatientScreeingSerializer(data=request.data,\
            context={'request': request})
        if Encounter.objects.filter(uid=encounter_id).exists():
            encounter_obj = Encounter.objects.get(uid=encounter_id)
            if Screeing.objects.select_related('encounter_id').filter(encounter_id=encounter_obj).exists():
                return Response({"message":"encounter id is already exists."},status=400)
            if serializer.is_valid():
                serializer.save(encounter_id=encounter_obj)
                return Response({"message":"screeing data added successfully"},status=200)
            logger.error(serializer.errors) 
            return Response({'message':serializer.errors}, status=400)
        logger.error("patient does not exists.") 
        return Response({"message":"patient does not exists."},status=400)


class PatientScreeingUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientScreeingSerializer

    def get(self, request, encounter_id, format=None):
        if Screeing.objects.select_related('encounter_id').filter(encounter_id__uid=encounter_id).exists():    
            screeing_obj = Screeing.objects.select_related('encounter_id').get(encounter_id__uid=encounter_id)
            serializer = PatientScreeingSerializer(screeing_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found."},status=400)

    def put(self, request, encounter_id, format=None):
        today_date = datetime.now()
        if Screeing.objects.select_related('encounter_id').filter(encounter_id__uid=encounter_id).exists():
            screeing_obj = Screeing.objects.select_related('encounter_id').get(encounter_id__uid=encounter_id)
            encounter_obj = Encounter.objects.get(uid=encounter_id)
            if today_date.timestamp() < encounter_obj.updated_at.timestamp():
                serializer = PatientScreeingSerializer(screeing_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save(updated_by = request.user,updated_date = datetime.datetime.now().date())
                    return Response({"message":"screeing encounter update"},status=200)
                logger.error(serializer.errors)
                return Response({'message':serializer.errors}, status=400)
            logger.error("update allow upto 24 hour only")
            return Response({"message":"update allow upto 24 hour only"},status=400)
        logger.error("screeing encounter id donot match")
        return Response({"message":"id do not match"},status=400) 
   