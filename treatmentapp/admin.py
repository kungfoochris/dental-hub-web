from django.contrib import admin

# Register your models here.
from userapp.models import User
from django.utils.translation import ugettext_lazy as _
from treatmentapp.models import Treatment

class TreatmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'fv_applied', 'treatment_plan_complete',\
		'notes','encounter_id','sdf_whole_mouth')

admin.site.register(Treatment, TreatmentAdmin)



# class AdminAppUser(admin.ModelAdmin):
# 	list_display = ('id', 'username','first_name','middle_name','last_name')

# admin.site.register(AppUser,AdminAppUser)
