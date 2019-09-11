from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter
from userapp.models import User


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class History(models.Model):
	id = models.CharField(max_length=200,blank=True)
	uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	bleeding = models.BooleanField(_('bleeding problem'),default=False)
	diabetes = models.BooleanField(default=False)
	liver = models.BooleanField(_('liver problem'),default=False)
	fever = models.BooleanField(_('rheumatic fever'),default=False)
	seizures = models.BooleanField(_('epilepsy or seizures'),default=False)
	hepatitis = models.BooleanField(_('hepatitis b or b'),default=False)
	hiv = models.BooleanField(default=False)
	no_allergies = models.BooleanField(default=False)
	allergies = models.CharField(blank=True,null=True,max_length=255)
	other = models.CharField(max_length=255,blank=True)
	no_underlying_medical = models.BooleanField(_('no underlying medical condition'),default=False,)
	not_taking_medication = models.BooleanField(_('not taking any medications'),default=False,)
	medication = models.CharField(max_length=255,blank=True)
	no_medication = models.BooleanField(default=False)
	encounter_id = models.ForeignKey(Encounter,on_delete=models.CASCADE,related_name='history')
	updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='update_history')
	updated_at = models.DateField(null=True)
