
# -*- coding:utf-8 -*-
from django.contrib.auth.models import Permission
import pytest
from faker import Faker
from mixer.backend.django  import mixer
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings
from django.test import TestCase

from userapp.models import User
from patientapp.models import Patient
from encounterapp.models import Encounter, History, Refer
from treatmentapp.models import Treatment
from addressapp.models import Geography, ActivityArea

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
fake = Faker()


class TestActivityArea(TestCase):
    def test_list_activityarea(self):
        client = APIClient()
        # un authorized access by user
        response = client.get('/api/v1/activities')
        assert response.status_code == 401, 'Permission not define'


        # un authorized access by user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/activities')
        assert response.status_code == 200, 'list of activities for user'

        # un authorized access by admin
        # user_obj = mixer.blend(User)
        # payload = jwt_payload_handler(user_obj)
        # token = jwt_encode_handler(payload)
        # client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # response = client.get('/api/v1/activities')
        # assert response.status_code == 200, 'list of activities for admin'

    def test_post_activityarea(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/activities')
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/activities', \
            {'name':fake.name(),},format='json')
        assert response.status_code == 400, 'only admin can add'


        # authorized user with admin
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name(),admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/activities',{'name':fake.name(),},format='json')
        assert response.status_code == 200, 'activity added'



        # serializers errors
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name(),admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/activities',{'name':'',},format='json')
        assert response.status_code == 400, 'serializers errors'


class TestActivityAreaUpdate(TestCase):
    def test_listupdate_activityarea(self):
        client = APIClient()
        # un authorized access by user
        activities_obj = mixer.blend(ActivityArea)
        response = client.get('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 401, 'Permission not define'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.get('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 200, 'list of activities for admin'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.get('/api/v1/activities/'+str(12))
        assert response.status_code == 204, 'list of activities for admin'


        # un authorized access by user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.get('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 400, 'list of activities for user'

    def test_update_activityarea(self):
        client = APIClient()

        # un authorized access by user
        activities_obj = mixer.blend(ActivityArea)
        activities_obj = mixer.blend(ActivityArea)
        response = client.put('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 401, 'Permission not define'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.put('/api/v1/activities/'+str(activities_obj.id),\
            {'name':fake.name(),},format='json')
        assert response.status_code == 200, 'activities upate'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.put('/api/v1/activities/'+str(1235),\
            {'name':'',},format='json')
        assert response.status_code == 204, 'content not found'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.put('/api/v1/activities/'+str(activities_obj.id),\
            {'name':'',},format='json')
        assert response.status_code == 400, 'serializers errors'


        #un authorized access by user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.put('/api/v1/activities/'+str(activities_obj.id),\
            {'name':'',},format='json')
        assert response.status_code == 400, 'only admin can access'


    def test_delete_activityarea(self):
        client = APIClient()

        # un authorized access by user
        activities_obj = mixer.blend(ActivityArea)
        response = client.delete('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 401, 'Permission not define'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.delete('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 204, 'data delete'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.delete('/api/v1/activities/'+str(326545))
        assert response.status_code == 204, 'content not found'


        #un authorized access by admin
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        activities_obj = mixer.blend(ActivityArea)
        response = client.delete('/api/v1/activities/'+str(activities_obj.id))
        assert response.status_code == 400, 'only admin can delete'








