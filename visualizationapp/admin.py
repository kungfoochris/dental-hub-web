from django.contrib import admin

# Register your models here.
from visualizationapp.models import Visualization
from django.utils.translation import ugettext_lazy as _

from import_export import resources

from import_export.admin import ImportExportActionModelAdmin


class VisualizationResource(resources.ModelResource):
	class Meta:
		model = Visualization
		fields = ('patiend_id', 'encounter_id','activities_id', 'geography_id',\
        'gender','exo','art','seal','sdf','sdf_whole_mouth','fv','refer_hp',\
        'refer_hyg','refer_dent','refer_dr','refer_other','carries_risk',\
        'decayed_primary_teeth_number','decayed_permanent_teeth_number',\
        'cavity_permanent_posterior_teeth','cavity_permanent_anterior_teeth',\
        'active_infection','reversible_pulpitis','need_art_filling',\
        'need_extraction','need_sdf','need_sealant','reason_for_visit',\
        'referral_type')
		export_order = ('patiend_id', 'encounter_id','activities_id',\
        'geography_id','gender','exo','art','seal','sdf','sdf_whole_mouth',\
        'fv','refer_hp','refer_hyg','refer_dent','refer_dr','refer_other',\
        'carries_risk','decayed_primary_teeth_number',\
        'decayed_permanent_teeth_number','cavity_permanent_posterior_teeth',\
        'cavity_permanent_anterior_teeth','active_infection',\
        'reversible_pulpitis','need_art_filling','need_extraction','need_sdf',\
        'need_sealant','reason_for_visit','referral_type')


class AdminVisualization(ImportExportActionModelAdmin):
    def has_add_permission(self, request):
        return False
    resource_class = VisualizationResource
    list_display = ('id', 'patiend_id', 'encounter_id','activities_id',\
	'geography_id','gender')

admin.site.register(Visualization, AdminVisualization)

# class AdminVisualization(admin.ModelAdmin):
#     list_display = ('id', 'patiend_id', 'encounter_id','activities_id', 'geography_id')
# admin.site.register(Visualization, AdminVisualization)
