from django.contrib import admin

# Register your models here.
from patientapp.models import Patient
from django.utils.translation import ugettext_lazy as _

class PatientAdmin(admin.ModelAdmin):
	list_display = ('uid', 'first_name', 'last_name', 'dob','phone','author','date','activity_area','geography','ward')
	list_filter = ('date',)
	search_fields = ['first_name','author__username','date']
admin.site.register(Patient,PatientAdmin)