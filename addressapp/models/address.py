# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    city = models.CharField(_('city/village'),max_length=150,null=True)
    state = models.CharField(_('state/province'),max_length=150,null=True)
    country = models.CharField(max_length=120,null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return  '%s %s %s' %(self.city,self.state,self.country)




  
