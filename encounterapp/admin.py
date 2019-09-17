from django.contrib import admin

# Register your models here.
from encounterapp.models import Encounter, History, Refer, Screeing
from django.utils.translation import ugettext_lazy as _


class EncounterAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'patient', 'encounter_type',\
		'author','activity_area','geography','created_at','updated_by','updated_at')
	list_filter = ('date','updated_at')

admin.site.register(Encounter, EncounterAdmin)



class HistoryAdmin(admin.ModelAdmin):
	list_display = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever','epilepsy_or_seizures',\
		'hepatitis_b_or_c','hiv','no_allergies','allergies','other','no_underlying_medical_condition',\
		'not_taking_any_medications','medications','no_medications','encounter_id','created_at','updated_by','updated_at')


admin.site.register(History, HistoryAdmin)


class ReferAdmin(admin.ModelAdmin):
	list_display = ('id','no_referal','health_post','dentist',\
		'physician','hygienist','other','encounter_id','time','date',\
		'created_at','updated_by','updated_at')


admin.site.register(Refer, ReferAdmin)


class ScreeingAdmin(admin.ModelAdmin):
	list_display = ('id','caries_risk','decayed_primary_teeth','decayed_permanent_teeth',\
		'cavity_permanent_postiror_teeth','cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis',\
		'need_art_filling','need_extraction','need_sdf','active_infection','encounter_id','high_blood_pressure','low_blood_pressure',\
		'thyroid_disorder','created_at','updated_by','updated_at')
admin.site.register(Screeing, ScreeingAdmin)