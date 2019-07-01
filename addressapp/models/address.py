# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator

class Address(models.Model):
    city = models.CharField(_('city/village'),max_length=150)
    state = models.CharField(_('state/province'),max_length=150)
    country = models.CharField(max_length=120)
    street_address = models.CharField(max_length=255)
    ward = models.PositiveIntegerField(_('ward no'),validators=[MaxValueValidator(99)])

    class Meta:
        abstract = True

    def __str__(self):
        return  '%s %s %s' %(self.city,self.state,self.country)