from django.contrib import admin

# Register your models here.
from encounterapp.models import Encounter, History, Refer, Screeing
from django.utils.translation import ugettext_lazy as _


class EncounterAdmin(admin.ModelAdmin):
	list_display = ('id','uid', 'date', 'patient', 'encounter_type',\
		'author','activity_area','geography','updated_by','updated_date')
	list_filter = ('date','updated_date')

admin.site.register(Encounter, EncounterAdmin)



class HistoryAdmin(admin.ModelAdmin):
	list_display = ('id','uid','bleeding','diabetes','liver','fever','seizures',\
		'hepatitis','hiv','no_allergies','allergies','other','no_underlying_medical',\
		'not_taking_medication','medication','no_medication','encounter_id','updated_by','updated_date')


admin.site.register(History, HistoryAdmin)


class ReferAdmin(admin.ModelAdmin):
	list_display = ('id','uid','no_referal','health_post','dentist',\
		'physician','hygienist','other','encounter_id','time','date',\
		'updated_by','updated_date')


admin.site.register(Refer, ReferAdmin)


class ScreeingAdmin(admin.ModelAdmin):
	list_display = ('id','uid','caries_risk','primary_teeth','permanent_teeth',\
		'postiror_teeth','anterior_teeth','need_sealant','reversible_pulpitis',\
		'art','extraction','need_sdf','active_infection','encounter_id',\
		'updated_by','updated_date')
admin.site.register(Screeing, ScreeingAdmin)
'updated_by','updated_date'