from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,\
    PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from encounterapp.models import Encounter,Screeing,Refer
from django.db.models.signals import post_save
from nepali.datetime import NepaliDate
import datetime
today = NepaliDate()
from django.db.models import Count
from django.db.models import Q


from treatmentapp.models import Treatment



def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Visualization(models.Model):
    id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    patiend_id = models.CharField(max_length=60)
    encounter_id = models.CharField(max_length=60,unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=60)
    activities_id = models.CharField(max_length=60)
    geography_id = models.CharField(max_length=60)
    exo = models.BooleanField(default=False)
    art = models.BooleanField(default=False)
    seal = models.BooleanField(default=False)
    sdf = models.BooleanField(default=False)
    fv = models.BooleanField(default=False)
    refer_hp = models.BooleanField(default=False)
    refer_hyg = models.BooleanField(default=False)
    refer_dent = models.BooleanField(default=False)
    refer_dr = models.BooleanField(default=False)
    refer_other = models.BooleanField(default=False)
    carries_risk = models.CharField(max_length=60,default="")
    decayed_primary_teeth = models.BooleanField(default=False)
    decayed_permanent_teeth = models.BooleanField(default=False)
    cavity_permanent_posterior_teeth = models.BooleanField(default=False)
    cavity_permanent_anterior_teeth = models.BooleanField(default=False)
    active_infection = models.BooleanField(default=False)
    reversible_pulpitis = models.BooleanField(default=False)
    need_art_filling = models.BooleanField(default=False)
    need_extraction = models.BooleanField(_('need extraction'),default=False)
    need_sdf = models.BooleanField(default=False)
    created_at = models.DateField(null=True,blank=True)
    sdf_whole_mouth = models.BooleanField(default=False)
    decayed_primary_teeth_number = models.PositiveIntegerField(_('decayed primary teeth'),null=True,blank=True)
    decayed_permanent_teeth_number = models.PositiveIntegerField(_('decayed permanent teeth'),null=True,blank=True)



def create_encounter(sender, **kwargs):
    if kwargs['created']:
        encounter_obj = Encounter.objects.get(id=kwargs['instance'].id)
        visualization_obj = Visualization()
        visualization_obj.patiend_id = encounter_obj.patient.id
        visualization_obj.encounter_id = kwargs['instance'].id
        visualization_obj.gender = encounter_obj.patient.gender
        dob = encounter_obj.patient.dob
        visualization_obj.age = today.npYear() - dob.year - ((today.npMonth(), today.npDay()) < (dob.month, dob.day))
        visualization_obj.activities_id = encounter_obj.activity_area.id
        visualization_obj.geography_id = encounter_obj.geography.id
        visualization_obj.created_at = encounter_obj.patient.created_at
        visualization_obj.save()
post_save.connect(create_encounter,sender=Encounter)

def create_screeing(sender, **kwargs):
    if kwargs['created']:
        print("=----")
        print(kwargs['instance'].encounter_id.id)
        visualization_obj = Visualization.objects.get(encounter_id=kwargs['instance'].encounter_id.id)
        visualization_obj.carries_risk = kwargs['instance'].carries_risk
        visualization_obj.decayed_primary_teeth_number = screeing_obj.decayed_primary_teeth
        visualization_obj.decayed_permanent_teeth_number = screeing_obj.decayed_permanent_teeth
        visualization_obj.decayed_primary_teeth = True
        visualization_obj.decayed_permanent_teeth = True
        visualization_obj.cavity_permanent_posterior_teeth = kwargs['instance'].cavity_permanent_posterior_teeth
        visualization_obj.cavity_permanent_anterior_teeth = kwargs['instance'].cavity_permanent_anterior_teeth
        visualization_obj.active_infection = kwargs['instance'].active_infection
        visualization_obj.reversible_pulpitis = kwargs['instance'].reversible_pulpitis
        visualization_obj.need_art_filling = kwargs['instance'].need_art_filling
        visualization_obj.need_extraction = kwargs['instance'].need_extraction
        visualization_obj.save()
        print("visualization added")
post_save.connect(create_screeing,sender=Screeing)

def create_refer(sender, **kwargs):
    if kwargs['created']:
        visualization_obj = Visualization.objects.get(encounter_id=kwargs['instance'].encounter_id.id)
        visualization_obj.refer_hp = kwargs['instance'].health_post
        visualization_obj.refer_hyg = kwargs['instance'].hygienist
        visualization_obj.refer_dent = kwargs['instance'].dentist
        visualization_obj.refer_dr = kwargs['instance'].general_physician
        if Refer.objects.filter(encounter_id__id=kwargs['instance'].encounter_id.id).values('other').annotate(Count('other')).count()==1:
            visualization_obj.refer_other = True
        visualization_obj.save()
        print("refer added")
post_save.connect(create_refer,sender=Refer)

def create_treatment(sender, **kwargs):
    if kwargs['created']:
        visualization_obj = Visualization.objects.get(encounter_id=kwargs['instance'].encounter_id.id)
        if Treatment.objects.filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
            |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
			|Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
            |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
            |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
            |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
            |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
            |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__id=kwargs['instance'].encounter_id.id).count()==1:
            visualization_obj.ext = True
        if Treatment.objects.filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
            |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
            |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
            |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
            |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
            |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
            |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
            |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__id=kwargs['instance'].encounter_id.id).count()==1:
            visualization_obj.sdf = True
        if Treatment.objects.filter(Q(tooth11='SEAl') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
            |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
            |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
            |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
            |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
            |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
            |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
            |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__id=kwargs['instance'].encounter_id.id).count()==1:
        	visualization_obj.seal = True
        if Treatment.objects.filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
            |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
            |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
            |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
            |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
            |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
            |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
            |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__id=kwargs['instance'].encounter_id.id).count()==1:
            visualization_obj.art = True
        visualization_obj.fv = kwargs['instance'].fv_applied
        visualization_obj.sdf_whole_mouth = kwargs['instance'].sdf_whole_mouth
        visualization_obj.save()
post_save.connect(create_treatment,sender=Treatment)
