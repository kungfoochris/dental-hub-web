from django.contrib import admin

# Register your models here.
from userapp.models import User , CustomUser, Role
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token

class AdminUserapp(admin.ModelAdmin):
	list_display = ('id', 'email', 'username','first_name', 'middle_name','last_name' ,'active', 'admin')
	fieldsets = ((_("Personal info"),{'fields':('username', 'first_name', 'middle_name','last_name','password', 'image','role','location','active')}),)
	# readonly_fields = ('password',)
	search_fields = ('username', )

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

admin.site.register(CustomUser, AdminUserapp)

class AdminRole(admin.ModelAdmin):
	list_display = ('id', 'name')

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

admin.site.unregister(Group)

admin.site.unregister(Token)

admin.site.register(Role,AdminRole)
