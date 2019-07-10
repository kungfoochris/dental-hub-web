
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


class TestGeography(TestCase):
    def test_list_geography(self):
        client = APIClient()
        # un authorized access by user
        response = client.get('/api/v1/geography')
        assert response.status_code == 200, 'list geography'

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
            'country':fake.name(),'street_address':fake.name()},format='json')
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



