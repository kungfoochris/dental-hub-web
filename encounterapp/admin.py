from django.contrib import admin

# Register your models here.
from encounterapp.models import Encounter, History
from django.utils.translation import ugettext_lazy as _

class EncounterAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'patient', 'encounter_type','author')

admin.site.register(Encounter, EncounterAdmin)



class HistoryAdmin(admin.ModelAdmin):
	list_display = ('id','encounter_id')


admin.site.register(History, HistoryAdmin)
