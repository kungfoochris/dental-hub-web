# -*- coding:utf-8 -*-
from django.contrib.auth.models import Permission
import pytest
from faker import Faker
from mixer.backend.django  import mixer
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from userapp.models import User
from addressapp.models import Geography

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
fake = Faker()


class TestUserListView(TestCase):
    '''
    for UserListView http://localhost/api/v1/users
    '''
    def test_list_users(self):
        client = APIClient()
        # un authorized access by user
        response = client.get('/api/v1/users')
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user but not admin
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/users', format='json')
        assert response.status_code == 400, 'only admin can access'

        # authorized user with admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/users', format='json')
        assert response.status_code == 200, 'list user'


    def test_register_users(self):
        client = APIClient()

        response = client.post('/api/v1/users',\
            {'first_name':fake.name(),'last_name':fake.name(),\
            'email':fake.email(),'middle_name':fake.name()},format='json')
        assert response.status_code == 401,'only admin can register'


        # authorized user but not admin
        user_obj = mixer.blend(User,admin=False)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/users',\
            {'first_name':fake.name(),'last_name':fake.name(),\
            'email':fake.email(),'middle_name':fake.name()},format='json')
        assert response.status_code == 400,'only admin can register'

        # authorized user with  admin
        user_obj = mixer.blend(User,admin=True)
        location_obj = mixer.blend(Geography)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/users',\
            {'first_name':"pk",'last_name':"karki",\
            'email':fake.email(),'location':[str(location_obj.id)],'middle_name':"hello"},format='json')
        assert response.status_code == 200,'user created successfully'


        # for serializer invalid
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/users',\
            {'first_name':fake.name(),'last_name':fake.name(),\
            'email':'','middle_name':fake.name()},format='json')
        assert response.status_code == 400,'Serializer invalid'

        # for serializer invalid
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/users',\
            {'first_name':'','last_name':fake.name(),\
            'email':fake.email(),'middle_name':fake.name()},format='json')
        assert response.status_code == 400,'Serializer invalid'

        # for email validation of already exist
        user_obj = mixer.blend(User,admin=True)
        email=fake.email()
        user_obj1 = mixer.blend(User,email=email)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/users',\
            {'first_name':'','last_name':fake.name(),\
            'email':email,'middle_name':fake.name()},format='json')
        assert response.status_code == 400,'Email already exist'

        
#         # for empty name
#         response = client.post('/api/v1/users', {'first_name': '',\
#              'last_name': '','email':fake.email(), 'password':pa,\
#                   'confirm_password':pa,'middle_name': ''}, format='json')
#         assert response.status_code == 400, 'name not provided'        

#         # for empty first name
#         response = client.post('/api/v1/users', {'first_name': '',\
#              'last_name': fake.name(),'email':fake.email(), 'password':pa,\
#                   'confirm_password':pa,'middle_name': fake.name()}, format='json')
#         assert response.status_code == 400, 'empty first name'

#         # for empty email 
#         response = client.post('/api/v1/users', {'first_name': '',\
#              'last_name': fake.name(),'email': '', 'password':pa,\
#                   'confirm_password':pa,'middle_name': fake.name()}, format='json')
#         assert response.status_code == 400, 'empty email name'


#     '''
#     for UpdateUserView path('profile/<int:pk>',UpdateUserView.as_view())
#     '''
#     def test_update_user_view(self):
#         mixer.blend(AmejRate, buy=2, sell=2, name='amej')
#         test_user = mixer.blend(User)
#         client = APIClient()

#         # for get method unauthenticated user
#         response = client.get('/api/v1/profile/update', format='json')
#         assert response.status_code == 401, 'un authenticated user.'

#         # # for get method authenticated user
#         payload = jwt_payload_handler(test_user)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

#         response = client.get('/api/v1/profile/update', \
#             format='json')
#         assert response.status_code == 200, 'authenticated for viewing user profile update.'

#         # to creating a bank
#         newPhoto = SimpleUploadedFile(name='new.JPG', \
#             content=open(MEDIA_ROOT+'/image/new.JPG', 'rb').read(), \
#                 content_type='image/jpeg')

#         # for put method i.e. update profile success without photo and phone
#         # ToDo is phone is verified then should it be removed.
#         response = client.put('/api/v1/profile/update', \
#             {'first_name' : fake.name(), 'last_name' : fake.name(), \
#                 'phone' : '', 'image' : ''}, format='json')
#         assert response.status_code == 200, 'Update profile success.'

