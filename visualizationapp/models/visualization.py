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

from django.dispatch import receiver
from treatmentapp.models import Treatment



def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Visualization(models.Model):
    id = models.CharField(max_length=200,\
        primary_key=True, default=keygenerator, editable=False)
    patiend_id = models.CharField(max_length=60, db_index=True)
    patient_name = models.CharField(max_length=100, default="")
    encounter_id = models.CharField(max_length=60, unique=True, db_index=True)
    age = models.IntegerField(db_index=True)
    gender = models.CharField(max_length=60, db_index=True)
    activities_id = models.CharField(max_length=60, db_index=True, null=True)
    activity_name = models.CharField(max_length=100, default="")
    geography_id = models.CharField(max_length=60, db_index=True, default="")
    geography_name = models.CharField(max_length=100, default="")
    exo = models.BooleanField(default=False, db_index=True)
    art = models.BooleanField(default=False, db_index=True)
    seal = models.BooleanField(default=False, db_index=True)
    sdf = models.BooleanField(default=False, db_index=True)
    fv = models.BooleanField(default=False, db_index=True)
    refer_hp = models.BooleanField(default=False, db_index=True)
    refer_hyg = models.BooleanField(default=False, db_index=True)
    refer_dent = models.BooleanField(default=False, db_index=True)
    refer_dr = models.BooleanField(default=False, db_index=True)
    refer_other = models.BooleanField(default=False, db_index=True)
    carries_risk = models.CharField(max_length=60, default="", db_index=True)
    decayed_primary_teeth = models.BooleanField(default=False, db_index=True)
    decayed_permanent_teeth = models.BooleanField(default=False, db_index=True)
    cavity_permanent_posterior_teeth = models.BooleanField(default=False, db_index=True)
    cavity_permanent_anterior_teeth = models.BooleanField(default=False, db_index=True)
    active_infection = models.BooleanField(default=False, db_index=True)
    reversible_pulpitis = models.BooleanField(default=False, db_index=True)
    need_art_filling = models.BooleanField(default=False, db_index=True)
    need_extraction = models.BooleanField(_('need extraction'), default=False, db_index=True)
    need_sdf = models.BooleanField(default=False, db_index=True)
    created_at = models.DateField(null=True, blank=True, db_index=True)
    sdf_whole_mouth = models.BooleanField(default=False, db_index=True)
    decayed_primary_teeth_number = models.PositiveIntegerField(_('decayed primary teeth'),\
        default=0, db_index=True)
    decayed_permanent_teeth_number = models.PositiveIntegerField(_('decayed permanent teeth'),\
        default=0, db_index=True)
    need_sealant = models.BooleanField(default=False, db_index=True)
    reason_for_visit = models.CharField(max_length=60, default="", db_index=True)
    referral_type = models.CharField(max_length=60, default="", db_index=True)
    author = models.CharField(max_length=60, default="")

    # class Meta:
    #     indexes = [
    #     models.Index(fields=['activities_id', 'geography_id',]),
    #     models.Index(fields=['-created_at',]),
    #     ]



def create_encounter(sender, **kwargs):
    if Encounter.objects.filter(id=kwargs['instance'].id):
        encounter_obj = Encounter.objects.get(id=kwargs['instance'].id)
        visualization_obj = Visualization()
        if Visualization.objects.filter(encounter_id=encounter_obj.id):
            print("visualization for this encounter is already exists.")
            visualization_obj = Visualization.objects.get(encounter_id=encounter_obj.id)
        visualization_obj.patiend_id = encounter_obj.patient.id
        visualization_obj.patient_name = encounter_obj.patient.full_name
        visualization_obj.gender = encounter_obj.patient.gender
        visualization_obj.encounter_id = kwargs['instance'].id
        dob = encounter_obj.patient.dob
        visualization_obj.age = today.npYear() - dob.year - ((today.npMonth(), today.npDay()) < (dob.month, dob.day))
        if encounter_obj.activity_area:
            visualization_obj.activities_id = encounter_obj.activity_area.id
            visualization_obj.activity_name = encounter_obj.activity_area.name
        if encounter_obj.geography:
            visualization_obj.geography_id = encounter_obj.geography.id
            visualization_obj.geography_name = encounter_obj.geography.name
        visualization_obj.created_at = encounter_obj.patient.created_at
        visualization_obj.reason_for_visit = encounter_obj.encounter_type
        visualization_obj.author = encounter_obj.author.username
        visualization_obj.save()
    # if kwargs['created']:

post_save.connect(create_encounter, sender=Encounter)

def create_screeing(sender, **kwargs):
    if Visualization.objects.filter(encounter_id=kwargs['instance'].encounter_id.id):
        visualization_obj = Visualization.objects.get(encounter_id=kwargs['instance'].encounter_id.id)
        visualization_obj.carries_risk = kwargs['instance'].carries_risk
        visualization_obj.decayed_primary_teeth_number = kwargs['instance'].decayed_primary_teeth
        visualization_obj.decayed_permanent_teeth_number = kwargs['instance'].decayed_permanent_teeth
        visualization_obj.decayed_primary_teeth = True
        visualization_obj.decayed_permanent_teeth = True
        visualization_obj.cavity_permanent_posterior_teeth = kwargs['instance'].cavity_permanent_posterior_teeth
        visualization_obj.cavity_permanent_anterior_teeth = kwargs['instance'].cavity_permanent_anterior_teeth
        visualization_obj.active_infection = kwargs['instance'].active_infection
        visualization_obj.reversible_pulpitis = kwargs['instance'].reversible_pulpitis
        visualization_obj.need_art_filling = kwargs['instance'].need_art_filling
        visualization_obj.need_extraction = kwargs['instance'].need_extraction
        visualization_obj.need_sealant = kwargs['instance'].need_sealant
        visualization_obj.save()
    # if kwargs['created']:

