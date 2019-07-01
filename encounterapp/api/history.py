import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import History, Encounter

from patientapp.serializers.patient import PatientSerializer
from encounterapp.serializers.history import PatientHistorySerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientHistoryView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientHistorySerializer

    def get(self, request, encounter_id, format=None):
        if History.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            history_obj = History.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientHistorySerializer(history_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found"},status=400)

    def post(self, request, encounter_id, format=None):
        serializer = PatientHistorySerializer(data=request.data,\
            context={'request': request})
        if Encounter.objects.filter(id=encounter_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if History.objects.select_related('encounter_id').filter(encounter_id=encounter_obj).exists():
                return Response({"message":"encounter id is already exists."},status=400)
            if serializer.is_valid():
                # history_obj = History()
                # history_obj.bleeding = serializer.validated_data['bleeding']
                # history_obj.diabete = serializer.validated_data['diabete']
                # history_obj.liver = serializer.validated_data['liver']
                # history_obj.fever = serializer.validated_data['fever']
                # history_obj.seizures = serializer.validated_data['seizures']
                # history_obj.hepatitis = serializer.validated_data['hepatitis']
                # history_obj.hiv = serializer.validated_data['hiv']
                # history_obj.allergic = serializer.validated_data['allergic']
                # history_obj.other = serializer.validated_data['other']
                # history_obj.medication = serializer.validated_data['medication']
                # history_obj.encounter_id = encounter_obj
                serializer.save(encounter_id=encounter_obj)
                return Response({"message":"encounter added"},status=200)
            return Response({'message':serializer.errors}, status=400) 
        return Response({"message":"patient does not exists."},status=400)


class PatientHistoryUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientHistorySerializer

    def get(self, request, encounter_id, format=None):
        if History.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():    
            history_obj = History.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            serializer = PatientHistorySerializer(history_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found."},status=400)

    def put(self, request, encounter_id, format=None):
        today_date = datetime.now()
        if History.objects.select_related('encounter_id').filter(encounter_id__id=encounter_id).exists():
            history_obj = History.objects.select_related('encounter_id').get(encounter_id__id=encounter_id)
            encounter_obj = Encounter.objects.get(id=encounter_id)
            if today_date.timestamp() < encounter_obj.update_date.timestamp():
                serializer = PatientHistorySerializer(history_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"history encounter update"},status=200)
                return Response({'message':serializer.errors}, status=400)
            return Response({"message":"update allow upto 24 hour only"},status=400)
        return Response({"message":"id do not match"},status=400)     


