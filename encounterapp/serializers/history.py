from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import History


class PatientHistorySerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = History
		fields = ('uid','id','bleeding','diabetes','liver','fever',\
			'seizures','hepatitis','hiv','no_allergies','allergies','other',\
			'medication', 'no_medication','no_underlying_medical',\
			'not_taking_medication', 'encounter_id',\
			'updated_by','updated_at')