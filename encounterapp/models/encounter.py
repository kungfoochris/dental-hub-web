from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from patientapp.models import Patient
from userapp.models import User
from datetime import datetime, timedelta
from addressapp.models import Geography, ActivityArea, Ward

REQUEST_CHOICES = (
    ("screeing", _("Checkup/Screeing")),
    ("pain", _("Relief of pain")),
    ("treatment plan", _("Continuation of treatment plan")),
    ("other", _("Other Problem")),
)


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()



def default_time():
    return datetime.now()+timedelta(minutes=1440)


class Encounter(models.Model):
    id = models.CharField(max_length=200,blank=True)
    uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    date = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    encounter_type = models.CharField(_('encounter type'),choices=REQUEST_CHOICES,max_length=30)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=default_time)
    activity_area = models.ForeignKey(ActivityArea,on_delete=models.CASCADE,related_name='encounter_area',null=True)
    geography = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='encounter_geography',null=True)
