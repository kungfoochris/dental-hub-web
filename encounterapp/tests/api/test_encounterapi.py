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
from addressapp.models import Geography, ActivityArea

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
fake = Faker()


class TestPatientEncounter(TestCase):
    def test_list_patientencounter(self):
        client = APIClient()
        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.get('/api/v1/patients/'+str(patient_obj.uid)+"/encounter")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.get('/api/v1/patients/'+str(patient_obj.uid)+"/encounter")
        assert response.status_code == 200, 'patientsencounter list'

    def test_post_patientencounter(self):
        activityarea_obj = mixer.blend(ActivityArea)
        geography_obj = mixer.blend(Geography)
        client = APIClient()

        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.uid)+"/encounter")
        assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.uid)+"/encounter", \
            {'encounter_type':'check','activityarea_id':str(activityarea_obj.id),\
            'geography_id':str(geography_obj.id),'id':fake.name()},format='json')
        assert response.status_code == 200, 'patients created'


        # serializers error
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.uid)+"/encounter", \
            {'encounter_type':'','activityarea_id':str(activityarea_obj.id),\
            'geography_id':str(geography_obj.id),'id':fake.name()},format='json')
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

        # activity id doesnot exists
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.uid)+"/encounter", \
            {'encounter_type':'check','activityarea_id':120,\
            'geography_id':str(geography_obj.id),'id':fake.name()},format='json')
        assert response.status_code == 400, 'activity id does not exists'


        # geography id doesnot exists
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        response = client.post('/api/v1/patients/'+str(patient_obj.uid)+"/encounter", \
            {'encounter_type':'check','activityarea_id':120,\
            'geography_id':123,'id':fake.name()},format='json')
        assert response.status_code == 400, 'geography id does not exists'


class TestPatientEncounterUpdate(TestCase):
    def test_list_patientencounter_update(self):
        client = APIClient()
        # un authorized access by user
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        if Encounter.objects.select_related('patient').filter(patient=patient_obj).exists():
            response = client.get('/api/v1/patients/'+str(patient_obj.id)+"/encounter/"+str(encounter_obj.uid))
            assert response.status_code == 401, 'Un authorized access denied.'

        # authorized user
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        response = client.get('/api/v1/patients/'+str(patient_obj.uid)+"/encounter/"+str(encounter_obj.uid))
        assert response.status_code == 200, 'patientsencounter list'


        # encounter id does not existss
        user_obj = mixer.blend(User)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        response = client.get('/api/v1/patients/'+str('kjfbkjb')+"/encounter/"+str(encounter_obj.uid))
        assert response.status_code == 400, 'encounter id does not exists'

    def test_update_patientencounter_update(self):
        activityarea_obj = mixer.blend(ActivityArea)
        geography_obj = mixer.blend(Geography)
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        client = APIClient()

        # un authorized access by user
        response = client.put('/api/v1/patients/'+str(patient_obj.uid)+"/encounter/"+str(encounter_obj.uid))
        assert response.status_code == 401, 'Un authorized access denied.'


        # authorized user
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/patients/'+str(patient_obj.uid)+"/encounter/"+str(encounter_obj.uid), \
            {'encounter_type':'pain'},format='json')
        assert response.status_code == 200, 'update patient encounter'

        # serializers error
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/patients/'+str(patient_obj.uid)+"/encounter/"+str(encounter_obj.uid), \
            {'encounter_type':'pk'},format='json')
        assert response.status_code == 400, 'serializers error'


        # serializers error
        user_obj = User.objects.create(email=fake.email(),\
            first_name=fake.name(),last_name=fake.name())
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.put('/api/v1/patients/'+str('fsnfbfbb')+"/encounter/"+str(encounter_obj.uid), \
            {'encounter_type':'pain'},format='json')
        assert response.status_code == 400, 'serializers error'
