import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from encounterapp.models import Encounter, Refer, History
from patientapp.models import Patient
from encounterapp.serializers.encounter import EncounterSerializer,AllEncounterSerializer



from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from addressapp.models import Geography, ActivityArea, Ward, Activity

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class EncounterView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterSerializer


    def get(self, request,patient_id, format=None):
        if User.objects.filter(id=request.user.id,admin=True):
            patient_obj = Patient.objects.get(uid=patient_id)
            encounter_obj = Encounter.objects.select_related('patient').filter(patient=patient_obj)
            serializer = AllEncounterSerializer(encounter_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
        elif CustomUser.objects.filter(id=request.user.id):
            patient_obj = Patient.objects.get(uid=patient_id)
            encounter_obj = Encounter.objects.select_related('geography').filter(geography=patient_obj.geography)
            serializer = AllEncounterSerializer(encounter_obj, many=True,\
                context={'request': request})
            return Response(serializer.data)
    def post(self, request, patient_id, format=None):
        serializer = EncounterSerializer(data=request.data,\
            context={'request': request})
        if Patient.objects.filter(uid=patient_id).exists():
            patient_obj = Patient.objects.get(uid=patient_id)
            if serializer.is_valid():
                if Activity.objects.filter(id=serializer.validated_data['activityarea_id']).exists():
                    if Geography.objects.filter(id=serializer.validated_data['geography_id']).exists():
                        activity_area_obj = Activity.objects.get(id=serializer.validated_data['activityarea_id'])
                        geography_obj = Geography.objects.get(id=serializer.validated_data['geography_id'])
                        encounter_obj = Encounter()
                        encounter_obj.encounter_type = serializer.validated_data['encounter_type']
                        encounter_obj.activity_area = activity_area_obj
                        encounter_obj.geography = geography_obj
                        encounter_obj.patient = patient_obj
                        encounter_obj.author = request.user
                        encounter_obj.save()
                        return Response({"message":"Encounter added","uid":encounter_obj.uid},status=200)
                    logger.error("Geography id does not exists.")
                    return Response({"message":"Geography id does not exists."},status=400)
                logger.error("Activity id does not exists.")
                return Response({"message":"Activity id does not exists."},status=400)
            logger.error(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
        logger.error('patient does not exists')
        return Response({"message":"patient does not exists"},status=400)

class EncounterUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterSerializer

    def get(self, request, patient_id, encounter_id, format=None):
        if Encounter.objects.select_related('patient').filter(uid=encounter_id,patient__uid=patient_id).exists():    
            encounter_obj = Encounter.objects.get(uid=encounter_id)
            serializer = EncounterSerializer(encounter_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        logger.error('encounter content not found.')
        return Response({"message":"content not found."},status=400)

    def put(self, request, patient_id, encounter_id, format=None):
        today_date = datetime.now()
        if Encounter.objects.select_related('patient').filter(uid=encounter_id,patient__uid=patient_id).exists():
            encounter_obj = Encounter.objects.get(uid=encounter_id)
            if today_date.timestamp() < encounter_obj.updated_at.timestamp():
                serializer = EncounterSerializer(encounter_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"encounter update"},status=200)
                logger.error(serializer.errors)
                return Response({'message':serializer.errors}, status=400)
            logger.error("update allow upto 24 hour only")
            return Response({"message":"update allow upto 24 hour only"},status=400)
        logger.error("encounter id donot match")
        return Response({"message":"id do not match"},status=400)    