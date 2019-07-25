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
from addressapp.models import Geography, ActivityArea

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class PatientListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name','full_name')

    def get(self, request, format=None):
        if request.user.admin:
            patient_obj = Patient.objects.all().order_by("-date")
            serializer = PatientSerializer(patient_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
        else:
            geography = Geography.objects.filter(user=request.user)
            print(geography)
            for i in geography:
                patient_obj = Patient.objects.select_related('geography').filter(geography=i).order_by("-date")
                serializer = PatientSerializer(patient_obj, many=True, \
                    context={'request': request})
                return Response(serializer.data)
            return Response({"message":"content not found"},status=204)

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data,\
            context={'request': request})
        if serializer.is_valid():
            if Geography.objects.filter(id=serializer.validated_data['geography_id']).exists():
                if ActivityArea.objects.filter(id=serializer.validated_data['activityarea_id']).exists():
                    activity_area_obj = ActivityArea.objects.get(id=serializer.validated_data['activityarea_id'])
                    geography_obj = Geography.objects.get(id=serializer.validated_data['geography_id'])
                    patient_obj = Patient()
                    patient_obj.id = serializer.validated_data['id']
                    patient_obj.first_name = serializer.validated_data['first_name']
                    patient_obj.last_name = serializer.validated_data['last_name']
                    patient_obj.middle_name = serializer.validated_data['middle_name']
                    patient_obj.gender = serializer.validated_data['gender']
                    patient_obj.dob = serializer.validated_data['dob']
                    patient_obj.phone = serializer.validated_data['phone']
                    patient_obj.marital_status = serializer.validated_data['marital_status']
                    patient_obj.education = serializer.validated_data['education']
                    patient_obj.latitude = serializer.validated_data['latitude']
                    patient_obj.longitude = serializer.validated_data['longitude']
                    patient_obj.ward = serializer.validated_data['ward']
                    patient_obj.city = serializer.validated_data['city']
                    patient_obj.state = serializer.validated_data['state']
                    patient_obj.country = serializer.validated_data['country']
                    patient_obj.street_address =serializer.validated_data['street_address']
                    patient_obj.author = request.user
                    patient_obj.activity_area = activity_area_obj
                    patient_obj.geography = geography_obj
                    patient_obj.save()
                    return Response(serializer.data,status=200)
                logger.error("ActivityArea id does not exists")
                return Response({"message":"ActivityArea id does not exists"}, status=400)
            logger.error("Geography id does not exists")
            return Response({"message":"Geography id does not exists"}, status=400)
        logger.error(serializer.errors)
        return Response({'message':serializer.errors}, status=400)    