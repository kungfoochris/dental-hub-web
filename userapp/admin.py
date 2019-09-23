from django.contrib import admin

# Register your models here.
from userapp.models import User , CustomUser, Role
from django.utils.translation import ugettext_lazy as _

class AdminUserapp(admin.ModelAdmin):
	list_display = ('id', 'email', 'username','first_name', 'middle_name','last_name' ,'active', 'admin')
	fieldsets = (
	(_("Personal info"),{'fields':('username', 'first_name', 'middle_name','last_name', 'image','active')}),
	)
	readonly_fields = ('password',)
	search_fields = ('username', )

admin.site.register(User, AdminUserapp)




class AdminRole(admin.ModelAdmin):
	list_display = ('id', 'name')

admin.site.register(Role,AdminRole)
