import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import Encountertype, Encounter
from encounterapp.serializers.encounter_type import EncountertypeSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class EncounterTypeView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncountertypeSerializer


    def get(self, request, format=None):
        encountertype_obj = Encountertype.objects.all()
        serializer = EncountertypeSerializer(encountertype_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EncountertypeSerializer(data=request.data,\
            context={'request': request})
        if Encounter.objects.filter(id=request.data['encounter_id']).exists():
            encounter_obj = Encounter.objects.get(id=request.data['encounter_id'])
            if serializer.is_valid():
                encountertype_obj = Encountertype()
                encountertype_obj.screeing = serializer.validated_data['screeing']
                encountertype_obj.pain = serializer.validated_data['pain']
                encountertype_obj.check = serializer.validated_data['check']
                encountertype_obj.treatment = serializer.validated_data['treatment']
                encountertype_obj.encounter_id = encounter_obj
                encountertype_obj.save()
                return Response(serializer.data,status=200)
            return Response({'message':serializer.errors}, status=400) 
        return Response({"message":"patient does not exists."},status=400)    