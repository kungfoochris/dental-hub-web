from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from patientapp.models import Patient
from userapp.models import User
from datetime import datetime, timedelta
from addressapp.models import Ward, Activity
from django.db.models.signals import post_save
import datetime


REQUEST_CHOICES = (
    ("Checkup / Screening", _("Checkup / Screening")),
    ("Relief of pain", _("Relief of pain")),
    ("Continuation of treatment plan", _("Continuation of treatment plan")),
    ("Other Problem", _("Other Problem")),
)


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


def default_time():
    return datetime.now() + timedelta(minutes=1440)


class Encounter(models.Model):
    # id = models.CharField(max_length=200,null=True)
    id = models.CharField(
        max_length=200, primary_key=True, default=keygenerator, editable=False
    )
    date = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    encounter_type = models.CharField(
        _("encounter type"), choices=REQUEST_CHOICES, max_length=150
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_area = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="encounter_area", null=True
    )
    other_problem = models.CharField(max_length=150, default="")
    geography = models.ForeignKey(
        Ward, on_delete=models.CASCADE, related_name="encounter_geography", null=True
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="update_encounter"
    )
    active = models.BooleanField(default=True)
    request_counter = models.IntegerField(default=0)
    updated_at = models.DateField(null=True)
    created_at = models.DateTimeField(db_index=True)
    server_date = models.DateField(null=True, editable=False)

    def __str__(self):
        return "%s, %s" % (self.patient.full_name, self.encounter_type)


def encounter_add(sender, instance, created, **kwargs):
    if created:
        encounter_obj = Encounter.objects.get(id=instance.id)
        encounter_obj.server_date = datetime.datetime.today().date()
        encounter_obj.save()


post_save.connect(encounter_add, sender=Encounter)
