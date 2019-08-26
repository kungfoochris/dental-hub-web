from django.contrib import admin

# Register your models here.
from encounterapp.models import Encounter, History, Refer, Screeing
from django.utils.translation import ugettext_lazy as _


class EncounterAdmin(admin.ModelAdmin):
	list_display = ('id','uid', 'date', 'patient', 'encounter_type','author','activity_area','geography')
	list_filter = ('date',)

admin.site.register(Encounter, EncounterAdmin)



class HistoryAdmin(admin.ModelAdmin):
	list_display = ('id','uid','bleeding','diabetes','liver','fever','seizures','hepatitis','hiv','no_allergies','allergies','other','no_underlying_medical','not_taking_medication','medication','no_medication','encounter_id')


admin.site.register(History, HistoryAdmin)


class ReferAdmin(admin.ModelAdmin):
	list_display = ('id','uid','no_referal','health_post','dentist','physician','hygienist','other','encounter_id','time','date')


admin.site.register(Refer, ReferAdmin)


class ScreeingAdmin(admin.ModelAdmin):
	list_display = ('id','uid','caries_risk','primary_teeth','permanent_teeth','postiror_teeth','anterior_teeth','need_sealant','reversible_pulpitis','art','extraction','need_sdf','active_infection','encounter_id')
admin.site.register(Screeing, ScreeingAdmin)
