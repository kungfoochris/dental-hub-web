# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .address import Address, Ward
from uuid import uuid4
from django.core.validators import MaxValueValidator


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()



# class Geography(models.Model):
# 	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
# 	district = models.CharField(max_length=50)
# 	municipality = models.CharField(max_length=50)
# 	tole = models.CharField(max_length=50)
# 	ward = models.PositiveIntegerField(_('ward_number'),validators=[MaxValueValidator(99)])
# 	status = models.BooleanField(default=True)

# 	def __str__(self):
# 		return self.tole

# 	@property
# 	def location(self):
# 		return "%s, %s-%s, %s" %(self.tole,self.municipality, self.ward, self.district)

class Geography(models.Model):
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	ward = models.ForeignKey(Ward,on_delete=models.CASCADE)
	tole = models.CharField(max_length=50)
	status = models.BooleanField(default=True)
	def __str__(self):
		return self.tole

	@property
	def location(self):
		return "%s, %s" %(self.tole,self.ward.location)

	@property
	def district(self):
		return self.ward.municipality.district.name

	@property
	def municipality(self):
		return self.ward.municipality.name

	@property
	def ward_number(self):
		return self.ward.ward
		


		