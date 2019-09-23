from django.contrib import admin

# Register your models here.
from addressapp.models import Geography,District, Municipality ,Ward, ActivityArea, Activity
from django.utils.translation import ugettext_lazy as _


class AdminGeographyapp(admin.ModelAdmin):
	list_display = ('id', 'tole', 'ward','status')

admin.site.register(Geography, AdminGeographyapp)

class AdminDistrict(admin.ModelAdmin):
	list_display = ('id', 'name','status')

admin.site.register(District, AdminDistrict)


class AdminMunicipality(admin.ModelAdmin):
	list_display = ('id', 'district', 'name','category','status')

admin.site.register(Municipality, AdminMunicipality)


class AdminWard(admin.ModelAdmin):
	list_display = ('id', 'municipality', 'ward','status','name')

admin.site.register(Ward, AdminWard)

class AdminActivity(admin.ModelAdmin):
	list_display = ('id', 'name')

admin.site.register(Activity, AdminActivity)


class AdminActivityArea(admin.ModelAdmin):
	list_display = ('id', 'activity', 'area','status')

admin.site.register(ActivityArea, AdminActivityArea)




# class AdminAppUser(admin.ModelAdmin):
# 	list_display = ('id', 'username','first_name','middle_name','last_name')

# admin.site.register(AppUser,AdminAppUser)
