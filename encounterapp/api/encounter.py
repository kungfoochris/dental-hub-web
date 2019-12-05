import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from encounterapp.models import Encounter, Refer, History
from patientapp.models import Patient
from encounterapp.serializers.encounter import EncounterSerializer,\
AllEncounterSerializer,EncounterUpdateSerializer



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
        if User.objects.filter(id=request.user.id):
            if Patient.objects.filter(id=patient_id):
                if Encounter.objects.select_related('patient').filter(patient__id=patient_id).exists():
                    encounter_obj = Encounter.objects.select_related('patient').filter(patient__id=patient_id)
                    serializer = AllEncounterSerializer(encounter_obj, many=True,\
                        context={'request': request})
                    return Response(serializer.data)
                return Response({"message":'encounter not added or not found'},status=400)
            return Response({"message":"patient id does not exist."},status=400)
        return Response({"message":"permission not allowed"},status=400)
        # if User.objects.filter(id=request.user.id,admin=True):
        #     patient_obj = Patient.objects.get(id=patient_id)
        #     encounter_obj = Encounter.objects.select_related('patient').filter(patient=patient_obj)
        #     serializer = AllEncounterSerializer(encounter_obj, many=True, \
        #         context={'request': request})
        #     return Response(serializer.data)

    def post(self, request, patient_id, format=None):
        serializer = EncounterSerializer(data=request.data,\
            context={'request': request})
        if Patient.objects.filter(id=patient_id).exists():
            patient_obj = Patient.objects.get(id=patient_id)
            if serializer.is_valid():
                if Activity.objects.filter(id=serializer.validated_data['activityarea_id']).exists():
                    if Ward.objects.filter(id=serializer.validated_data['geography_id']).exists():
                        activity_area_obj = Activity.objects.get(id=serializer.validated_data['activityarea_id'])
                        geography_obj = Ward.objects.get(id=serializer.validated_data['geography_id'])
                        encounter_obj = Encounter()
                        encounter_obj.encounter_type = serializer.validated_data['encounter_type']
                        encounter_obj.activity_area = activity_area_obj
                        encounter_obj.geography = geography_obj
                        encounter_obj.patient = patient_obj
                        encounter_obj.author = patient_obj.author
                        encounter_obj.other_problem = serializer.validated_data['other_problem']
                        encounter_obj.created_at = serializer.validated_data['created_at']
                        encounter_obj.save()
                        logger.error("Encounter added successfully.")
                        return Response({"message":"Encounter added","id":encounter_obj.id},status=200)
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
    serializer_class = EncounterUpdateSerializer

    def get(self, request, patient_id, encounter_id, format=None):
        if Encounter.objects.select_related('patient').filter(id=encounter_id,patient__id=patient_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            serializer = EncounterSerializer(encounter_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        logger.error('encounter content not found.')
        return Response({"message":"content not found or parameter not match."},status=400)

    def put(self, request, patient_id, encounter_id, format=None):
        today_date = datetime.now()
        if Encounter.objects.select_related('patient').filter(id=encounter_id,patient__id=patient_id).exists():
            encounter_obj=Encounter.objects.select_related('patient').get(id=encounter_id,patient__id=patient_id)
            serializer = EncounterUpdateSerializer(encounter_obj,data=request.data,\
                context={'request': request},partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.error("Encounter updated successfully.")
                return Response({"message":"encounter update"},status=200)
                logger.error(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
            logger.error("update allow upto 24 hour only")
        logger.error("encounter id donot match")
        return Response({"message":"id do not match"},status=400)
