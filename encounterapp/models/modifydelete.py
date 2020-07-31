from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from patientapp.models import Patient
from userapp.models import User
from datetime import datetime, timedelta
from . encounter import Encounter
from datetime import datetime, timedelta


def default_time():
    return datetime.now()+timedelta(minutes=5)


REASON_FOR_DELETION = (
    ("accidental_entry", _("Accidental Entry")),
    ("duplicate_encounter", _("Duplicate Encounter")),
    ("incorrect_patient", _("Incorrect Patient")),
    ("incorrect_user", _("Incorrect User")),
    ("other", _("Other")),
)

MODIFY_STATUS = (
    ("pending", _("Pending ")),
    ("approved", _("Approved")),
    ("rejected", _("Rejected")),
    ("modified", _("Modified")),
    ("expired", _("Expired")),
)

DELETE_STATUS = (
    ("pending", _("Pending ")),
    ("deleted", _("Deleted")),
)

FLAG = (
    ("modify", _("Modify ")),
    ("delete", _("Delete")),
)



class ModifyDelete(models.Model):
    encounter = models.ForeignKey(Encounter,on_delete=models.CASCADE,related_name='encounter_modify_delete',null=True)
    reason_for_modification = models.TextField(default="")
    modify_status = models.CharField(max_length=100,choices = MODIFY_STATUS,default="")
    reason_for_deletion = models.CharField(max_length=100,choices = REASON_FOR_DELETION,default="")
    other_reason_for_deletion = models.TextField(default="")
    delete_status = models.CharField(max_length=100,choices = DELETE_STATUS,default="")
    flag = models.CharField(max_length=100,choices = FLAG)
    modify_approved_at = models.DateTimeField(null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    modify_expiry_date = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    restore_expiry_date = models.DateTimeField(null=True)
    


    def __str__(self):
        return self.encounter.patient.full_name


