import re
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login as dj_login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User


from userapp.serializers.user import UserSerializer
from userapp.emailsend import emailsend

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class UserListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        if request.user.admin:
            user=User.objects.all().exclude(admin=True)
            serializer = UserSerializer(user, many=True, \
                context={'request': request})
            return Response(serializer.data)
        return Response({"message":"Access is denied."},status=403)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data,\
            context={'request': request})
        if request.user.admin:
            if User.objects.filter(email=request.data['email']).count()==0:
                if serializer.is_valid():
                    password = uuid.uuid4().hex[:8].upper()
                    user_obj = User()
                    user_obj.password=password
                    user_obj.email=serializer.validated_data['email']
                    user_obj.first_name=serializer.validated_data['first_name']
                    user_obj.last_name=serializer.validated_data['last_name']
                    user_obj.middle_name = serializer.validated_data['middle_name']
                    user_obj.save()
                    emailsend(user_obj.id,password)
                    return Response({"message":"User create successfully."},status=200)
                return Response({'message':serializer.errors}, status=400)     
            return Response({'message':'This email already exists.'},status=400)
        return Response({"message":"Access is denied."},status=403)