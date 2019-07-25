
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
import re


class TestGeography(TestCase):
    def test_list_geography(self):
        client = APIClient()
        # un authorized access by user
        response = client.get('/api/v1/geography')
        assert response.status_code == 401, 'list geography'

        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/geography')
        assert response.status_code == 200, 'user can access'


        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/geography')
        assert response.status_code == 200, 'admin can access'

    def test_post_geography(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/geography')
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/geography', \
            {'city':fake.name(),'state':fake.name(),\
            'country':fake.name(),'street_address':fake.name()},format='json')
        assert response.status_code == 400, 'only admin can add'


        # authorized user with admin
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name(),admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/geography', \
            {'city':fake.name(),'state':fake.name(),\
            'country':fake.name(),'street_address':"ktm"},format='json')
        assert response.status_code == 200, 'geography added'



        # serializers errors
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name(),admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/geography', \
            {'city':fake.name(),'state':'',\
            'country':fake.name(),'street_address':fake.name()},format='json')
        assert response.status_code == 400, 'serializers errors'


        # location already added
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Geography.objects.create(city="ktm",state="ktm",street_address="ktm",country="nepal")
        response = client.post('/api/v1/geography', \
            {'city':"ktm",'state':"ktm",\
            'country':"Nepal",'street_address':"ktm"},format='json')
        assert response.status_code == 400, 'location already exists'


        # authorized user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/geography', \
            {'city':fake.name(),'street_address':fake.name(),\
            'state':fake.name(),'country':"Nepal"},format='json')
        assert response.status_code == 400, 'street_address should contain only string'


class TestGeographyUpdate(TestCase):
    def test_listupdate_geography(self):
        client = APIClient()
        # un authorized access by user
        response = client.get('/api/v1/geography')
        assert response.status_code == 401, 'list geography'

        #authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.get('/api/v1/geography/'+str(geography_obj.id))
        assert response.status_code == 200, 'admin can access'



        #authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.get('/api/v1/geography/'+str(23656544654))
        assert response.status_code == 204, 'content not found'

        #authorized access by admin
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.get('/api/v1/geography/'+str(geography_obj.id))
        assert response.status_code == 400, 'only admin can access'



    def test_post_geography(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.put('/api/v1/geography')
        assert response.status_code == 401, 'Un authorized access denied.'

        # unauthorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.put('/api/v1/geography/'+str(geography_obj.id), \
            {'city':fake.name(),'state':fake.name(),\
            'country':fake.name(),'street_address':fake.name()},format='json')
        assert response.status_code == 400, 'only admin can add'


        # location already added
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj=Geography.objects.create(city="ktm",state="ktm",street_address="ktm",country="nepal")
        response = client.put('/api/v1/geography/'+str(geography_obj.id), \
            {'city':"ktm",'state':"ktm",\
            'country':"Nepal",'street_address':"ktm"},format='json')
        assert response.status_code == 400, 'location already exists'


        # authorized user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.put('/api/v1/geography/'+str(geography_obj.id), \
            {'city':fake.name(),'street_address':"ktm",\
            'state':fake.name(),'country':"Nepal"},format='json')
        assert response.status_code == 200, 'only admin can edit'


        # authorized user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.put('/api/v1/geography/'+str(geography_obj.id), \
            {'city':fake.name(),'street_address':fake.name(),\
            'state':fake.name(),'country':"Nepal"},format='json')
        assert response.status_code == 400, 'street_address should contain only string'


        # authorized user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.put('/api/v1/geography/'+str(geography_obj.id), \
            {'city':fake.name(),'street_address':fake.name(),\
            'state':fake.name(),'country':''},format='json')
        assert response.status_code == 400, 'serializers errors'


        # authorized user
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.put('/api/v1/geography/'+str(1165465456), \
            {'city':fake.name(),'street_address':fake.name(),\
            'state':fake.name(),'country':'Nepal'},format='json')
        assert response.status_code == 204, 'content not found'


    def test_delete_geography(self):
        client = APIClient()

        # un authorized access by user
        geography_obj = mixer.blend(Geography)
        response = client.delete('/api/v1/geography/'+str(geography_obj.id))
        assert response.status_code == 401, 'Permission not define'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.delete('/api/v1/geography/'+str(geography_obj.id))
        assert response.status_code == 204, 'data delete'


        #un authorized access by admin
        user_obj = mixer.blend(User,admin=True)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.delete('/api/v1/geography/'+str(326545))
        assert response.status_code == 204, 'content not found'


        #un authorized access by admin
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        geography_obj = mixer.blend(Geography)
        response = client.delete('/api/v1/geography/'+str(geography_obj.id))
        assert response.status_code == 400, 'only admin can delete'





