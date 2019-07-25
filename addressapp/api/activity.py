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
        # if request.method == 'GET':
        #     return True
        return request.user and request.user.is_authenticated


class ActivityAreaListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = ActivityAreaSerializer

    def get(self, request, format=None):
        activityarea_obj = ActivityArea.objects.filter(status=True)
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


class ActivityAreaUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = ActivityAreaSerializer

    def get(self, request, pk, format=None):
        if request.user.admin:
            if ActivityArea.objects.filter(id=pk,status=True).exists():  
                activity_obj = ActivityArea.objects.get(id=pk,status=True)
                serializer = ActivityAreaSerializer(activity_obj, many=False, \
                    context={'request': request})
                return Response(serializer.data)
            return Response({"message":"content not found"},status=204)
        return Response({"message":"only admin can see"},status=400)

    def put(self, request, pk, format=None):
        if request.user.admin:
            if ActivityArea.objects.filter(id=pk,status=True).exists():
                activity_obj = ActivityArea.objects.get(id=pk)
                serializer = ActivityAreaSerializer(activity_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    activity_obj.name = serializer.validated_data['name']
                    activity_obj.save()
                    return Response({"message":"activity update"},status=200)
                # logger.error(serializer.errors)
                return Response({'message':serializer.errors}, status=400)
            # logger.error("content not found")
            return Response({"message":"content not found"},status=204)
        # logger.error("only admin can edit")
        return Response({"message":"only admin can edit"},status=400)


    def delete(self, request, pk, format=None):
        if request.user.admin:
            if ActivityArea.objects.filter(id=pk,status=True).exists():
                activity_obj = ActivityArea.objects.get(id=pk)
                activity_obj.status = False
                activity_obj.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"message":"no content found"},status=204)
        return Response({'errors': 'Permission Denied'},status=400)     