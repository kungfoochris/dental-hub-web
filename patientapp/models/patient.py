from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,\
    PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from userapp.models import User
from addressapp.models import Address
from datetime import date 
from django.core.validators import MaxValueValidator
from addressapp.models import Geography, ActivityArea


REQUEST_CHOICES = (
    ("male", _("Male")),
    ("female", _("Female")),
    ("other", _("Other")),
)


MARITAL_CHOICES = (
    ("single", _("Single")),
    ("married", _("Married")),
)



def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Patient(Address):
	id = models.CharField(max_length=200,blank=True)
	uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	middle_name = models.CharField(max_length=60,blank=True)
	gender = models.CharField(choices=REQUEST_CHOICES,max_length=30)
	dob = models.DateField(_("date of birth"))
	age = models.PositiveIntegerField(editable=False,null=True)
	phone = models.CharField(_("phone number"),max_length=17,unique=True)
	marital_status = models.CharField(choices=MARITAL_CHOICES,max_length=30,default='single')
	education = models.CharField(_("education level"),max_length=255)
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_obj',null=True)
	date = models.DateTimeField(_('register_date'),auto_now=True)
	latitude = models.DecimalField(help_text='author latitude',max_digits=12, decimal_places=8,default=12)
	longitude = models.DecimalField(help_text='author longitude',max_digits=12, decimal_places=8,default=12)
	ward = models.PositiveIntegerField(_('ward no'),validators=[MaxValueValidator(99)])
	activity_area = models.ForeignKey(ActivityArea,on_delete=models.CASCADE,related_name='patient_area',null=True)
	geography = models.ForeignKey(Geography,on_delete=models.CASCADE,related_name='patient_geography',null=True)



	def save(self, *args, **kwargs):
		today = date.today()
		dob = self.dob
		age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
		self.age=age
		print(age)
		super(Patient, self).save(*args, **kwargs)

	@property
	def full_name(self):
		return "%s %s %s" %(self.first_name, self.middle_name,self.last_name)