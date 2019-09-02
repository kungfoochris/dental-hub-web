# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator
from encounterapp.models import Encounter
from uuid import uuid4
from userapp.models import User

def keygenerator():
    uid = uuid4()
    return uid.hex.upper()

REQUEST_CHOICES = (
    ("NONE", _("NONE")),
    ("SDF", _("SDF")),
    ("SEAL", _("SEAL")),
    ("ART", _("ART")),
    ("EXO", _("EXO")),
    ("UNTR", _("UNTR")),
    ("SMART", _("SMART")),
)

class Treatment(models.Model):
    id = models.CharField(max_length=200,blank=True)
    uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    tooth18 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth17 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth16 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth15 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth14 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth13 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth12 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth11 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth21 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth22 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth23 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth24 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth25 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth26 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth27 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth28 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth48 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth47 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth46 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth45 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth44 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth43 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth42 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth41 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth31 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth32 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth33 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth34 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth35 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth36 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth37 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth38 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth55 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth54 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth53 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth52 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth51 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth61 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth62 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth63 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth64 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth65 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth85 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth84 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth83 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth82 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth81 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth71 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth72 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth73 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth74 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    tooth75 = models.CharField(choices=REQUEST_CHOICES,default="NONE",max_length=30)
    fluoride_varnish = models.BooleanField(_('fluoride varnish'),default=False)
    treatment_complete = models.BooleanField(_('treatment complete'),default=False)
    note = models.TextField(blank=True)
    encounter_id = models.ForeignKey(Encounter,on_delete=models.CASCADE,related_name='treatment')
    whole_mouth = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='update_treatment')
    updated_date = models.DateField(null=True)
