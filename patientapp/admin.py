from django.contrib import admin

# Register your models here.
from patientapp.models import Patient
from django.utils.translation import ugettext_lazy as _

class PatientAdmin(admin.ModelAdmin):
	pass
admin.site.register(Patient,PatientAdmin)