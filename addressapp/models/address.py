# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from django.core.validators import MaxValueValidator

def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Address(models.Model):
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	district = models.CharField(max_length=50)
	municipality = models.CharField(max_length=50)
	municipality_type = models.CharField(max_length=50)
	ward = models.PositiveIntegerField(_('ward_number'),validators=[MaxValueValidator(99)])

	def __str__(self):
		return "%s, %s - %s" %(self.district, self.geo_type, self.ward)

	@property
	def address(self):
		return "%s, %s - %s" %(self.district, self.geo_type, self.ward)

class District(models.Model):
    name = models.CharField(max_length=50)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Municipality(models.Model):
	#id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	district = models.ForeignKey(District,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=50)
	status = models.BooleanField(default=True)

	def __str__(self):
		return "%s, %s" %(self.name,self.district.name)

class Ward(models.Model):
	#id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)
	ward = models.PositiveIntegerField(_('ward_number'),validators=[MaxValueValidator(99)])
	status = models.BooleanField(default=False)
	name = models.CharField(max_length=50,default='')

	def __str__(self):
		return "%s , %s - %s" %(self.municipality.district.name,self.municipality.name, self.ward)

	@property
	def district(self):
		return self.municipality.district.name



	@property
	def location(self):
		return "%s, %s - %s" %(self.municipality.district.name,self.municipality.name, self.ward)

	@property
	def municipality_name(self):
		return self.municipality.name
