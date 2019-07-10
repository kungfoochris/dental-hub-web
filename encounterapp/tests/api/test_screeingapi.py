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
from encounterapp.models import Encounter, History, Screeing
from addressapp.models import Geography, ActivityArea

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
fake = Faker()


class TestPatientScreeing(TestCase):
    def test_list_patientscreeing(self):
        client = APIClient()
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        screeing_obj = mixer.blend(Screeing,encounter_id=encounter_obj)
        # un authorized access by user
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing")
        assert response.status_code == 200, 'patients screeing list'

        # content not found
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str('kjfkdkdnn')+"/screeing")
        assert response.status_code == 400, 'content not found'


    def test_post_patientscreeing(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing", \
            {'caries_risk':'low','primary_teeth':1,'permanent_teeth':2,'id':fake.name()},format='json')
        assert response.status_code == 200, 'patients screeing added'

        # encounter id already exists
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        screeing_obj = mixer.blend(Screeing,encounter_id=encounter_obj)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing",\
            {'primary_teeth':1,'permanent_teeth':2,'id':fake.name()},format='json')
        assert response.status_code == 400, 'encounter_id already exists'

        # encounter id  doesnot exists
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        screeing_obj = mixer.blend(Screeing,encounter_id=encounter_obj)
        response = client.post('/api/v1/encounter/'+str('jfsjbnjnj')+"/screeing",\
            {'primary_teeth':1,'permanent_teeth':2,'id':fake.name()},format='json')
        assert response.status_code == 400, 'encounter_id doesnot exists'




class TestPatientScreeingUpdate(TestCase):
    def test_list_patientscreeing_update(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        screeing_obj = mixer.blend(Screeing,encounter_id=encounter_obj)
        client = APIClient()

        # un authorized access by user
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing/update")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing/update")
        assert response.status_code == 200, 'patientshistory list'

        # content not found
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str('sndksn')+"/screeing/update")
        assert response.status_code == 400, 'content not found'


    def test_update_patientscreeing_update(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        screeing_obj = mixer.blend(Screeing,encounter_id=encounter_obj)
        client = APIClient()

        # un authorized access by user
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing/update")
        assert response.status_code == 401, 'Un authorized access denied.'


        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/screeing/update", \
            {'primary_teeth':2},format='json')
        assert response.status_code == 200, 'update patient screeing'

        # encounter id does not exists 
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str('fsjbjbj')+"/screeing/update", \
            {'primary_teeth':3},format='json')
        assert response.status_code == 400, 'encounter_id doesnot exists'

#         # serializers error
#         user_obj = User.objects.create(email=fake.email(),\
#             first_name=fake.name(),last_name=fake.name())
#         payload = jwt_payload_handler(user_obj)
#         token = jwt_encode_handler(payload)
#         client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
#         response = client.put('/api/v1/encounter/'+str('fsjbjbj')+"/history/update", \
#             {'bleeding':'hellopk'},format='json')
#         assert response.status_code == 400, 'serializers error'

