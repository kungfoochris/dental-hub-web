from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter
from userapp.models import User
import datetime


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class History(models.Model):
    id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    blood_disorder = models.BooleanField(_('bleeding problem'),default=False)
    diabetes = models.BooleanField(default=False)
    liver_problem = models.BooleanField(_('liver problem'),default=False)
    rheumatic_fever = models.BooleanField(_('rheumatic fever'),default=False)
    seizuers_or_epilepsy = models.BooleanField(_('epilepsy or seizures'),default=False)
    hepatitis_b_or_c = models.BooleanField(_('hepatitis b or c'),default=False)
    hiv = models.BooleanField(default=False)
    no_allergies = models.BooleanField(default=False)
    allergies = models.CharField(default="",max_length=255)
    other = models.CharField(max_length=255,default="")
    no_underlying_medical_condition = models.BooleanField(_('no underlying medical condition'),default=False,)
    not_taking_any_medications = models.BooleanField(_('not taking any medications'),default=False,)
    medications = models.CharField(max_length=255,default="")
    no_medications = models.BooleanField(default=False)
    encounter_id = models.OneToOneField(Encounter,on_delete=models.CASCADE,related_name='history')
    high_blood_pressure = models.BooleanField(default=False)
    low_blood_pressure = models.BooleanField(default=False)
    thyroid_disorder = models.BooleanField(default=False)
	# updated_at = models.DateField(null=True)
