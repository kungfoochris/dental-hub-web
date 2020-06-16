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
from addressapp.models import ActivityArea, Ward, Activity

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

    def post(self, request, patient_id, format=None):
        serializer = EncounterSerializer(data=request.data,\
            context={'request': request})
        if Patient.objects.filter(id=patient_id).exists():
            patient_obj = Patient.objects.get(id=patient_id)
            if serializer.is_valid():
                activity_area_obj = serializer.validated_data['activityarea_id']
                if Activity.objects.filter(id=activity_area_obj).exists():
                    activity_area_obj = Activity.objects.get(id=activity_area_obj)
                geography_obj = serializer.validated_data['geography_id']
                if Ward.objects.filter(id=serializer.validated_data['geography_id']).exists():
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
                logger.info("%s %s" %("Encounter added successfully by", request.user.full_name))
                return Response({"message":"Encounter added","id":encounter_obj.id},status=200)
                # logger.info("Geography id does not exists in encounter section.")
                # return Response({"message":"Geography id does not exists. created by="+request.user.full_name},status=400)
                # logger.info("Activity id does not exists in encounter section.")
                # return Response({"message":"Activity id does not exists."},status=400)
            logger.info(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
        logger.info("%s %s" %("Patient id does not exist in encounter section: created by="+request.user.full_name, patient_id))
        return Response({"message":"patient does not exists. created by="+request.user.full_name}, status=400)

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
                logger.info("%s %s" %("Encounter update successfully by", request.user.full_name))
                return Response({"message":"encounter update"},status=200)
            logger.info(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
        logger.info("%s %s" %("Patient id does not  exists in encounter section : ", patient_id))
        return Response({"message":"id do not match"},status=400)


