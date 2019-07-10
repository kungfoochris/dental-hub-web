import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User

from addressapp.serializers.activity import ActivityAreaSerializer
from addressapp.models import ActivityArea

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated


class ActivityAreaListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = ActivityAreaSerializer

    def get(self, request, format=None):
        activityarea_obj = ActivityArea.objects.all()
        serializer = ActivityAreaSerializer(activityarea_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.admin:
            serializer = ActivityAreaSerializer(data=request.data,\
                context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            return Response({'message':serializer.errors}, status=400)
        return Response({"message":"you have to be admin"},status=400)     