from django.contrib import admin

# Register your models here.
from addressapp.models import Geography
from django.utils.translation import ugettext_lazy as _

class AdminGeographyapp(admin.ModelAdmin):
	list_display = ('id', 'district', 'municipality','tole', 'ward','status')

admin.site.register(Geography, AdminGeographyapp)




# class AdminAppUser(admin.ModelAdmin):
# 	list_display = ('id', 'username','first_name','middle_name','last_name')

# admin.site.register(AppUser,AdminAppUser)
