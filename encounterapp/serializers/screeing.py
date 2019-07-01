from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Screeing


class PatientScreeingSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Screeing
		fields = ('id','caries_risk','primary_teeth','permanent_teeth','postiror_teeth',\
			'anterior_teeth','infection','reversible_pulpitis','art','extraction',\
			'refernal_kdh','encounter_id')