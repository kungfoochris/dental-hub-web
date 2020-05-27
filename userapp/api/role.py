import re
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login as dj_login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser, Role


from userapp.serializers.role import RoleSerializer


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class RoleListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = RoleSerializer

    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id,admin=True).exists():
            role_obj=Role.objects.all()
            serializer = RoleSerializer(role_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
            logger.error("Access is denied.")
        return Response({"message":"Access is denied."},status=400)

    def post(self, request, format=None):
        serializer = RoleSerializer(data=request.data,\
            context={'request': request})
        if User.objects.filter(id=request.user.id,admin=True).exists():
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message':serializer.errors}, status=400)
        logger.error("Access is denied.")
        return Response({"message":"Access is denied."},status=400)
