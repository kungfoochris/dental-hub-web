import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from patientapp.models import Patient

from patientapp.serializers.patient import PatientSerializer, PatientUpdateSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from addressapp.models import ActivityArea, Ward, Activity
from addressapp.models import Address,Ward,Municipality,District
import datetime

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

    def get(self, request, geography_id,format=None):
        if Patient.objects.filter(geography__id=geography_id):
            patient_obj = Patient.objects.filter(geography__id=geography_id).order_by("-date")
            serializer = PatientSerializer(patient_obj, many=True, context={'request': request})
            return Response(serializer.data,status=200)
        return Response({"message":"content not found"},status=204)

class GeographyPatientListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientSerializer

    def get(self, request,format=None):
        if CustomUser.objects.filter(id=request.user.id):
            user_obj = CustomUser.objects.get(id=request.user.id)
            add_patient=Patient.objects.none()
            for i in user_obj.location.all():
                patient_obj = Patient.objects.select_related('geography').filter(geography=i).order_by("-date")
                add_patient |= patient_obj
            serializer = PatientSerializer(add_patient, many=True, context={'request': request})
            return Response(serializer.data,status=200)
        return Response({"message":"only app user can access."},status=400)

class PatientAdd(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name','full_name')
    def get(self, request,format=None):
        if User.objects.filter(id=request.user.id).exists():
            patient_obj = Patient.objects.all().order_by("-date")
            serializer = PatientSerializer(patient_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"do not have a permission"},status=400)

    def post(self, request,format=None):
        serializer = PatientSerializer(data=request.data,\
            context={'request': request})
        if serializer.is_valid():
<<<<<<< HEAD
            print(serializer.validated_data['district_id'].id)
            print(serializer.validated_data['municipality_id'].id)
            print(serializer.validated_data['ward_id'].id)
            p = Patient.objects.filter(first_name=serializer.validated_data['first_name'],last_name=serializer.validated_data['last_name'],phone=serializer.validated_data['phone'],dob=serializer.validated_data['dob'],gender=serializer.validated_data['gender']).first()
        
