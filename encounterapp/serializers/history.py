from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import History


class PatientHistorySerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = History
		fields = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever',\
			'epilepsy_or_seizures','hepatitis_b_or_c','hiv','no_allergies','allergies','other',\
			'medications', 'no_medications','no_underlying_medical_condition',\
			'not_taking_any_medications', 'encounter_id',\
			'updated_by','updated_at','created_at')
		read_only_fields = ('updated_at',)


class PatientHistoryUpdateSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = History
		fields = ('id','blood_disorder','diabetes','liver_problem','rheumatic_fever',\
			'epilepsy_or_seizures','hepatitis_b_or_c','hiv','no_allergies','allergies','other',\
			'medications', 'no_medications','no_underlying_medical_condition',\
			'not_taking_any_medications', 'encounter_id',\
			'updated_by','updated_at','created_at')
		read_only_fields = ('created_at',)