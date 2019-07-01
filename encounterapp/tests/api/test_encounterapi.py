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
from encounterapp.models import Encounter

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
fake = Faker()


class TestPatientEncounter(TestCase):
    def test_list_patientencounter(self):
        client = APIClient()
        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.get('/api/v1/patients/'+str(patient_obj.id)+"/encounter")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.get('/api/v1/patients/'+str(patient_obj.id)+"/encounter")
        assert response.status_code == 200, 'patientsencounter list'

    def test_post_patientencounter(self):
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.id)+"/encounter")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.id)+"/encounter", {'encounter_type':'check'},format='json')
        assert response.status_code == 200, 'patients created'


        # serializers error
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.id)+"/encounter", {'encounter_type':''},format='json')
        assert response.status_code == 400, 'serializers error'

        # patient exists or not
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str('knbfkb211654')+"/encounter", {'encounter_type':''},format='json')
        assert response.status_code == 400, 'patient does not exists'


class TestPatientEncounterUpdate(TestCase):
    def test_list_patientencounter_update(self):
        client = APIClient()
        # un authorized access by user
        # patient_obj = mixer.blend(Patient)
        # if Encounter.objects.select_related('patient').filter(patient=patient_obj).exists():
        #     response = client.get('/api/v1/patients/'+str(patient_obj.id)+"/encounter")
        #     assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.get('/api/v1/patients/'+str(patient_obj.id)+"/encounter")
        assert response.status_code == 200, 'patientsencounter list'

