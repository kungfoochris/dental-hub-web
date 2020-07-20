import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser
from encounterapp.models import Encounter, Refer, History
from patientapp.models import Patient

from flagapp.serializers.flag import FlagSerializer, FlagUpdateSerializer,\
    AllFlagSerializer
from django.contrib.contenttypes.models import ContentType

from flagapp.models import Flag

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class FlagListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = FlagSerializer


    def get(self, request, format=None):
        flag_obj = Flag.objects.all().order_by('-created_at')
        serializer = AllFlagSerializer(flag_obj, many=True,\
        context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FlagSerializer(data=request.data,\
            context={'request': request})
        if serializer.is_valid():
            try:
                content_type = ContentType.objects.get(model=serializer.validated_data['content_type'])
                content_obj = content_type.get_object_for_this_type(id=serializer.validated_data['object_id'])
                serializer.save(author=request.user, patient_name=content_obj.full_name)
            except:
                return Response("object id do not match")

            logger.info("%s %s" %("Flag added successfully by", request.user.full_name))
            return Response(serializer.data)
        logger.info(serializer.errors)
        return Response({'message':serializer.errors}, status=400)

class FlagUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = FlagUpdateSerializer

    def get(self, request, flag_id, format=None):
        if Flag.objects.filter(id=flag_id).exists():
            flag_obj = Flag.objects.get(id=flag_id)
            serializer = FlagSerializer(flag_obj, many=False, \
                context={'request': request})
            return Response(serializer.data)
        logger.error('flag content not found.')
        return Response({"message":"content not found or parameter not match."},status=400)

    def put(self, request, flag_id, format=None):
        if Flag.objects.filter(id=flag_id).exists():
            if Flag.objects.filter(id=flag_id,status=False).exists():
                flag_obj =Flag.objects.get(id=flag_id)
                serializer = FlagUpdateSerializer(flag_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    if Patient.objects.filter(id=flag_obj.object_id):
                        patient_obj = Patient.objects.get(id=flag_obj.object_id)
                        patient_obj.delete()
                        serializer.save()
                        logger.info("%s %s" %("Flag delete successfully by", request.user.full_name))
                        return Response({"message":"Flag delete"},status=200)
                    return Response({"message":"flag object_id does not found"},status=400)
                logger.info(serializer.errors)
                return Response({'message':serializer.errors}, status=400)
            return Response({"message":"Flag id already delete"},status=400)
        logger.info("%s %s" %("Flag id does not  exists in encounter section : ", patient_id))
        return Response({"message":"id do not match"},status=400)

    def delete(self, request, flag_id, format=None):
        if Flag.objects.filter(id=flag_id).exists():
            flag_obj = Flag.objects.get(id=flag_id)
            if flag_obj.status == False:
                try:
                    content_type = ContentType.objects.get(model=flag_obj.content_type.model)
                    content_obj = content_type.get_object_for_this_type(id=flag_obj.object_id)
                    content_obj.delete()

                    flag_obj.status = True
                    flag_obj.save()
                    return Response({"message":"Flag delete successfully."}, status=200)
                except:
                    return Response({"message":"Sorry could not delete a flag."}, status=200)
            return Response({"message":"This flag data is already deleted."}, status=400)
        return Response({'errors': 'Flag id do not match.'}, status=400)
