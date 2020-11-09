# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


from uuid import uuid4

REQUEST_CHOICES = (
    ("Health Post", _("Health Post")),
    ("School Seminar", _("School Seminar")),
    ("Community Outreach", _("Community Outreach")),
    ("Training", _("Training")),
)

def keygenerator():
    uid = uuid4()
    return uid.hex.upper()

class Activity(models.Model):
	name = models.CharField(max_length=250,unique=True)

	def __str__(self):
		return self.name

class ActivityArea(models.Model):
	activity = models.ForeignKey(Activity,on_delete=models.CASCADE,null=True)
	area = models.CharField(max_length=30,null=True,blank=True)
	status = models.BooleanField(default=True)

	def __str__(self):
		return  '%s %s' %(self.area,self.name)
