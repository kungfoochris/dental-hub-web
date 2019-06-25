from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,\
    PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from userapp.models import User
from addressapp.models import Address

REQUEST_CHOICES = (
    ("male", _("Male")),
    ("female", _("Female")),
    ("other", _("Other")),
)


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Patient(Address):
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	middle_name = models.CharField(max_length=60)
	gender = models.CharField(choices=REQUEST_CHOICES,max_length=30)
	dob = models.DateField(_("date of birth"),null=True)
	phone = models.CharField(_("phone number"),max_length=17,unique=True)
	education = models.CharField(_("education level"),max_length=255)
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_obj',null=True)
	date = models.DateTimeField(_('register_date'),auto_now=True)
	latitude = models.DecimalField(help_text='author latitude',max_digits=12, decimal_places=8,default=12)
	longitude = models.DecimalField(help_text='author longitude',max_digits=12, decimal_places=8,default=12)


	@property
	def full_name(self):
		return "%s %s %s" %(self.first_name, self.middle_name,self.last_name)