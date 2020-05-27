from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,\
    PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from userapp.models import User
from addressapp.models import Address, District, Municipality ,Ward
from datetime import date
from django.core.validators import MaxValueValidator
from addressapp.models import Activity

from django.db.models import Count
from django.db.models.functions import TruncMonth
from nepali.datetime import NepaliDate
import datetime

from django.core.exceptions import ValidationError


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


ACTION_CHOICES = (
    ("Accidentally enter", _("Accidentally enter")),
    ("Duplicate encounter", _("Duplicate encounter")),
    ("Incorrect patient", _("Incorrect patient")),
    ("Incorrect user", _("Incorrect user")),
    ("Other", _("Other")),
    )


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Flag(models.Model):
    id = models.CharField(max_length=200, primary_key=True, default=keygenerator, editable=False)
    created_at = models.DateField(db_index=True)
    updated_at = models.DateField(db_index=True,null=True,blank=True)
    status = models.BooleanField(default=False)
    reason = models.CharField(choices=ACTION_CHOICES, default="Blank",max_length=50)
    other = models.CharField(max_length=250,default="")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=200)
    content_object = GenericForeignKey()
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="flag_author")

    def clean(self):
        if self.reason == 'Other' and self.other == "":
            raise ValidationError(_("other field is required."))
        if self.reason != "Other" and self.other != "":
            raise ValidationError(_("other field is required only only other is choosen in a reason section"))
