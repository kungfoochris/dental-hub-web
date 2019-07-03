from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class History(models.Model):
	id = models.CharField(max_length=200,blank=True)
	uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	bleeding = models.BooleanField(_('bleeding problem'),default=False)
	diabete = models.BooleanField(default=False)
	liver = models.BooleanField(_('liver problem'),default=False)
	fever = models.BooleanField(_('rheumatic fever'),default=False)
	seizures = models.BooleanField(_('epilepsy or seizures'),default=False)
	hepatitis = models.BooleanField(_('hepatitis b or b'),default=False)
	hiv = models.BooleanField(default=False)
	allergic = models.BooleanField(default=False)
	other = models.CharField(max_length=255,blank=True)
	medication = models.CharField(max_length=255,blank=True)
	no_medication = models.BooleanField(default=False)
	encounter_id = models.ForeignKey(Encounter,on_delete=models.CASCADE,related_name='history')
