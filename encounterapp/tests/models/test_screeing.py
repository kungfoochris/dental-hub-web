# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from encounterapp.models import Encounter, Screeing
from patientapp.models import Patient

pytestmark = pytest.mark.django_db
fake = Faker()

class TestScreeingModel():

    def test_init(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        screeing_obj = mixer.blend(Screeing,encounter_id=encounter_obj)
        assert screeing_obj== Screeing.objects.last(),\
        "should create Screeing Encounter instance"
