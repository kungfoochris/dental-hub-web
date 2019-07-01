from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter

def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Encountertype(models.Model):
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	screeing = models.BooleanField(_('screeing'),default=False)
	pain = models.BooleanField(_('relief of pain'),default=False)
	check = models.BooleanField(_('routine check'),default=False)
	treatment = models.BooleanField(_('ongoing treatment'),default=False)
	encounter_id = models.ForeignKey(Encounter,on_delete=models.CASCADE)
