from django.contrib import admin

# Register your models here.
from patientapp.models import Patient
from django.utils.translation import ugettext_lazy as _

from import_export import resources

from import_export.admin import ImportExportActionModelAdmin

class PatientResource(resources.ModelResource):
	class Meta:
		model = Patient
		fields = ('id','first_name','middle_name','last_name','gender','dob',\
		'phone','author__username','activity_area__name','geography__name',\
		'district__name','municipality__name','ward__ward','education',\
		'updated_by__username','created_at','updated_at','recall_date','recall_time')
		export_order = ('id','first_name','middle_name','last_name','gender',\
		'dob','phone','author__username','activity_area__name',\
		'geography__name','district__name','municipality__name','ward__ward',\
		'education','updated_by__username','created_at','updated_at',\
		'recall_date','recall_time')

class PatientAdmin(ImportExportActionModelAdmin):
	def has_add_permission(self, request):
		return False
	resource_class = PatientResource
	list_display = ('id', 'first_name', 'last_name', 'dob','phone',\
	'author','date','activity_area','geography','ward','updated_by',\
	'created_at','updated_at')
	list_filter = ('date','created_at')
	search_fields = ['first_name','author__username','date',\
	'updated_by__username','updated_at','created_at',\
	'activity_area__name','geography__name','municipality__name','district__name']

admin.site.register(Patient, PatientAdmin)

# class PatientAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'first_name', 'last_name', 'dob','phone',\
# 		'author','date','activity_area','geography','ward','updated_by','created_at','updated_at')
# 	list_filter = ('date','created_at')
# 	search_fields = ['first_name','author__username','date','updated_by__username','updated_at','created_at']
# admin.site.register(Patient,PatientAdmin)
