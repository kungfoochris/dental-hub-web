import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from encounterapp.models import Encounter, Refer, History
from patientapp.models import Patient
from encounterapp.serializers.encounter import EncounterSerializer,AllEncounterSerializer



from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class EncounterView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterSerializer


    def get(self, request,patient_id, format=None):
        patient_obj = Patient.objects.get(id=patient_id)
        encounter_obj = Encounter.objects.select_related('patient').filter(patient=patient_obj)
        serializer = AllEncounterSerializer(encounter_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

    def post(self, request, patient_id, format=None):
        serializer = EncounterSerializer(data=request.data,\
            context={'request': request})
        if Patient.objects.filter(id=patient_id).exists():
            patient_obj = Patient.objects.get(id=patient_id)
            if serializer.is_valid():
            	serializer.save(patient=patient_obj,author=request.user)
            	return Response(serializer.data,status=200)
            return Response({'message':serializer.errors}, status=400)
        return Response({"message":"patient does not exists"},status=400)

class EncounterUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterSerializer

    def get(self, request, patient_id, encounter_id, format=None):
        if Encounter.objects.select_related('patient').filter(patient__id=patient_id).exists():    
            encounter_obj = Encounter.objects.get(id=encounter_id)
            serializer = EncounterSerializer(encounter_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found."},status=400)

    def put(self, request, patient_id, encounter_id, format=None):
        today_date = datetime.now()
        if Encounter.objects.select_related('patient').filter(patient__id=patient_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if today_date.timestamp() < encounter_obj.update_date.timestamp():
                serializer = EncounterSerializer(encounter_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"encounter update"},status=200)
                return Response({'message':serializer.errors}, status=400)
            return Response({"message":"update allow upto 24 hour only"},status=400)
        return Response({"message":"id do not match"},status=400)    