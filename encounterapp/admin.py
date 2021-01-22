from django.contrib import admin

# Register your models here.
from encounterapp.models import Encounter, History, Refer, Screeing
from encounterapp.models.modifydelete import ModifyDelete
from django.utils.translation import ugettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class EncounterResource(resources.ModelResource):
	class Meta:
		model = Encounter
		fields = ('id', 'date', 'patient', 'encounter_type',\
		'author','activity_area', 'area', 'geography','created_at','updated_by','updated_at','other_problem')
		export_order = ('id', 'date', 'patient', 'encounter_type',\
		'author','activity_area', 'area', 'geography','created_at','updated_by','updated_at','other_problem')

class EncounterAdmin(ImportExportActionModelAdmin):
	resource_class = EncounterResource
	list_display = ('id', 'date', 'patient', 'encounter_type',\
		'author','activity_area', 'area', 'geography','created_at','updated_by','updated_at','other_problem')
	list_filter = ('date','updated_at')
	search_fields = ['id', 'patient__id', 'area__area', 'author__username','date','updated_by__username','updated_at','created_at']

	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def has_view_permission(self, request, obj=None):
		if request.user.is_staff or request.user.is_superuser:
			return True

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			False

	def has_change_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			return False

admin.site.register(Encounter, EncounterAdmin)


class HistoryResource(resources.ModelResource):
	class Meta:
		model = History
		fields = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever','seizuers_or_epilepsy',\
		'hepatitis_b_or_c','hiv','no_allergies','allergies','other','no_underlying_medical_condition',\
		'not_taking_any_medications','medications','no_medications','encounter_id',\
		'high_blood_pressure','low_blood_pressure','thyroid_disorder')
		export_order = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever','seizuers_or_epilepsy',\
		'hepatitis_b_or_c','hiv','no_allergies','allergies','other','no_underlying_medical_condition',\
		'not_taking_any_medications','medications','no_medications','encounter_id',\
		'high_blood_pressure','low_blood_pressure','thyroid_disorder')


class HistoryAdmin(ImportExportActionModelAdmin):
	resource_class = HistoryResource
	list_display = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever','seizuers_or_epilepsy',\
		'hepatitis_b_or_c','hiv','no_allergies','allergies','other','no_underlying_medical_condition',\
		'not_taking_any_medications','medications','no_medications','encounter_id',\
		'high_blood_pressure','low_blood_pressure','thyroid_disorder')
	list_filter = ('encounter_id__date','encounter_id__updated_at')
	search_fields = ['encounter_id__patient__first_name']

	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def has_view_permission(self, request, obj=None):
		if request.user.is_staff or request.user.is_superuser:
			return True

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			False

	def has_change_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			return False

admin.site.register(History, HistoryAdmin)



class ReferResource(resources.ModelResource):
	class Meta:
		model = Refer
		fields = ('id','no_referal','health_post','dentist',\
		'general_physician','hygienist','other','encounter_id')
		export_order = ('id','no_referal','health_post','dentist',\
		'general_physician','hygienist','other','encounter_id')


class ReferAdmin(ImportExportActionModelAdmin):
	resource_class = ReferResource
	list_display = ('id','no_referal','health_post','dentist',\
		'general_physician','hygienist','other','encounter_id')
	list_filter = ('encounter_id__date','encounter_id__updated_at')
	search_fields = ['encounter_id__id','encounter_id__patient__first_name']


	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def has_view_permission(self, request, obj=None):
		if request.user.is_staff or request.user.is_superuser:
			return True

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			False

	def has_change_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			return False


admin.site.register(Refer, ReferAdmin)


class ScreeningResource(resources.ModelResource):
	class Meta:
		model = Screeing
		fields = ('id','carries_risk','decayed_primary_teeth','decayed_permanent_teeth',\
		'cavity_permanent_posterior_teeth','cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis',\
		'need_art_filling','need_extraction','need_sdf','active_infection','encounter_id')
		export_order = ('id','carries_risk','decayed_primary_teeth','decayed_permanent_teeth',\
		'cavity_permanent_posterior_teeth','cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis',\
		'need_art_filling','need_extraction','need_sdf','active_infection','encounter_id')


class ScreeingAdmin(ImportExportActionModelAdmin):
	resource_class = ScreeningResource
	list_display = ('id','carries_risk','decayed_primary_teeth','decayed_permanent_teeth',\
		'cavity_permanent_posterior_teeth','cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis',\
		'need_art_filling','need_extraction','need_sdf','active_infection','encounter_id')
	list_filter = ('encounter_id__date','encounter_id__updated_at')
	search_fields = ['encounter_id__id','encounter_id__patient__first_name']

	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def has_view_permission(self, request, obj=None):
		if request.user.is_staff or request.user.is_superuser:
			return True

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			False

	def has_change_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			return False

admin.site.register(Screeing, ScreeingAdmin)




class ModifyDeleteAdmin(admin.ModelAdmin):
	list_display = ('id', 'encounter', 'reason_for_modification', 'modify_status',\
		'reason_for_deletion','other_reason_for_deletion','delete_status','flag','modify_approved_at','author')
	search_fields = ['id', 'encounter__id']

	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		return False

	def has_view_permission(self, request, obj=None):
		if request.user.is_staff or request.user.is_superuser:
			return True

	def has_delete_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			False

	def has_change_permission(self, request, obj=None):
		if request.user.is_superuser and request.user.is_staff:
			return True
		elif request.user.is_staff:
			return False

admin.site.register(ModifyDelete, ModifyDeleteAdmin)


