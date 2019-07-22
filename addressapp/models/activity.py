# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActivityArea(models.Model):
    name = models.CharField(_('activity area'),max_length=150)
    status = models.BooleanField(default=True)


    def __str__(self):
        return  '%s' %(self.name)