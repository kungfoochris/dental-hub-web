# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .address import Address

class Geography(Address):
	status = models.BooleanField(default=True)
	





  
