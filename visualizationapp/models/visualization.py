from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from encounterapp.models import Encounter, Screeing, Refer
from django.db.models.signals import post_save
from nepali.datetime import NepaliDate
from django.db.models import Q
from django.dispatch import receiver
from treatmentapp.models import Treatment
from django.db.models import Count
from collections import Counter

today = NepaliDate()


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Visualization(models.Model):
    id = models.CharField(
        max_length=200, primary_key=True, default=keygenerator, editable=False
    )
    patiend_id = models.CharField(max_length=60, db_index=True)
    patient_name = models.CharField(max_length=100, default="")
    encounter_id = models.CharField(max_length=60, unique=True, db_index=True)
    age = models.IntegerField(db_index=True)
    gender = models.CharField(max_length=60, db_index=True)
    activities_id = models.CharField(max_length=60, db_index=True, null=True)
    activity_name = models.CharField(max_length=100, default="")
    geography_id = models.CharField(max_length=60, db_index=True, default="")
    geography_name = models.CharField(max_length=100, default="")
    exo = models.IntegerField(default=0, db_index=True)
    art = models.IntegerField(default=0, db_index=True)
    seal = models.IntegerField(default=0, db_index=True)
    sdf = models.IntegerField(default=0, db_index=True)
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
    need_extraction = models.BooleanField(
        _("need extraction"), default=False, db_index=True
    )
    need_sdf = models.BooleanField(default=False, db_index=True)
    created_at = models.DateField(null=True, blank=True, db_index=True)
    sdf_whole_mouth = models.BooleanField(default=False, db_index=True)
    decayed_primary_teeth_number = models.PositiveIntegerField(
        _("decayed primary teeth"), default=0, db_index=True
    )
    decayed_permanent_teeth_number = models.PositiveIntegerField(
        _("decayed permanent teeth"), default=0, db_index=True
    )
    need_sealant = models.BooleanField(default=False, db_index=True)
    reason_for_visit = models.CharField(max_length=60, default="", db_index=True)
    referral_type = models.CharField(max_length=60, default="", db_index=True)
    author = models.CharField(max_length=60, default="")


def create_encounter(sender, **kwargs):
    if Encounter.objects.filter(id=kwargs["instance"].id):
        encounter_obj = Encounter.objects.get(id=kwargs["instance"].id)
        visualization_obj = Visualization()
        if Visualization.objects.filter(encounter_id=encounter_obj.id):
            print("visualization for this encounter is already exists.")
            visualization_obj = Visualization.objects.get(encounter_id=encounter_obj.id)
        visualization_obj.patiend_id = encounter_obj.patient.id
        visualization_obj.patient_name = encounter_obj.patient.full_name
        visualization_obj.gender = encounter_obj.patient.gender
        visualization_obj.encounter_id = kwargs["instance"].id
        dob = encounter_obj.patient.dob
        visualization_obj.age = (
            today.npYear()
            - dob.year
            - ((today.npMonth(), today.npDay()) < (dob.month, dob.day))
        )
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
    if Visualization.objects.filter(encounter_id=kwargs["instance"].encounter_id.id):
        visualization_obj = Visualization.objects.get(
            encounter_id=kwargs["instance"].encounter_id.id
        )
        visualization_obj.carries_risk = kwargs["instance"].carries_risk
        visualization_obj.decayed_primary_teeth_number = kwargs[
            "instance"
        ].decayed_primary_teeth
        visualization_obj.decayed_permanent_teeth_number = kwargs[
            "instance"
        ].decayed_permanent_teeth
        visualization_obj.decayed_primary_teeth = True
        visualization_obj.decayed_permanent_teeth = True
        visualization_obj.cavity_permanent_posterior_teeth = kwargs[
            "instance"
        ].cavity_permanent_posterior_teeth
        visualization_obj.cavity_permanent_anterior_teeth = kwargs[
            "instance"
        ].cavity_permanent_anterior_teeth
        visualization_obj.active_infection = kwargs["instance"].active_infection
        visualization_obj.reversible_pulpitis = kwargs["instance"].reversible_pulpitis
        visualization_obj.need_art_filling = kwargs["instance"].need_art_filling
        visualization_obj.need_extraction = kwargs["instance"].need_extraction
        visualization_obj.need_sealant = kwargs["instance"].need_sealant
        visualization_obj.save()
    # if kwargs['created']:


