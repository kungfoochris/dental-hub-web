
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


class TestPatientTreatment(TestCase):
    def test_list_patientstreatment(self):
        client = APIClient()
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        # un authorized access by user
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment")
        assert response.status_code == 200, 'patients treatment list'

        # content not found
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str('kjfkdkdnn')+"/treatment")
        assert response.status_code == 400, 'content not found'


    def test_post_patienttreatment(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment", \
            {'id':fake.name(),},format='json')
        assert response.status_code == 200, 'patients treatment added'

        # encounter id already exists
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        response = client.post('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment",\
            {'fluoride_varnish':True,'id':fake.name()},format='json')
        assert response.status_code == 400, 'encounter_id already exists'

        # encounter id doesnot exists
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        response = client.post('/api/v1/encounter/'+str('jjdbj')+"/treatment",\
            {'id':fake.name()},format='json')
        assert response.status_code == 400, 'encounter id doesnot exists'


        # serializers errors
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        response = client.post('/api/v1/encounter/'+str('jjdbj')+"/treatment",\
            {'fluoride_varnish':'','id':fake.name()},format='json')
        assert response.status_code == 400, 'serializers errors'



class TestPatientTreatmentUpdate(TestCase):
    def test_list_patientstreatment_update(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        client = APIClient()

        # un authorized access by user
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment/update")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment/update")
        assert response.status_code == 200, 'patients  update treatment list'

        # content not found
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get('/api/v1/encounter/'+str('sndksn')+"/treatment/update")
        assert response.status_code == 400, 'content not found'



    def test_update_patientstreatment_update(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        client = APIClient()

        # un authorized access by user
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment/update")
        assert response.status_code == 401, 'Un authorized access denied.'


        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str(encounter_obj.uid)+"/treatment/update", \
            {'fluoride_varnish':False},format='json')
        assert response.status_code == 200, 'update patient treatment'

        # encounter id does not exists 
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str('fsjbjbj')+"/treatment/update", \
            {'fluoride_varnish':False},format='json')
        assert response.status_code == 400, 'encounter_id doesnot exists'

        # serializers error
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/encounter/'+str('fsjbjbj')+"/treatment/update", \
            {'fluoride_varnish':'hellopk'},format='json')
        assert response.status_code == 400, 'serializers error'

