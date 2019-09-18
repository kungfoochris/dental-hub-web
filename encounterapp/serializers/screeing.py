from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Screeing


class PatientScreeingSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = Screeing
		fields = ('id','caries_risk','decayed_primary_teeth','decayed_permanent_teeth','cavity_permanent_postiror_teeth',\
			'cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis','need_art_filling','need_extraction',\
			'need_sdf','encounter_id','active_infection','high_blood_pressure',\
			'low_blood_pressure','thyroid_disorder','updated_by','updated_at','created_at')
		read_only_fields = ('updated_at',)


class PatientScreeingUpdateSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = Screeing
		fields = ('id','caries_risk','decayed_primary_teeth','decayed_permanent_teeth','cavity_permanent_postiror_teeth',\
			'cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis','need_art_filling','need_extraction',\
			'need_sdf','encounter_id','active_infection','high_blood_pressure',\
			'low_blood_pressure','thyroid_disorder','updated_by','updated_at','created_at')
		read_only_fields = ('created_at',)