# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from encounterapp.models import Encounter
from patientapp.models import Patient

pytestmark = pytest.mark.django_db
fake = Faker()

class TestEncounterModel():

    def test_init(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        assert encounter_obj== Encounter.objects.last(),\
        "should create Patient Encounter instance"
