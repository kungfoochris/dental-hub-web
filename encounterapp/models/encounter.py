from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from patientapp.models import Patient
from userapp.models import User
from datetime import datetime, timedelta
from addressapp.models import ActivityArea, Ward, Activity
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
    return datetime.now()+timedelta(minutes=1440)


class Encounter(models.Model):
    # id = models.CharField(max_length=200,null=True)
    id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
    date = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    encounter_type = models.CharField(_('encounter type'),choices=REQUEST_CHOICES,max_length=150)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=default_time)
    activity_area = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='encounter_area')
    other_problem = models.CharField(max_length=150,default="")
    geography = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='encounter_geography')
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='update_encounter')
    updated_at = models.DateField(null=True)
    created_at = models.DateField(db_index=True)


    def __str__(self):
        return self.patient.full_name
