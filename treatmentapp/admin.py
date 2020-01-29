from django.contrib import admin

# Register your models here.
from userapp.models import User
from django.utils.translation import ugettext_lazy as _
from treatmentapp.models import Treatment

from import_export import resources

from import_export.admin import ImportExportActionModelAdmin

# class TreatmentAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'fv_applied', 'treatment_plan_complete',\
# 		'notes','encounter_id','sdf_whole_mouth')
# 	list_filter = ('encounter_id__date','encounter_id__updated_at')
# 	search_fields = ['encounter_id__patient__first_name']
#
# 	def has_add_permission(self, request, obj=None):
# 		if request.user.is_superuser:
# 			return True
# 		return False
#
# 	def has_view_permission(self, request, obj=None):
# 		if request.user.is_staff or request.user.is_superuser:
# 			return True
#
# 	def has_delete_permission(self, request, obj=None):
# 		if request.user.is_superuser and request.user.is_staff:
# 			return True
# 		elif request.user.is_staff:
# 			False
#
# 	def has_change_permission(self, request, obj=None):
# 		if request.user.is_superuser and request.user.is_staff:
# 			return True
# 		elif request.user.is_staff:
# 			return False
#
# admin.site.register(Treatment, TreatmentAdmin)



class TreatmentResource(resources.ModelResource):
	class Meta:
		model = Treatment
		fields = ('id','tooth18','tooth17','tooth16','tooth15','tooth14',\
		'tooth13','tooth12', 'tooth11','tooth21',\
		'tooth22','tooth23','tooth24','tooth25',\
		'tooth26','tooth27','tooth28','tooth48','tooth47','tooth46','tooth45',\
		'tooth44','tooth43','tooth42','tooth41','tooth31','tooth32','tooth33',\
		'tooth34','tooth35','tooth36','tooth37','tooth38','tooth55','tooth54',\
		'tooth53','tooth52','tooth51','tooth61','tooth62','tooth63','tooth64',\
		'tooth65','tooth85','tooth84','tooth83','tooth82','tooth81','tooth71',\
		'tooth72','tooth73','tooth74','tooth75',\
		'encounter_id__created_at', 'encounter_id__geography__name',\
		'encounter_id__activity_area__name')
		export_order = ('id','tooth18','tooth17','tooth16','tooth15','tooth14',\
		'tooth13','tooth12', 'tooth11','tooth21',\
		'tooth22','tooth23','tooth24','tooth25',\
		'tooth26','tooth27','tooth28','tooth48','tooth47','tooth46','tooth45',\
		'tooth44','tooth43','tooth42','tooth41','tooth31','tooth32','tooth33',\
		'tooth34','tooth35','tooth36','tooth37','tooth38','tooth55','tooth54',\
		'tooth53','tooth52','tooth51','tooth61','tooth62','tooth63','tooth64',\
		'tooth65','tooth85','tooth84','tooth83','tooth82','tooth81','tooth71',\
		'tooth72','tooth73','tooth74','tooth75',\
		'encounter_id__created_at','encounter_id__geography__name',\
		'encounter_id__activity_area__name')

class TreatmentAdmin(ImportExportActionModelAdmin):
	def has_add_permission(self, request):
		return False
	resource_class = TreatmentResource
	list_display = ('id', 'fv_applied', 'treatment_plan_complete',\
		'notes', 'encounter_id', 'sdf_whole_mouth')
	list_filter = ('encounter_id__date','encounter_id__updated_at')
	search_fields = ['encounter_id__id','encounter_id__geography__name',]

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


admin.site.register(Treatment, TreatmentAdmin)



# class AdminAppUser(admin.ModelAdmin):
# 	list_display = ('id', 'username','first_name','middle_name','last_name')

# admin.site.register(AppUser,AdminAppUser)
