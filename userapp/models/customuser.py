from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,\
    PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4

from userapp.models import User,Role
from addressapp.models import Ward

def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class CustomUser(User):
	location = models.ManyToManyField(Ward)
	role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='role',null=True)
