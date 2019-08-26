from django.contrib import admin

# Register your models here.
from userapp.models import User , CustomUser
from django.utils.translation import ugettext_lazy as _

class AdminUserapp(admin.ModelAdmin):
	list_display = ('id', 'email', 'username','first_name', 'middle_name','last_name' ,'active', 'admin')
	fieldsets = (
	(_("Personal info"),{'fields':('username', 'first_name', 'middle_name','last_name', 'image','active')}),
	)
	readonly_fields = ('password',)
	search_fields = ('username', )

admin.site.register(User, AdminUserapp)




# class AdminAppUser(admin.ModelAdmin):
# 	list_display = ('id', 'username','first_name','middle_name','last_name')

# admin.site.register(AppUser,AdminAppUser)
