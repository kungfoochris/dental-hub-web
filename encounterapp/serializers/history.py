from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import History


class PatientHistorySerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = History
		fields = ('uid','id','bleeding','diabetes','liver','fever',\
			'seizures','hepatitis','hiv','no_allergies','allergies','other',\
			'medication', 'no_medication','no_underlying_medical','not_taking_medication', 'encounter_id')