post_save.connect(create_screeing, sender=Screeing)


def create_refer(sender, **kwargs):
    if Visualization.objects.filter(encounter_id=kwargs["instance"].encounter_id.id):
        visualization_obj = Visualization.objects.get(
            encounter_id=kwargs["instance"].encounter_id.id
        )
        visualization_obj.refer_hp = kwargs["instance"].health_post
        visualization_obj.refer_hyg = kwargs["instance"].hygienist
        visualization_obj.refer_dent = kwargs["instance"].dentist
        visualization_obj.refer_dr = kwargs["instance"].general_physician
        if kwargs["instance"].other == "":
            visualization_obj.refer_other = False
        else:
            visualization_obj.refer_other = True
            visualization_obj.referral_type = "Refer Other"

        if kwargs["instance"].health_post is True:
            visualization_obj.referral_type = "Refer Hp"

        if kwargs["instance"].dentist is True:
            visualization_obj.referral_type = "Refer Dent"

        if kwargs["instance"].hygienist is True:
            visualization_obj.referral_type = "Refer Hyg"

        if kwargs["instance"].general_physician is True:
            visualization_obj.referral_type = "Refer Dr"

        visualization_obj.save()
    # if kwargs['created']:


post_save.connect(create_refer, sender=Refer)


def create_treatment(sender, **kwargs):
    if Visualization.objects.filter(encounter_id=kwargs["instance"].encounter_id.id):
        visualization_obj = Visualization.objects.get(
            encounter_id=kwargs["instance"].encounter_id.id
        )
        treatment_obj = Treatment.objects.values('tooth11', 'tooth12', 'tooth13', 'tooth14', 'tooth15', 'tooth16', 'tooth17', 'tooth18', 'tooth21', 'tooth22', 'tooth23', 'tooth24', 'tooth25', 'tooth26', 'tooth27', 'tooth28', 'tooth31', 'tooth32', 'tooth33', 'tooth34', 'tooth35', 'tooth36', 'tooth37', 'tooth38', 'tooth41', 'tooth42', 'tooth43', 'tooth44', 'tooth45', 'tooth46', 'tooth47', 'tooth48', 'tooth51', 'tooth52', 'tooth53', 'tooth54', 'tooth55', 'tooth61', 'tooth62', 'tooth63', 'tooth64', 'tooth65', 'tooth71', 'tooth72', 'tooth73', 'tooth74', 'tooth75', 'tooth81', 'tooth82', 'tooth83', 'tooth84', 'tooth85').annotate(Count('id')).get(id=kwargs["instance"].id)
        if Counter(treatment_obj.values())['EXO'] > 0:
            visualization_obj.exo = Counter(treatment_obj.values())['EXO']
        if Counter(treatment_obj.values())['SDF'] > 0:
            visualization_obj.sdf = Counter(treatment_obj.values())['SDF']
        if Counter(treatment_obj.values())['SEAL'] > 0:
            visualization_obj.seal = Counter(treatment_obj.values())['SEAL']
        if Counter(treatment_obj.values())['ART'] > 0:
            visualization_obj.art = Counter(treatment_obj.values())['ART']
        if Counter(treatment_obj.values())['SMART'] > 0:
            visualization_obj.art = Counter(treatment_obj.values())['ART']
            visualization_obj.sdf = Counter(treatment_obj.values())['SDF']
        visualization_obj.fv = kwargs["instance"].fv_applied
        visualization_obj.sdf_whole_mouth = kwargs["instance"].sdf_whole_mouth
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
