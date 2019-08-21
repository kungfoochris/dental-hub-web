from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter

REQUEST_CHOICES = (
    ("Low", _("Low")),
    ("High", _("High")),
    ("Medium", _("Medium")),
)


def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Screeing(models.Model):
	id = models.CharField(max_length=200,blank=True)
	uid = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	caries_risk = models.CharField(_('caries risk'),choices=REQUEST_CHOICES,max_length=30)
	primary_teeth = models.PositiveIntegerField(_('decayed primary teeth'))
	permanent_teeth = models.PositiveIntegerField(_('decayed permanent teeth'))
	postiror_teeth = models.BooleanField(_('cavity permanent postiror teeth'),default=False)
	anterior_teeth = models.BooleanField(_('cavity permanent anterior teeth'),default=False)
	need_sealant = models.BooleanField(_('need sealant'),default=False)
	reversible_pulpitis = models.BooleanField(_('mouth pain due to reversible pulpitis'),default=False)
	art = models.BooleanField(_('Atraumatic restorative treatment'),default=False)
	extraction = models.BooleanField(_('need extraction'),default=False)
	need_sdf = models.BooleanField(_('need sdf'),default=False)
	active_infection = models.BooleanField(default=False)
	encounter_id = models.ForeignKey(Encounter,on_delete=models.CASCADE,related_name='screeing')