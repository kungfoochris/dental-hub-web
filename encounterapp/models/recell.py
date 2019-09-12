from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Recell(models.Model):
	# id = models.CharField(max_length=200,blank=True)
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
