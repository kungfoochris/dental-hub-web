# import re
# import uuid
# from django.conf import settings
# from django.contrib.auth import authenticate, login as dj_login
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions

# from userapp.models import User, AppUser
# from userapp.serializers.appuser import AppUserSerializer

# from addressapp.models import Geography

# import logging
# # Get an instance of a logger
# logger = logging.getLogger(__name__)

# class IsPostOrIsAuthenticated(permissions.BasePermission):        

#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             return True
#         return request.user and request.user.is_authenticated


# class AppUserListView(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = AppUserSerializer

#     def get(self, request, format=None):
#         if request.user.admin:
#             user=AppUser.objects.filter(active=True)
#             serializer = AppUserSerializer(user, many=True, \
#                 context={'request': request})
#             return Response(serializer.data)
#         logger.error("Access is denied.")
#         return Response({"message":"Access is denied."},status=400)

#     def post(self, request, format=None):
#         serializer = AppUserSerializer(data=request.data,\
#             context={'request': request})
#         if AppUser.objects.filter(username=request.data['username']).exists():
#             appuser=AppUser.objects.get(username=request.data['username'])
#             user = authenticate(email=appuser.username, password=request.data['password'])
#             if user:
#                 dj_login(request, user)
#                 return Response({"message":"Login successfull"},status=200)
#             logger.error("password do not match")
#             return Response({"message":"password do not match"},status=400)
#         logger.error("username does not exists.")
#         return Response({'message':'username does not exists.'},status=400)
#         # logger.error("Access is denied.")
#         # return Response({"message":"Access is denied."},status=400)