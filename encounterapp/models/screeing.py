from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from .encounter import Encounter
from userapp.models import User
import datetime

REQUEST_CHOICES = (
    ("Low", _("Low")),
    ("High", _("High")),
    ("Medium", _("Medium")),
)

REQUEST_CHOICES1 = (
	("Normal", _("Normal")),
    ("Low", _("Low")),
    ("High", _("High")),
)



def keygenerator():
    uid = uuid4()
    return uid.hex.upper()


class Screeing(models.Model):
	# id = models.CharField(max_length=200,null=True)
	id = models.CharField(max_length=200,primary_key=True, default=keygenerator, editable=False)
	carries_risk = models.CharField(_('caries risk'),choices=REQUEST_CHOICES,max_length=30)
	decayed_primary_teeth = models.PositiveIntegerField(_('decayed primary teeth'))
	decayed_permanent_teeth = models.PositiveIntegerField(_('decayed permanent teeth'))
	cavity_permanent_posterior_teeth = models.BooleanField(_('cavity permanent posterior teeth'),default=False)
	cavity_permanent_anterior_teeth = models.BooleanField(_('cavity permanent anterior teeth'),default=False)
	need_sealant = models.BooleanField(_('need sealant'),default=False)
	reversible_pulpitis = models.BooleanField(_('mouth pain due to reversible pulpitis'),default=False)
	need_art_filling = models.BooleanField(_('Atraumatic restorative treatment'),default=False)
	need_extraction = models.BooleanField(_('need extraction'),default=False)
	need_sdf = models.BooleanField(_('need sdf'),default=False)
	active_infection = models.BooleanField(default=False)
	high_blood_pressure = models.BooleanField(default=False)
	low_blood_pressure = models.BooleanField(default=False)
	thyroid_disorder = models.BooleanField(default=False)
	encounter_id = models.OneToOneField(Encounter,on_delete=models.CASCADE,related_name='screening')
	updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='update_screeing')
	updated_at = models.DateField(null=True)
	created_at = models.DateField()