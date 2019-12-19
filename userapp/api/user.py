import re
import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login as dj_login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User, CustomUser


from userapp.serializers.user import UserSerializer, ForgetPasswordSerializer,\
PasswordResetSerializer, ProfileSerializer, UpdateUserSerializer,\
 PasswordChangeSerializer, CheckUSerializer, UpdateUserDataSerializer,WardSerializer,\
 UserStatusSerializer, AdminPasswordResetSerializer,ProfileSerializer1,UserTokenSerializer
from userapp.emailsend import emailsend
from random import randint
from addressapp.models import Geography

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from rest_framework_jwt.settings import api_settings

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class CustomAuthToken(APIView):
    # permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = UserTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserTokenSerializer(data=request.data,\
        context={'request': request})
        if serializer.is_valid():
            if CustomUser.objects.filter(username=serializer.validated_data['username'],role__name='appuser').exists():
                print("======================================")
                user_obj = User.objects.get(username=serializer.validated_data['username'])
                user = authenticate(username=user_obj.username, password=serializer.validated_data['password'])
                if user is None:
                    return Response({'message':'Invalid username/password.'},status=400)
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                return Response({"token":token},status=200)
            return Response({'message':"username does not exist"},status=400)
        return Response(serializer.errors)

    # def post(self, request, format=None):
    #     serializer = UserTokenSerializer(data=request.data,\
    #         context={'request': request})
    #     if serializer.is_valid():
    #         if User.objects.filter(username=serializer.validated_data['username']).exists():
    #             user_obj = User.objects.get(username=serializer.validated_data['username'])
    #             print("**************************************")
    #             print(user_obj.username)
    #             t = Token.objects.create(user=user_obj)
    #             print("================")
    #             print(t)
    #             return Response(serializer.data)
    #         return Response({"message":"Username do not match"},status=400)





class UserListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = UserSerializer


    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            user=CustomUser.objects.all().exclude(admin=True)
            serializer = UserSerializer(user, many=True, \
                context={'request': request})
            return Response(serializer.data)
            logger.error("Access is denied.")
        return Response({"message":"Access is denied."},status=400)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data,\
            context={'request': request})
        if User.objects.filter(id=request.user.id).exists():
            if CustomUser.objects.filter(username=request.data['username']).count()==0:
                if request.data['password'] == request.data['confirm_password']:
                    if serializer.is_valid():
                        if re.match("^[a-zA-Z]+$", serializer.validated_data['first_name']):
                            if re.match("^[a-zA-Z]+$", serializer.validated_data['last_name']):
                                user_obj = CustomUser()
                                password = serializer.validated_data['password']
                                user_obj.password=password
                                user_obj.username=serializer.validated_data['username']
                                user_obj.first_name=serializer.validated_data['first_name'].capitalize()
                                user_obj.last_name=serializer.validated_data['last_name'].capitalize()
                                user_obj.middle_name = serializer.validated_data['middle_name']
                                user_obj.role = serializer.validated_data['role']
                                user_obj.save()
                                user_obj.location.clear()
                                for i in serializer.validated_data['area']:
                                    user_obj.location.add(i)
                                # text_content = 'Account is successful created'
                                # template_name = "email/activation.html"
                                # emailsend(request.user.id,text_content,template_name,password)
                                return Response({"message":"User added successfully.","full_name":user_obj.full_name,"username":user_obj.username,"active":user_obj.active},status=200)
                            logger.error("Last name should be only combination of string")
                            return Response({"message":"Last name should be only combination of string"},status=400)
                        logger.error("First name should be only combination of string")
                        return Response({"message":"First name should be only combination of string"},status=400)
                    print(serializer.errors)
                    return Response({'message':serializer.errors}, status=400)
                return Response({"message":"password do not match"},status=400)
            logger.error("This email already exists.")
            return Response({'message':'This username already exists.'},status=400)
        logger.error("Access is denied.")
        return Response({"message":"Access is denied."},status=400)


