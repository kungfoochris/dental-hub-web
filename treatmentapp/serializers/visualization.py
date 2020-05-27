from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from patientapp.models import Patient


class VisualizatioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = ('location_visualization',)
