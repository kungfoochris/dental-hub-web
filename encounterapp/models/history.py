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
	# id = models.CharField(max_length=200,blank=True)
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	blood_disorder = models.BooleanField(_('bleeding problem'),default=False)
	diabetes = models.BooleanField(default=False)
	liver_problem = models.BooleanField(_('liver problem'),default=False)
	rheumatic_fever = models.BooleanField(_('rheumatic fever'),default=False)
	epilepsy_or_seizures = models.BooleanField(_('epilepsy or seizures'),default=False)
	hepatitis_b_or_c = models.BooleanField(_('hepatitis b or c'),default=False)
	hiv = models.BooleanField(default=False)
	no_allergies = models.BooleanField(default=False)
	allergies = models.CharField(blank=True,null=True,max_length=255)
	other = models.CharField(max_length=255,blank=True)
	no_underlying_medical_condition = models.BooleanField(_('no underlying medical condition'),default=False,)
	not_taking_any_medications = models.BooleanField(_('not taking any medications'),default=False,)
	medications = models.CharField(max_length=255,blank=True)
	no_medications = models.BooleanField(default=False)
	encounter_id = models.OneToOneField(Encounter,on_delete=models.CASCADE,related_name='history')
	updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='update_history')
	updated_at = models.DateField(null=True)
	created_at = models.DateField(default=datetime.date.today)
