# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from patientapp.models import Patient

pytestmark = pytest.mark.django_db
fake = Faker()

class TestPatientModel():

    def test_init(self):
        patient_obj = mixer.blend(Patient)
        assert patient_obj== Patient.objects.last(), "should create Patient instance"

    def test_full_name(self):
        patient_obj = mixer.blend(Patient)
        assert patient_obj.full_name == '%s %s %s' %(str(patient_obj.first_name),str(patient_obj.middle_name),str(patient_obj.last_name)),\
        'full name is matched'
