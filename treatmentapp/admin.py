from django.contrib import admin

# Register your models here.
from userapp.models import User
from django.utils.translation import ugettext_lazy as _
from treatmentapp.models import Treatment

class TreatmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'fv_applied', 'treatment_plan_complete',\
		'notes','encounter_id','sdf_whole_mouth')
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

admin.site.register(Treatment, TreatmentAdmin)



# class AdminAppUser(admin.ModelAdmin):
# 	list_display = ('id', 'username','first_name','middle_name','last_name')

# admin.site.register(AppUser,AdminAppUser)
