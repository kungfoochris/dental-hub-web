# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from encounterapp.models import Encounter, Refer
from patientapp.models import Patient

pytestmark = pytest.mark.django_db
fake = Faker()

class TestReferModel():

    def test_init(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        refer_obj = mixer.blend(Refer,encounter_id=encounter_obj)
        assert refer_obj== Refer.objects.last(),\
        "should create Refer Encounter instance"
