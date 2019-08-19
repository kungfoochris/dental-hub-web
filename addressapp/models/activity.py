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

class ActivityArea(models.Model):
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	name = models.CharField(max_length=250,null=True,blank=True)
	area = models.CharField(choices=REQUEST_CHOICES,max_length=30)
	status = models.BooleanField(default=True)

	def __str__(self):
		return  '%s %s' %(self.area,self.name)