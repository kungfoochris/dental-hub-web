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
from addressapp.models import Geography, Activity

from django.db.models import Count
from django.db.models.functions import TruncMonth
from nepali.datetime import NepaliDate
import datetime

REQUEST_CHOICES = (
    ("male", _("Male")),
    ("female", _("Female")),
    ("other", _("Other")),
)




def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Patient(models.Model):
	# id = models.CharField(max_length=200,blank=True)
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	middle_name = models.CharField(max_length=60,blank=True)
	gender = models.CharField(choices=REQUEST_CHOICES,max_length=30)
	dob = models.DateField(_("date of birth"))
	phone = models.CharField(_("phone number"),max_length=17)
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_obj')
	date = models.DateTimeField(_('register_date'),auto_now=True)
	latitude = models.DecimalField(help_text='author latitude',max_digits=12, decimal_places=8,default=12)
	longitude = models.DecimalField(help_text='author longitude',max_digits=12, decimal_places=8,default=12)
	activity_area = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='patient_area')
	geography = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='patient_geography')
	district = models.ForeignKey(District,on_delete=models.CASCADE)
	municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)
	education = models.CharField(max_length=50)
	ward = models.ForeignKey(Ward,on_delete=models.CASCADE,)
	updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='update_patient')
	updated_at = models.DateField(blank=True,null=True)
	created_at = models.DateField(db_index=True)
	recall_date = models.DateField(blank=True,null=True)
	recall_time = models.TimeField(blank=True,null=True)
	recall_geography = models.IntegerField(blank=True,default=0)


	def __str__(self):
		return "%s %s %s" %(self.first_name, self.middle_name,self.last_name)

	# def save(self, *args, **kwargs):
	# 	today = NepaliDate()
	# 	dob = self.dob
	# 	age = today.npYear() - dob.year - ((today.npMonth(), today.npDay()) < (dob.month, dob.day))
	# 	self.age=age
	# 	print(age)
	# 	super(Patient, self).save(*args, **kwargs)

	# def save(self, *args, **kwargs):
	# 	today = date.today()
	# 	dob = self.dob
	# 	age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
	# 	self.age=age
	# 	print(age)
	# 	super(Patient, self).save(*args, **kwargs)

	@property
	def full_name(self):
		return "%s %s %s" %(self.first_name, self.middle_name,self.last_name)