post_save.connect(create_screeing,sender=Screeing)

def create_refer(sender, **kwargs):
    if Visualization.objects.filter(encounter_id=kwargs['instance'].encounter_id.id):
        visualization_obj = Visualization.objects.get(encounter_id=kwargs['instance'].encounter_id.id)
        visualization_obj.refer_hp = kwargs['instance'].health_post
        visualization_obj.refer_hyg = kwargs['instance'].hygienist
        visualization_obj.refer_dent = kwargs['instance'].dentist
        visualization_obj.refer_dr = kwargs['instance'].general_physician
        if  kwargs['instance'].other=="":
            visualization_obj.refer_other = False
        else:
            visualization_obj.refer_other = True
            visualization_obj.referral_type = "Refer Other"

        if kwargs['instance'].health_post is True:
            visualization_obj.referral_type = "Refer Hp"

        if kwargs['instance'].dentist is True:
            visualization_obj.referral_type = "Refer Dent"

        if kwargs['instance'].hygienist is True:
            visualization_obj.referral_type = "Refer Hyg"

        if kwargs['instance'].general_physician is True:
            visualization_obj.referral_type = "Refer Dr"

        visualization_obj.save()
    # if kwargs['created']:

post_save.connect(create_refer,sender=Refer)

def create_treatment(sender, **kwargs):
    if Visualization.objects.filter(encounter_id=kwargs['instance'].encounter_id.id):
        visualization_obj = Visualization.objects.get(encounter_id=kwargs['instance'].encounter_id.id)
        if Treatment.objects.filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
            |Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
            |Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
            |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
            |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
            |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
            |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
            |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__id=kwargs['instance'].encounter_id.id):
            visualization_obj.exo = True
        if Treatment.objects.filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
            |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
            |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
            |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
            |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
            |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
            |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
            |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__id=kwargs['instance'].encounter_id.id):
            visualization_obj.sdf = True
        if Treatment.objects.filter(Q(tooth11='SEAl') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
            |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
            |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
            |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
            |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
            |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
            |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
            |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__id=kwargs['instance'].encounter_id.id):
            visualization_obj.seal = True

        if Treatment.objects.filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
            |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
            |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
            |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
            |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
            |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
            |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
            |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__id=kwargs['instance'].encounter_id.id):
            visualization_obj.art = True

        if Treatment.objects.filter(Q(tooth11='SMART') | Q(tooth12='SMART')|Q(tooth13='SMART') | Q(tooth14='SMART')|Q(tooth15='SMART') | Q(tooth16='SMART')|Q(tooth17='SMART') | Q(tooth18='SMART')\
            |Q(tooth21='SMART') | Q(tooth22='SMART')|Q(tooth23='SMART') | Q(tooth24='SMART')|Q(tooth25='SMART') | Q(tooth26='SMART')|Q(tooth27='SMART') | Q(tooth28='SMART')\
            |Q(tooth31='SMART') | Q(tooth32='SMART')|Q(tooth33='SMART') | Q(tooth34='SMART')|Q(tooth35='SMART') | Q(tooth36='SMART')|Q(tooth37='SMART') | Q(tooth38='SMART')\
            |Q(tooth41='SMART') | Q(tooth42='SMART')|Q(tooth43='SMART') | Q(tooth44='SMART')|Q(tooth45='SMART') | Q(tooth46='SMART')|Q(tooth47='SMART') | Q(tooth48='SMART')\
            |Q(tooth51='SMART') | Q(tooth52='SMART')|Q(tooth53='SMART') | Q(tooth54='SMART')|Q(tooth55='SMART')\
            |Q(tooth61='SMART') | Q(tooth62='SMART')|Q(tooth63='SMART') | Q(tooth64='SMART')|Q(tooth65='SMART')\
            |Q(tooth71='SMART') | Q(tooth72='SMART')|Q(tooth73='SMART') | Q(tooth74='SMART')|Q(tooth75='SMART')\
            |Q(tooth81='SMART') | Q(tooth82='SMART')|Q(tooth83='SMART') | Q(tooth84='SMART')|Q(tooth85='SMART')).filter(encounter_id__id=kwargs['instance'].encounter_id.id):
            visualization_obj.art = True
            visualization_obj.sdf = True
        visualization_obj.fv = kwargs['instance'].fv_applied
        visualization_obj.sdf_whole_mouth = kwargs['instance'].sdf_whole_mouth
        visualization_obj.save()
    # if kwargs['created']:

post_save.connect(create_treatment, sender=Treatment)



@receiver(models.signals.pre_delete, sender=Encounter)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.id:
        if Visualization.objects.filter(encounter_id=instance.id):
            for i in Visualization.objects.filter(encounter_id=instance.id):
                i.delete()
