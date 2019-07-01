from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from patientapp.models import Patient
from userapp.models import User
from datetime import datetime, timedelta

REQUEST_CHOICES = (
    ("screeing", _("Screeing")),
    ("pain", _("Relief of pain")),
    ("check", _("Routine check")),
    ("treatment", _("Ongoing treatment")),
)


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()



def default_time():
    return datetime.now()+timedelta(minutes=1440)


class Encounter(models.Model):
    id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    date = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    encounter_type = models.CharField(_('encounter type'),choices=REQUEST_CHOICES,max_length=30)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    update_date = models.DateTimeField(default=default_time)
