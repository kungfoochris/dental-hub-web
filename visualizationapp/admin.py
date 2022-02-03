from django.contrib import admin

# Register your models here.
from visualizationapp.models import Visualization
from django.utils.translation import ugettext_lazy as _

from import_export import resources

from import_export.admin import ImportExportActionModelAdmin


class VisualizationResource(resources.ModelResource):
	class Meta:
		model = Visualization
		fields = ('patiend_id','patient_name','geography_id','geography_name',\
		'activities_id','activity_name','encounter_id','reason_for_visit',\
        'gender','age','carries_risk','decayed_primary_teeth_number',\
        'decayed_permanent_teeth_number','cavity_permanent_posterior_teeth',\
        'cavity_permanent_anterior_teeth', 'exo','art','seal','sdf',\
		'sdf_whole_mouth','fv','referral_type','active_infection',\
        'reversible_pulpitis','need_art_filling','need_extraction','need_sdf',\
        'need_sealant','author','created_at')
		export_order = ('patiend_id','patient_name','geography_id','geography_name',\
		'activities_id','activity_name','encounter_id','reason_for_visit',\
        'gender','age','carries_risk','decayed_primary_teeth_number',\
        'decayed_permanent_teeth_number','cavity_permanent_posterior_teeth',\
        'cavity_permanent_anterior_teeth', 'exo','art','seal','sdf',\
		'sdf_whole_mouth','fv','referral_type','active_infection',\
        'reversible_pulpitis','need_art_filling','need_extraction','need_sdf',\
        'need_sealant','author','created_at')


class AdminVisualization(ImportExportActionModelAdmin):
	def has_add_permission(self, request):
		return False
	resource_class = VisualizationResource
	list_display = ('patiend_id','patient_name','geography_id','geography_name',\
	'activities_id','activity_name','encounter_id','reason_for_visit',\
	'gender','age','carries_risk','decayed_primary_teeth_number',\
	'decayed_permanent_teeth_number','cavity_permanent_posterior_teeth',\
	'cavity_permanent_anterior_teeth', 'exo','art','seal','sdf',\
	'sdf_whole_mouth','fv','referral_type','active_infection',\
	'reversible_pulpitis','need_art_filling','need_extraction','need_sdf',\
	'need_sealant','author','created_at')
	list_filter = ('created_at',)
	search_fields = ['created_at','gender','author','geography_name','activity_name','encounter_id']

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


admin.site.register(Visualization, AdminVisualization)

# class AdminVisualization(admin.ModelAdmin):
#     list_display = ('id', 'patiend_id', 'encounter_id','activities_id', 'geography_id')
# admin.site.register(Visualization, AdminVisualization)
