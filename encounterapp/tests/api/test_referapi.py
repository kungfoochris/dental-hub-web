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
from addressapp.models import Geography, ActivityArea

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
fake = Faker()


class TestPatientRefer(TestCase):
    def test_list_patientrefer(self):
        client = APIClient()
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        refer_obj = mixer.blend(Refer,encounter_id=encounter_obj)
        # un authorized access by user
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer")
        assert response.status_code == 200, 'patients refer list'

        # content not found
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str('kjfkdkdnn')+"/refer")
        assert response.status_code == 400, 'content not found'


    def test_post_patientrefer(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer", \
            {'id':fake.name(),},format='json')
        assert response.status_code == 200, 'patients refer added'

        # encounter id already exists
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer",\
            {'dentist':True,'id':fake.name()},format='json')
        assert response.status_code == 400, 'encounter_id already exists'



class TestPatientReferUpdate(TestCase):
    def test_list_patientrefer_update(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        refer_obj = mixer.blend(Refer,encounter_id=encounter_obj)
        client = APIClient()

        # un authorized access by user
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer/update")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer/update")
        assert response.status_code == 200, 'patients  update refer list'

        # content not found
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str('sndksn')+"/refer/update")
        assert response.status_code == 400, 'content not found'


        # serializers error
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer/update", \
            {'dentist':'hellopk'},format='json')
        assert response.status_code == 400, 'serializers error'


    def test_update_patienthistory_update(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        refer_obj = mixer.blend(Refer,encounter_id=encounter_obj)
        client = APIClient()

        # un authorized access by user
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer/update")
        assert response.status_code == 401, 'Un authorized access denied.'


        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/refer/update", \
            {'dentist':False},format='json')
        assert response.status_code == 200, 'update patient refer'

        # encounter id does not exists 
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str('fsjbjbj')+"/refer/update", \
            {'dentist':False},format='json')
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

