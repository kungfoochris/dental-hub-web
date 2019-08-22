from django.contrib import admin

# Register your models here.
from patientapp.models import Patient
from django.utils.translation import ugettext_lazy as _

class PatientAdmin(admin.ModelAdmin):
	list_display = ('id','uid', 'first_name', 'last_name', 'dob','phone','author','date','activity_area','geography','ward')
admin.site.register(Patient,PatientAdmin)