from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Screeing


class PatientScreeingSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Screeing
		fields = ('uid','id','caries_risk','primary_teeth','permanent_teeth','postiror_teeth',\
			'anterior_teeth','need_sealant','reversible_pulpitis','art','extraction',\
			'need_sdf','encounter_id','active_infection','blood_pressure')