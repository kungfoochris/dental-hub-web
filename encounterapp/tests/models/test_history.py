# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from encounterapp.models import Encounter, History
from patientapp.models import Patient

pytestmark = pytest.mark.django_db
fake = Faker()

class TestHistoryModel():

    def test_init(self):
        patient_obj = mixer.blend(Patient)
        encounter_obj = mixer.blend(Encounter,patient=patient_obj)
        history_obj = mixer.blend(History,encounter_id=encounter_obj)
        assert history_obj== History.objects.last(),\
        "should create History Encounter instance"