#         # for put method i.e. update profile success without photo and string
#         # ToDo text/string is been accepted
#         response = client.put('/api/v1/profile/update', \
#             {'first_name' : fake.name(), 'last_name' : fake.name(), \
#                 'phone' : 'testphone', 'image' : ''}, format='json')
#         assert response.status_code == 200, 'Update profile success.'
        
#         # phone more than 17 digit
#         # ToDo phone number is 20 digits and it is taken
#         response = client.put('/api/v1/profile/update', \
#             {'first_name' : fake.name(), 'last_name' : fake.name(), \
#                 'phone' : 12345678901234567890, 'image' : ''}, format='json')
#         assert response.status_code == 200, 'Update profile success.'

#         # update profile success with new photo
#         response = client.put('/api/v1/profile/update', \
#             {'first_name' : fake.name(), 'last_name' : fake.name(), \
#                 'phone' : fake.msisdn(), 'image' : newPhoto})
#         assert response.status_code == 200, 'Update profile success.'
        
#         # update profile success with new photo but no last name
#         response = client.put('/api/v1/profile/update', \
#             {'first_name' : fake.name(), 'last_name' : '', \
#                 'phone' : fake.msisdn(), 'image' : newPhoto})
#         assert response.status_code == 400, 'last name is empty.'
        
#         # update profile success with new photo but no first name
#         response = client.put('/api/v1/profile/update', \
#             {'first_name' : '', 'last_name' : fake.name(), \
#                 'phone' : fake.msisdn(), 'image' : newPhoto})
#         assert response.status_code == 400, 'first name is empty.'

#         # for update profile with wrong email
#         # ToDo invalid email is taking
#         # response = client.put('/api/v1/profile/update', \
#         #     {'first_name' : fake.name(), 'last_name' : fake.name(), \
#         #         'image' : ''}, format='json')
#         # assert response.status_code == 400, 'Invalid email.'


#     '''
#     for User Account Activation path('users/activate',UserAccountActivate.as_view())
#     '''
#     def test_UserAccount_Activate(self):
#         mixer.blend(AmejRate, buy=2, sell=2, name='amej')
#         activate_user = mixer.blend(User, token='thisisatoken4334')
#         client = APIClient()

#         # token first use
#         response = client.post('/api/v1/users/activate', \
#             {'token' : activate_user.token}, format='json')
#         assert response.status_code == 200, 'User activated successfully.'

#         # token re-use
#         response = client.post('/api/v1/users/activate', \
#             {'token' : activate_user.token}, format='json')
#         assert response.status_code == 401, 'Token has expired.'

# class TestPasswordManage(TestCase):
#     '''
#     for UserForgetPassword
#     '''
#     def test_forget_password(self):
#         client = APIClient()
#         fake_email = fake.email()
#         user_obj = mixer.blend(User, email=fake_email)
#         # for correct registered email
#         response = client.post('/api/v1/users/forgetpassword',\
#             {'email' : fake_email}, format='json')
#         assert response.status_code == 200, 'password reset successfully'

#         # for not registered email
#         response = client.post('/api/v1/users/forgetpassword',\
#             {'email' : fake.email()}, format='json')
#         assert response.status_code == 400, 'email not registered.'


#     '''
#     for UserResetPassword Test case for Reset Password
#     '''    
#     def test_reset_password(self):
#         fake_password = fake.name()
#         client = APIClient()


#         # reset password without token
#         response = client.post('/api/v1/users/resetpassword',\
#             {'token' : "3398", 'password' : fake_password,\
#                 'confirm_password' : fake_password}, format='json')
#         assert response.status_code == 400, 'token do not match'

#         # reset password with different password and confirm_passowrd
#         user_obj = mixer.blend(User,token="1234")
#         response = client.post('/api/v1/users/resetpassword',\
#             {'token' :str(1234), 'password' : fake_password,\
#                 'confirm_password' : fake.name()}, format='json')
#         assert response.status_code == 400, 'password do not'

#         # reset password success
#         user_obj = mixer.blend(User,token="2565")
#         response = client.post('/api/v1/users/resetpassword',\
#             {'token' :str(2565), 'password' : fake_password,\
#                 'confirm_password' :fake_password}, format='json')
#         assert response.status_code == 200, 'password reset success'

