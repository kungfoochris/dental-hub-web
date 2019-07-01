import re
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login as dj_login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User


from userapp.serializers.user import UserSerializer, ForgetPasswordSerializer,\
PasswordResetSerializer, ProfileSerializer, UpdateUserSerializer, PasswordChangeSerializer
from userapp.emailsend import emailsend
from random import randint

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
                    text_content = 'Account is successful created'
                    template_name = "email/activation.html"
                    emailsend(user_obj.id,text_content,template_name,password)
                    return Response({"message":"User create successfully."},status=200)
                return Response({'message':serializer.errors}, status=400)     
            return Response({'message':'This email already exists.'},status=400)
        return Response({"message":"Access is denied."},status=403)


class UserForgetPassword(APIView):
    serializer_class = ForgetPasswordSerializer
    def post(self, request, format=None):
        if User.objects.filter(email=request.data['email']):
            user_obj = User.objects.get(email=request.data['email'])
            text_content = 'Password Reset Email'
            template_name = "email/forgetpassword.html"
            from_email = settings.DEFAULT_FROM_EMAIL
            subject = 'Password Reset'
            recipients = [user_obj.email]
            token = str(randint(000000, 999999))
            user_obj.token = token
            user_obj.update_password = False
            user_obj.save()
            text_content = 'Password Reset Token'
            template_name = "email/forgetpassword.html"
            emailsend(user_obj.id,text_content,template_name,token)
            return Response({'message':'Password Reset Code is send to your mail'},status=200)
        return Response({'message':'Mail cannot be sent as the email address does not exist.'},status=400)

class UserResetPassword(APIView):
    serializer_class = PasswordResetSerializer
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data,\
            context={'request': request})
        if request.data['password'] == request.data['confirm_password']:
            if serializer.is_valid():
                if User.objects.filter(token = serializer.validated_data['token']).exists():
                    user_obj = User.objects.get(token = serializer.validated_data['token'])
                    user_obj.active = True
                    user_obj.password = serializer.validated_data['password']
                    user_obj.token=None
                    user_obj.save()
                    return Response({'message':'Password is successful reset'},status=200)
                return Response({'message':'Token is expired'},status=400) 
            return Response({'message':serializer.errors}, status=400)
        return Response({'message':'Your new password and confirmation password do not match.'},status=400)




class ProfileListView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request,format=None):
        user_obj = User.objects.get(id=request.user.id)
        serializers = ProfileSerializer(user_obj, many=False,\
            context={'request': request})
        return Response(serializers.data,status=200)

class UpdateUserView(APIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request,format=None):
            user = User.objects.get(pk=request.user.id)
            serializer = UpdateUserSerializer(user, \
                context={'request': request})
            return Response(serializer.data,status=200)

    def put(self, request,format=None):
        user_obj = User.objects.get(id = request.user.id)
        serializer = UpdateUserSerializer(user_obj,\
         data=request.data,context={'request': request}, partial=True)
        if serializer.is_valid():
            user_obj = User.objects.get(id = request.user.id)
            user_obj.image = serializer.validated_data['image']
            user_obj.update_password = False
            user_obj.save()
            return Response({"message":"Update successful"},status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangepassword(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    def post(self, request, format=None):
        serializer = PasswordChangeSerializer(data=request.data,\
            context={'request': request})
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']
            if new_password == confirm_password:
                user_obj=User.objects.get(id=request.user.id)
                user = authenticate(email=user_obj.email, password=old_password)
                if user:
                    dj_login(request, user)
                    user_obj.password=confirm_password
                    user_obj.save()
                    return Response({'message':'password change successfully'},status=200)
                return Response({'message':'old password do not match'},status=400)
            return Response({'message':'Your new password and confirmation password do not match.'},status=400)
        return Response({'message':serializer.errors}, status=400)
            
       

