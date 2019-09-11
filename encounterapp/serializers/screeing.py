from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Screeing


class PatientScreeingSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = Screeing
		fields = ('uid','id','caries_risk','primary_teeth','permanent_teeth','postiror_teeth',\
			'anterior_teeth','need_sealant','reversible_pulpitis','art','extraction',\
			'need_sdf','encounter_id','active_infection','high_blood_pressure',\
			'low_blood_pressure','thyroid','updated_by','updated_at')