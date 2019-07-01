from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import History


class PatientHistorySerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = History
		fields = ('id','bleeding','diabete','liver','fever',\
			'seizures','hepatitis','hiv','allergic','other',\
			'medication', 'no_medication', 'encounter_id')