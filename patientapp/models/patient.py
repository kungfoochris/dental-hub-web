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
from addressapp.models import Geography, ActivityArea

from django.db.models import Count
from django.db.models.functions import TruncMonth


REQUEST_CHOICES = (
    ("male", _("Male")),
    ("female", _("Female")),
    ("other", _("Other")),
)




def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Patient(models.Model):
	id = models.CharField(max_length=200,blank=True)
	uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	middle_name = models.CharField(max_length=60,blank=True,null=True)
	gender = models.CharField(choices=REQUEST_CHOICES,max_length=30)
	dob = models.DateField(_("date of birth"))
	age = models.PositiveIntegerField(editable=False,null=True)
	phone = models.CharField(_("phone number"),max_length=17,unique=True)
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_obj')
	date = models.DateTimeField(_('register_date'),auto_now=True)
	latitude = models.DecimalField(help_text='author latitude',max_digits=12, decimal_places=8,default=12)
	longitude = models.DecimalField(help_text='author longitude',max_digits=12, decimal_places=8,default=12)
	activity_area = models.ForeignKey(ActivityArea,on_delete=models.CASCADE,related_name='patient_area')
	geography = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='patient_geography')
	district = models.ForeignKey(District,on_delete=models.CASCADE,null=True)
	municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE,null=True)
	education = models.CharField(max_length=50,null=True)
	ward = models.ForeignKey(Ward,on_delete=models.CASCADE,null=True)



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