#         # serializer error 
#         user_obj = mixer.blend(User,token="2565")
#         response = client.post('/api/v1/users/resetpassword',\
#             {'token' :'', 'password' : fake_password,\
#                 'confirm_password' :fake_password}, format='json')
#         assert response.status_code == 400, 'serializer error'

#         user_obj = mixer.blend(User,token="2565")
#         response = client.post('/api/v1/users/resetpassword',\
#             {'token' :'2565', 'password' : fake_password,\
#                 'confirm_password' :''}, format='json')
#         assert response.status_code == 400, 'serializer error'

#         user_obj = mixer.blend(User,token="2565")
#         response = client.post('/api/v1/users/resetpassword',\
#             {'token' :'2565', 'password' : '',\
#                 'confirm_password' :fake_password}, format='json')
#         assert response.status_code == 400, 'serializer error'




# class TestProfile(TestCase):
#     def test_profile(self):
#         client = APIClient()
#         # without authenticated user
#         response = client.get('/api/v1/profile', format='json')
#         assert response.status_code == 401, 'Unauthenticated user.'

#         # by using authenticated user
#         user_obj = mixer.blend(User)
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.get('/api/v1/profile',format='json')
#         assert response.status_code == 200, 'profile update.'


# class ProfileUpdate(TestCase):
#     def test_getupdateprofile(self):
#         client = APIClient()
#         # without authenticated user
#         response = client.get('/api/v1/profile/update', format='json')
#         assert response.status_code == 401, 'Unauthenticated user.'

#         # by using authenticated user
#         user_obj = User.objects.create(email=fake.email(),first_name=fake.name(),last_name=fake.name())
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.get('/api/v1/profile/update', format='json')
#         assert response.status_code == 200, 'show profile of  user.'

#     def test_updateprofile(self):
#         client = APIClient()
#         newPhoto = SimpleUploadedFile(name='default-avatar.png',\
#             content=open(MEDIA_ROOT+'/profile/default-avatar.png', 'rb').read(),\
#             content_type='image/png')
#         # without authenticated user
#         response = client.put('/api/v1/profile/update', {'image':newPhoto},format='json')
#         assert response.status_code == 401, 'Unauthenticated user.'

#         # by using authenticated user
#         user_obj = User.objects.create(email=fake.email(),first_name=fake.name(),last_name=fake.name())
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.put('/api/v1/profile/update', {'image':newPhoto},format='json')
#         assert response.status_code == 200, 'show profile of  user.'


# class ChangePassword(TestCase):

#     '''
#     for UserChangepassword http://localhost/api/v1/users/changepassword
#     '''
#     def test_change_passwrod_post(self):
#         client = APIClient()
#         old_password = fake.password()
#         fake_password = fake.password()

#         # unauthenticated user
#         response = client.post('/api/v1/users/changepassword', \
#             {'old_password' : fake.password(), 'new_password' : fake_password, \
#                 'confirm_password' : fake_password}, format='json')
#         assert response.status_code == 400, 'old password is wrong'



