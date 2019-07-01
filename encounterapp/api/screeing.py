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

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientScreeingView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientScreeingSerializer


    def get(self, request, encounter_id,format=None):
        if Screeing.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            screeing_obj = Screeing.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientScreeingSerializer(screeing_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found"},status=400)


    def post(self, request, encounter_id, format=None):
        serializer = PatientScreeingSerializer(data=request.data,\
            context={'request': request})
        if Encounter.objects.filter(id=encounter_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if Screeing.objects.select_related('encounter_id').filter(encounter_id=encounter_obj).exists():
                return Response({"message":"encounter id is already exists."},status=400)
            if serializer.is_valid():
                screeing_obj = Screeing()
                screeing_obj.caries_risk = serializer.validated_data['caries_risk']
                screeing_obj.primary_teeth = serializer.validated_data['primary_teeth']
                screeing_obj.permanent_teeth = serializer.validated_data['permanent_teeth']
                screeing_obj.postiror_teeth = serializer.validated_data['postiror_teeth']
                screeing_obj.anterior_teeth = serializer.validated_data['anterior_teeth']
                screeing_obj.infection = serializer.validated_data['infection']
                screeing_obj.reversible_pulpitis = serializer.validated_data['reversible_pulpitis']
                screeing_obj.art = serializer.validated_data['art']
                screeing_obj.extraction = serializer.validated_data['extraction']
                screeing_obj.refernal_kdh = serializer.validated_data['refernal_kdh']
                screeing_obj.encounter_id = encounter_obj
                screeing_obj.save()
                return Response(serializer.data,status=200)
            return Response({'message':serializer.errors}, status=400) 
        return Response({"message":"patient does not exists."},status=400)


class PatientScreeingUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientScreeingSerializer

    def get(self, request, encounter_id, format=None):
        if Screeing.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():    
            screeing_obj = Screeing.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientScreeingSerializer(screeing_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found."},status=400)

    def put(self, request, encounter_id, format=None):
        today_date = datetime.now()
        if Screeing.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            screeing_obj = Screeing.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if today_date.timestamp() < encounter_obj.update_date.timestamp():
                serializer = PatientScreeingSerializer(screeing_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"screeing encounter update"},status=200)
                return Response({'message':serializer.errors}, status=400)
            return Response({"message":"update allow upto 24 hour only"},status=400)
        return Response({"message":"id do not match"},status=400) 
   