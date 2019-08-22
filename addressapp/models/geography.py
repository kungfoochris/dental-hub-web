# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .address import Address
from uuid import uuid4
from django.core.validators import MaxValueValidator


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()



class Geography(models.Model):
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	district = models.CharField(max_length=50)
	municipality = models.CharField(max_length=50)
	tole = models.CharField(max_length=50)
	ward = models.PositiveIntegerField(_('ward_number'),validators=[MaxValueValidator(99)])
	status = models.BooleanField(default=True)

	def __str__(self):
		return self.tole

	@property
	def location(self):
		return "%s , %s - %s" %(self.district,self.municipality, self.ward)