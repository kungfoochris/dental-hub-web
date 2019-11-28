from django.contrib import admin

# Register your models here.
from visualizationapp.models import Visualization
from django.utils.translation import ugettext_lazy as _

class AdminVisualization(admin.ModelAdmin):
    list_display = ('id', 'patiend_id', 'encounter_id','activities_id', 'geography_id')
admin.site.register(Visualization, AdminVisualization)