=======
>>>>>>> 5a65c92dd9443457b14629d75ff61b02204bf284
            if Patient.objects.filter(first_name=serializer.validated_data['first_name'],last_name=serializer.validated_data['last_name'],phone=serializer.validated_data['phone'],dob=serializer.validated_data['dob'],gender=serializer.validated_data['gender']).count()==0:
                ward_obj = serializer.validated_data['geography_id']
                if Ward.objects.filter(id=serializer.validated_data['geography_id']).exists():
                    ward_obj = Ward.objects.get(id=serializer.validated_data['geography_id'])
                activity_area_obj = serializer.validated_data['activityarea_id']
                if Activity.objects.filter(id=activity_area_obj).exists():
                    activity_area_obj = Activity.objects.get(id=activity_area_obj)

                patient_obj = Patient()
                if serializer.validated_data['recall_geography']==None:
                    patient_obj.first_name = serializer.validated_data['first_name']
                    patient_obj.last_name = serializer.validated_data['last_name']
                    patient_obj.middle_name = serializer.validated_data['middle_name']
                    patient_obj.gender = serializer.validated_data['gender']
                    patient_obj.dob = serializer.validated_data['dob']
                    patient_obj.phone = serializer.validated_data['phone']
                    patient_obj.latitude = serializer.validated_data['latitude']
                    patient_obj.longitude = serializer.validated_data['longitude']
                    patient_obj.ward = serializer.validated_data['ward_id']
                    patient_obj.municipality = serializer.validated_data['municipality_id']
                    patient_obj.district = serializer.validated_data['district_id']
                    patient_obj.author = serializer.validated_data['author']
                    patient_obj.activity_area = activity_area_obj
                    patient_obj.geography = ward_obj
                    patient_obj.education = serializer.validated_data['education']
                    patient_obj.created_at = serializer.validated_data['created_at']
                    # patient_obj.recall_date = serializer.validated_data['recall_date']
                    patient_obj.recall_time = serializer.validated_data['recall_time']
                    patient_obj.area = serializer.validated_data['area']
                    patient_obj.save()
                else:
                    patient_obj.first_name = serializer.validated_data['first_name']
                    patient_obj.last_name = serializer.validated_data['last_name']
                    patient_obj.middle_name = serializer.validated_data['middle_name']
                    patient_obj.gender = serializer.validated_data['gender']
                    patient_obj.dob = serializer.validated_data['dob']
                    patient_obj.phone = serializer.validated_data['phone']
                    patient_obj.latitude = serializer.validated_data['latitude']
                    patient_obj.longitude = serializer.validated_data['longitude']
                    patient_obj.ward = serializer.validated_data['ward_id']
                    patient_obj.municipality = serializer.validated_data['municipality_id']
                    patient_obj.district = serializer.validated_data['district_id']
                    patient_obj.author = serializer.validated_data['author']
                    patient_obj.activity_area = activity_area_obj
                    patient_obj.geography = ward_obj
                    patient_obj.education = serializer.validated_data['education']
                    patient_obj.created_at = serializer.validated_data['created_at']
                    # patient_obj.recall_date = serializer.validated_data['recall_date']
                    patient_obj.recall_time = serializer.validated_data['recall_time']
                    patient_obj.recall_geography = serializer.validated_data['recall_geography']
                    patient_obj.area = serializer.validated_data['area']
                    patient_obj.save()
                logger.info("%s %s, %s %s, %s %s, %s %s, %s %s, %s %s ,%s %s, %s %s, %s %s, %s %s, %s %s, %s %s" %("Patient added successfully by", request.user.full_name,"Patient id:",patient_obj.id,"first name:",patient_obj.first_name,"last name:",patient_obj.last_name,"phone:",patient_obj.phone,"dob:",patient_obj.dob,"gender:",patient_obj.gender,"ward:",patient_obj.ward.name,"Activity Area:",patient_obj.activity_area.name,"District:",patient_obj.district.name,"Geography:",patient_obj.geography.name,"Municipality:",patient_obj.municipality.name))
                return Response({"message":"Patient created successfully","id":patient_obj.id},status=200)
                    #logger.info("ActivityArea id does not exists in patient section")
                    #return Response({"message":"Activity id does not exists"}, status=400)
                # logger.info("Geography id does not exists in patient section created by="+request.user.full_name)
                # return Response({"message":"Geography id does not exists created by="+request.user.full_name}, status=400)
            logger.info("%s %s, %s %s, %s %s, %s %s, %s %s, %s %s, %s %s " %("Duplicate data added in by=",request.user.full_name,"Patient ID",p.id,"first name:",serializer.validated_data['first_name'],"last name:",serializer.validated_data['last_name'],"phone:",serializer.validated_data['phone'],"dob:",serializer.validated_data['dob'],"gender:",serializer.validated_data['gender']))
            return Response({"message":"duplicate data created by="+request.user.full_name},status=409)
        logger.info(serializer.errors)
        return Response({'message':serializer.errors}, status=400)


class PatientUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PatientUpdateSerializer

    def get(self, request, patient_id, format=None):
        if Patient.objects.filter(id=patient_id).exists():
            patient_obj = Patient.objects.get(id=patient_id)
            serializer = PatientSerializer(patient_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        logger.error('encounter content not found.')
        return Response({"message":"content not found."},status=400)

    def put(self, request, patient_id, format=None):
        if Patient.objects.filter(id=patient_id).exists():
            patient_obj = Patient.objects.get(id=patient_id)
            serializer = PatientUpdateSerializer(patient_obj,data=request.data,\
                context={'request': request},partial=True)
            if serializer.is_valid():
                patient_obj.first_name = serializer.validated_data['first_name']
                patient_obj.last_name = serializer.validated_data['last_name']
                patient_obj.middle_name = serializer.validated_data['middle_name']
                patient_obj.gender = serializer.validated_data['gender']
                patient_obj.dob = serializer.validated_data['dob']
                patient_obj.phone = serializer.validated_data['phone']
                patient_obj.ward = serializer.validated_data['ward_id']
                patient_obj.municipality = serializer.validated_data['municipality_id']
                patient_obj.district = serializer.validated_data['district_id']
                patient_obj.education = serializer.validated_data['education']
                patient_obj.updated_by = serializer.validated_data['updated_by']
                patient_obj.updated_at = serializer.validated_data['updated_at']
                patient_obj.save()
                serializer.save()
                logger.info("%s %s" %("Patient update successfully by", request.user.full_name))
                return Response({"message":"patient update"},status=200)
            logger.info(serializer.errors)
            return Response({'message':serializer.errors}, status=400)
        logger.info("encounter id donot match")
        return Response({"message":"id do not match"},status=400)
