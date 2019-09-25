from django.contrib import admin

# Register your models here.
from encounterapp.models import Encounter, History, Refer, Screeing
from django.utils.translation import ugettext_lazy as _


class EncounterAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'patient', 'encounter_type',\
		'author','activity_area','geography','created_at','updated_by','updated_at','other_problem')
	list_filter = ('date','updated_at')

admin.site.register(Encounter, EncounterAdmin)



class HistoryAdmin(admin.ModelAdmin):
	list_display = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever','seizuers_or_epilepsy',\
		'hepatitis_b_or_c','hiv','no_allergies','allergies','other','no_underlying_medical_condition',\
		'not_taking_any_medications','medications','no_medications','encounter_id')


admin.site.register(History, HistoryAdmin)


class ReferAdmin(admin.ModelAdmin):
	list_display = ('id','no_referal','health_post','dentist',\
		'general_physician','hygienist','other','encounter_id')


admin.site.register(Refer, ReferAdmin)


class ScreeingAdmin(admin.ModelAdmin):
	list_display = ('id','carries_risk','decayed_primary_teeth','decayed_permanent_teeth',\
		'cavity_permanent_posterior_teeth','cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis',\
		'need_art_filling','need_extraction','need_sdf','active_infection','encounter_id','high_blood_pressure','low_blood_pressure',\
		'thyroid_disorder')
admin.site.register(Screeing, ScreeingAdmin)
