import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import Refer, Encounter

from treatmentapp.serializers.treatment import PatientTreatmentSerializer,PatientTreatmentUpdateSerializer
from treatmentapp.models import Treatment

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientTreatmentView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientTreatmentSerializer


    def get(self, request, encounter_id, format=None):
        if Treatment.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            treatment_obj = Treatment.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientTreatmentSerializer(treatment_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found"},status=400)

    def post(self, request, encounter_id, format=None):
        serializer = PatientTreatmentSerializer(data=request.data,\
            context={'request': request})
        if Encounter.objects.filter(id=encounter_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if Treatment.objects.select_related('encounter_id').filter(encounter_id=encounter_obj).exists():
                logger.info("%s %s" %("Encounter already exists in treatment section : ", encounter_id))
                return Response({"message":"encounter id is already exists."},status=409)
            if serializer.is_valid():
                serializer.save(encounter_id=encounter_obj)
                logger.info("%s %s" %("Treatment added successfully by", encounter_id))
                return Response(serializer.data,status=200)
            logger.error(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
        logger.info("%s %s" %("Encounter id does not exists in treatment section : ", encounter_id))
        return Response({"message":"patient does not exists."},status=400)

class PatientTreatmentUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientTreatmentUpdateSerializer

    def get(self, request, encounter_id, format=None):
        if Treatment.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            treatment_obj = Treatment.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientTreatmentSerializer(treatment_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found."},status=400)

    def put(self, request, encounter_id, format=None):
        if Treatment.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            treatment_obj = Treatment.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientTreatmentUpdateSerializer(treatment_obj,data=request.data,\
                context={'request': request},partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info("%s %s" %("Treatment Update successfully by a", encounter_id))
                return Response(serializer.data,status=200)
            logger.error(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
        logger.info("%s %s" %("Encounter id does not exists in treatment section : ", encounter_id))
        return Response({"message":"id do not match"},status=400)
