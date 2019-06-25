import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User
from patientapp.models import Patient

from patientapp.serializers.patient import PatientSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name','full_name')

    def get(self, request, format=None):
        patient_obj = Patient.objects.all()
        serializer = PatientSerializer(patient_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data,\
            context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data,status=200)
        return Response({'message':serializer.errors}, status=400)     