class UserForgetPassword(APIView):
    serializer_class = ForgetPasswordSerializer
    def post(self, request, format=None):
        if User.objects.filter(email=request.data['email']).exists():
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
        if User.objects.filter(id=request.user.id,admin=True):
            user_obj = User.objects.get(id=request.user.id)
            serializers = ProfileSerializer(user_obj, many=False,\
                context={'request': request})
            return Response(serializers.data,status=200)
        else:
            user_obj = CustomUser.objects.get(id=request.user.id)
            serializers = ProfileSerializer1(user_obj, many=False,\
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
                user = authenticate(username=user_obj.username, password=old_password)
                if user:
                    dj_login(request, user)
                    user_obj.password=confirm_password
                    user_obj.save()
                    return Response({'message':'password change successfully'},status=200)
                return Response({'message':'old password do not match'},status=400)
            return Response({'message':'Your new password and confirmation password do not match.'},status=400)
        return Response({'message':serializer.errors}, status=400)

class AdminUserCheckView(APIView):
    serializer_class = CheckUSerializer
    def post(self, request, format=None):
        serializer = CheckUSerializer(data=request.data,\
            context={'request': request})
        if serializer.is_valid():
            if User.objects.filter(email=serializer.validated_data['email'],admin=True).exists():
                adminuser_obj=User.objects.get(email=serializer.validated_data['email'],admin=True)
                return Response({"username":adminuser_obj.username},status=200)
            return Response({"message":"Invalid username/password."},status=400)
        return Response({'message':serializer.errors}, status=400)

class WardCheckView(APIView):
    serializer_class = CheckUSerializer
    def post(self, request, format=None):
        serializer = WardSerializer(data=request.data,\
            context={'request': request})
        if CustomUser.objects.select_related('role').filter(role__name='warduser',username=request.data['username']).exists():
            return Response({"message":'ward user login'},status=200)
        return Response({"message":"Invalid username/password."},status=400)


class UpdateUserDataView(APIView):
    serializer_class = UpdateUserDataSerializer
    permission_classes = (IsPostOrIsAuthenticated,)
    def get(self, request,pk,format=None):
        if User.objects.filter(id=request.user.id,admin=True):
            if CustomUser.objects.filter(id=pk,active=True).exists():
                user = CustomUser.objects.get(id=pk)
                serializer = UpdateUserDataSerializer(user, \
                    context={'request': request})
                return Response(serializer.data,status=200)
            return Response({"message":"content not found"},status=204)
        return Response({"message":"only admin can see"},status=400)

    def put(self, request, pk, format=None):
        if User.objects.filter(id=request.user.id,admin=True):
            user_obj = CustomUser.objects.get(id=pk)
            serializer = UpdateUserDataSerializer(user_obj,\
                data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                if re.match("^[a-zA-Z]+$", serializer.validated_data['first_name']):
                    if re.match("^[a-zA-Z]+$", serializer.validated_data['last_name']):
                        user_obj.first_name = serializer.validated_data['first_name'].capitalize()
                        user_obj.middle_name = serializer.validated_data['middle_name']
                        user_obj.last_name = serializer.validated_data['last_name'].capitalize()
                        user_obj.username = serializer.validated_data['username']
                        user_obj.update_password = False
                        user_obj.save()
                        user_obj.location.clear()
                        for i in serializer.validated_data['area']:
                            print(i)
                            user_obj.location.add(i)
                        return Response({"message":"Update data successful"},status=200)
                    logger.error("Last name should be only combination of string")
                    return Response({"message":"Last name should be only combination of string"},status=400)
                logger.error("First name should be only combination of string")
                return Response({"message":"First name should be only combination of string"},status=400)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"only admin can add"},status=400)

    def delete(self, request, pk, format=None):
        if request.user.admin:
            if CustomUser.objects.filter(id=pk,active=True).exists():
                user_obj = CustomUser.objects.get(id=pk)
                user_obj.active = False
                user_obj.staff = False
                user_obj.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"message":"no content found"},status=204)
        return Response({'errors': 'Permission Denied'},status=400)

class UserStatus(APIView):
    serializer_class = UserStatusSerializer
    def post(self, request, user_id, format=None):
        if request.user.admin:
            if CustomUser.objects.filter(id=user_id):
                serializer = UserStatusSerializer(data=request.data,\
                    context={'request': request})
                customuser_obj = CustomUser.objects.get(id=user_id)
                print(type(request.data['status_obj']))
                if request.data['status_obj'] is False:
                    customuser_obj.active=True
                    customuser_obj.update_password=False
                    customuser_obj.save()
                    print("status true")
                    return Response({"message":"User status update successfully.","data":True},status=200)
                else:
                    customuser_obj.active=False
                    customuser_obj.update_password=False
                    customuser_obj.save()
                    print("status false")
                    return Response({"message":"User status update successfully.","data":False},status=200)
            return Response({"message":"User ID does not exist."},status=400)
        return Response({"message":"only admin can do "},status=400)



class AdminPasswordRest(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = AdminPasswordResetSerializer
    def post(self, request, format=None):
        serializer = AdminPasswordResetSerializer(data=request.data,\
            context={'request': request})
        if request.user.admin:
            if request.data['new_password'] == request.data['confirm_password']:
                if serializer.is_valid():
                    if CustomUser.objects.filter(username = serializer.validated_data['username'],active=True).exists():
                        user_obj = User.objects.get(username = serializer.validated_data['username'])
                        user_obj.password = serializer.validated_data['new_password']
                        user_obj.save()
                        return Response({'message':'Password is successful reset'},status=200)
                    return Response({'message':'Username does not exist or User is in active'},status=400)
                return Response({'message':serializer.errors}, status=400)
            return Response({'message':'Your new password and confirmation password do not match.'},status=400)
        return Response({"message":"only admin can add"},status=400)
