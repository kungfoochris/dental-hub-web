import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import Refer, Encounter

from encounterapp.serializers.refer import PatientReferSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientReferView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientReferSerializer


    def get(self, request, encounter_id, format=None):
        if Refer.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            refer_obj = Refer.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientReferSerializer(refer_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found"},status=400)

    def post(self, request, encounter_id, format=None):
        serializer = PatientReferSerializer(data=request.data,\
            context={'request': request})
        if Encounter.objects.filter(id=encounter_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if Refer.objects.select_related('encounter_id').filter(encounter_id=encounter_obj).exists():
                return Response({"message":"encounter id is already exists."},status=400)
            if serializer.is_valid():
                refer_obj = Refer()
                refer_obj.no_referal = serializer.validated_data['no_referal']
                refer_obj.health_post = serializer.validated_data['health_post']
                refer_obj.dentist = serializer.validated_data['dentist']
                refer_obj.physician = serializer.validated_data['physician']
                refer_obj.hygienist = serializer.validated_data['hygienist']
                refer_obj.encounter_id = encounter_obj
                refer_obj.save()
                return Response(serializer.data,status=200)
            return Response({'message':serializer.errors}, status=400) 
        return Response({"message":"patient does not exists."},status=400)

class PatientReferUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientReferSerializer

    def get(self, request, encounter_id, format=None):
        if Refer.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():    
            refer_obj = Refer.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientReferSerializer(refer_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found."},status=400)

    def put(self, request, encounter_id, format=None):
        today_date = datetime.now()
        if Refer.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            refer_obj = Refer.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if today_date.timestamp() < encounter_obj.update_date.timestamp():
                serializer = PatientReferSerializer(refer_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"refer encounter update"},status=200)
                return Response({'message':serializer.errors}, status=400)
            return Response({"message":"update allow upto 24 hour only"},status=400)
        return Response({"message":"id do not match"},status=400)     