#         # authenticated user
#         user_obj = mixer.blend(User,password='iam100good')
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.post('/api/v1/users/changepassword', \
#             {'old_password' : user_obj.password, 'new_password' : fake_password, \
#                 'confirm_password' : fake_password}, format='json')
#         assert response.status_code == 200, 'password change successfully'


#         # password donot match
#         user_obj = mixer.blend(User,password='iam100good')
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.post('/api/v1/users/changepassword', \
#             {'old_password' : user_obj.password, 'new_password' : fake_password, \
#                 'confirm_password' : fake.password()}, format='json')
#         assert response.status_code == 400, 'password donot match'


#         # password donot match
#         user_obj = mixer.blend(User,password='iam100good')
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.post('/api/v1/users/changepassword', \
#             {'old_password' : "12345jdhsd", 'new_password' : "iam100bad", \
#                 'confirm_password' : "iam100bad"}, format='json')
#         assert response.status_code == 400, 'old password donot match'

#         # serializer donot match
#         user_obj = mixer.blend(User,password='iam100good')
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.post('/api/v1/users/changepassword', \
#             {'new_password' : "iam100bad", \
#                 'confirm_password' : "iam100bad"}, format='json')
#         assert response.status_code == 400, 'serializer error'



class AdminUserCheckView(TestCase):
    def test_checkuser(self):
        client = APIClient()
        email = fake.email()

        # authenticated user
        user_obj = mixer.blend(User,email=fake.email(),admin=True)
        response = client.post('/api/v1/checkuser', \
            {'email' : user_obj.email}, format='json')
        assert response.status_code == 200, 'status is true'


        # authenticated user
        user_obj = mixer.blend(User,email=fake.email())
        response = client.post('/api/v1/checkuser', \
            {'email' : user_obj.email}, format='json')
        assert response.status_code == 400, 'invalid user'

        # seriaizer error
        user_obj = mixer.blend(User,email=email,admin=True)
        response = client.post('/api/v1/checkuser', \
            {'email' : fake.name()}, format='json')
        assert response.status_code == 400, 'seriaizer error'


        # unauthenticated user
        response = client.post('/api/v1/checkuser', \
            {'email' : fake.email()}, format='json')
        assert response.status_code == 400, 'invalid user'


class UpdateUserData(TestCase):
    def test_listupdateuserdata(self):
        client = APIClient()

        # unauthenticated user
        user_obj = mixer.blend(User)
        response = client.get('/api/v1/users/'+str(user_obj.id))
        assert response.status_code == 401, 'unauthenticated user'

        # authenticated user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.get('/api/v1/users/'+str(user_obj1.id))
        assert response.status_code == 400, 'only admin can access'


        # authenticated user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.get('/api/v1/users/'+str(user_obj1.id))
        assert response.status_code == 200, 'admin can access'


        # authenticated user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.get('/api/v1/users/'+str(123164654654))
        assert response.status_code == 204, 'content not found'


    def test_updateuserdata(self):
        client = APIClient()

        # unauthenticated user
        user_obj = mixer.blend(User)
        response = client.put('/api/v1/users/'+str(user_obj.id),\
            {'email' : fake.email()}, format='json')
        assert response.status_code == 401, 'unauthenticated user'


        # authenticated user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.put('/api/v1/users/'+str(user_obj1.id),\
            {'email' : fake.email()}, format='json')
        assert response.status_code == 400, 'only admin can update'


        # authenticated user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        location_obj = mixer.blend(Geography)
        user_obj1 = mixer.blend(User)
        response = client.put('/api/v1/users/'+str(user_obj1.id),\
            {'email' : fake.email(),'first_name':'pk','last_name':'pk',\
            'middle_name':fake.name(),'location':[str(location_obj.id)]}, format='json')
        assert response.status_code == 200, 'admin can access'


        # authenticated user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        location_obj = mixer.blend(Geography)
        user_obj1 = mixer.blend(User)
        response = client.put('/api/v1/users/'+str(user_obj1.id),\
            {'email' : fake.email(),'first_name':fake.name(),'last_name':'pk',\
            'middle_name':fake.name(),'location':[str(location_obj.id)]}, format='json')
        assert response.status_code == 400, 'first_name should contain string only'


        # authenticated user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        location_obj = mixer.blend(Geography)
        user_obj1 = mixer.blend(User)
        response = client.put('/api/v1/users/'+str(user_obj1.id),\
            {'email' : fake.email(),'first_name':'pk','last_name':fake.name(),\
            'middle_name':fake.name(),'location':[str(location_obj.id)]}, format='json')
        assert response.status_code == 400, 'last_name should contain string only'



         # authenticated user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        location_obj = mixer.blend(Geography)
        user_obj1 = mixer.blend(User)
        response = client.put('/api/v1/users/'+str(user_obj1.id),\
            {'email' : fake.name(),'first_name':'pk','last_name':'pk',\
            'middle_name':fake.name(),'location':[str(location_obj.id)]}, format='json')
        assert response.status_code == 400, 'serializer error'


    def test_delete_user(self):
        client = APIClient()

        # un authorized access by user
        user_obj = mixer.blend(User)
        response = client.delete('/api/v1/users/'+str(user_obj.id))
        assert response.status_code == 401, 'Permission not define'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.delete('/api/v1/users/'+str(user_obj1.id))
        assert response.status_code == 204, 'data delete'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.delete('/api/v1/users/'+str(326545))
        assert response.status_code == 204, 'content not found'


        #un authorized access by admin
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        user_obj1 = mixer.blend(User)
        response = client.delete('/api/v1/users/'+str(user_obj1.id))
        assert response.status_code == 400, 'only admin can delete'