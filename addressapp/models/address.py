# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Address(models.Model):
    city = models.CharField(_('city/village'),max_length=150)
    state = models.CharField(_('state/province'),max_length=150)
    country = models.CharField(max_length=120)
    street_address = models.CharField(max_length=255)
    class Meta:
        abstract = True

    def __str__(self):
        return "%s, %s, %s" %(self.street_address, self.city, self.state)


    @property
    def address(self):
        return "%s, %s" %(self.street_address, self.city)


    @property
    def location(self):
        return "%s, %s, %s" %(self.street_address, self.city, self.state)