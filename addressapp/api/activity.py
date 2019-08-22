import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser

from addressapp.serializers.activity import ActivitySerializer,ActivityAreaSerializer

from addressapp.models import Activity, ActivityArea

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated


class ActivityListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = ActivityAreaSerializer
    def get(self, request, format=None):
        activity_obj = Activity.objects.all()
        serializer = ActivitySerializer(activity_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

class ActivityAreaListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = ActivityAreaSerializer

    def get(self, request, format=None):
        activityarea_obj = ActivityArea.objects.filter(status=True)
        serializer = ActivityAreaSerializer(activityarea_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user:
            serializer = ActivityAreaSerializer(data=request.data,\
                context={'request': request})
            if serializer.is_valid():
                activityarea_obj=ActivityArea()
                activityarea_obj.activity = serializer.validated_data['activity_id']
                activityarea_obj.area = serializer.validated_data['area']
                activityarea_obj.save()
                return Response({"message":"schoolseminar area added successfully"},status=200)
            return Response({'message':serializer.errors}, status=400)
        return Response({"message":"you have to be admin"},status=400)

# class SchoolSeminarList(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = SchoolSeminarSerializer

#     def get(self, request, format=None):
#         schoolseminar_obj = SchoolSeminar.objects.filter(status=True)
#         serializer = SchoolSeminarSerializer(schoolseminar_obj, many=True, \
#             context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         if request.user:
#             serializer = SchoolSeminarSerializer(data=request.data,\
#                 context={'request': request})
#             if serializer.is_valid():
#                 schoolseminar_obj=SchoolSeminar()
#                 schoolseminar_obj.activity = serializer.validated_data['activity_id']
#                 schoolseminar_obj.area = serializer.validated_data['area']
#                 schoolseminar_obj.save()
#                 return Response({"message":"schoolseminar area added successfully"},status=200)
#             return Response({'message':serializer.errors}, status=400)
#         return Response({"message":"you have to be admin"},status=400)




# class CommunityList(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = CommunitySerializer

#     def get(self, request, format=None):
#         community_obj = Community.objects.filter(status=True)
#         serializer = CommunitySerializer(community_obj, many=True, \
#             context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         if request.user:
#             serializer = CommunitySerializer(data=request.data,\
#                 context={'request': request})
#             if serializer.is_valid():
#                 community_obj=Community()
#                 community_obj.activity = serializer.validated_data['activity_id']
#                 community_obj.area = serializer.validated_data['area']
#                 community_obj.save()
#                 return Response({"message":"community area added successfully"},status=200)
#             return Response({'message':serializer.errors}, status=400)
#         return Response({"message":"you have to be admin"},status=400)

# class TrainingList(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = TrainingSerializer

#     def get(self, request, format=None):
#         training_obj = Training.objects.filter(status=True)
#         serializer = TrainingSerializer(training_obj, many=True, \
#             context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         if request.user:
#             serializer = TrainingSerializer(data=request.data,\
#                 context={'request': request})
#             if serializer.is_valid():
#                 training_obj=Training()
#                 training_obj.activity = serializer.validated_data['activity_id']
#                 training_obj.area = serializer.validated_data['area']
#                 training_obj.save()
#                 return Response({"message":"community area added successfully"},status=200)
#             return Response({'message':serializer.errors}, status=400)
#         return Response({"message":"you have to be admin"},status=400)


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