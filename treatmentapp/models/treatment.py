# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator
from encounterapp.models import Encounter
from uuid import uuid4

def keygenerator():
    uid = uuid4()
    return uid.hex.upper()

REQUEST_CHOICES = (
    ("None", _("None")),
    ("SDF", _("SDF")),
    ("SEAL", _("SEAL")),
    ("ART", _("ART")),
    ("EXO", _("EXO")),
    ("UNTR", _("UNTR")),
)

class Treatment(models.Model):
    id = models.CharField(max_length=200,blank=True)
    uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    teeth1 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth2 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth3 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth4 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth5 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth6 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth7 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth8 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth9 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth10 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth11 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth12 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth13 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth14 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth15 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth16 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth17 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth18 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth19 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth20 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth21 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth22 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth23 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth24 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth25 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth26 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth27 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth28 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth29 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth30 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth31 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    teeth32 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth1 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth2 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth3 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth4 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth5 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth6 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth7 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth8 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth9 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth10 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth11 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth12 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth13 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth14 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth15 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth16 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth17 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth18 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth19 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    primary_teeth20 = models.CharField(choices=REQUEST_CHOICES,default="None",max_length=30)
    fluoride_varnish = models.BooleanField(_('fluoride varnish'),default=False)
    treatment_complete = models.BooleanField(_('treatment complete'),default=False)
    note = models.TextField(blank=True)
    encounter_id = models.ForeignKey(Encounter,on_delete=models.CASCADE,related_name='treatment')
