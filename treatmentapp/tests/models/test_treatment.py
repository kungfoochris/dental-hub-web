# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from encounterapp.models import Encounter
from treatmentapp.models import Treatment
from patientapp.models import Patient

pytestmark = pytest.mark.django_db
fake = Faker()

class TestTreatmentModel():

    def test_init(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        treatment_obj = mixer.blend(Treatment,encounter_id=encounter_obj)
        assert treatment_obj== Treatment.objects.last(),\
        "should create Treatment Encounter instance"
