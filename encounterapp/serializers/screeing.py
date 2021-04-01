from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Screeing


class PatientScreeingSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Screeing
		fields = ('id','carries_risk','decayed_primary_teeth','decayed_permanent_teeth','cavity_permanent_posterior_teeth',\
			'cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis','need_art_filling','need_extraction',\
			'need_sdf','active_infection','soft_issue_finding','need_fv','need_dentist_or_hygienist','encounter_id')


class PatientScreeingUpdateSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Screeing
		fields = ('id','carries_risk','decayed_primary_teeth','decayed_permanent_teeth','cavity_permanent_posterior_teeth',\
			'cavity_permanent_anterior_teeth','need_sealant','reversible_pulpitis','need_art_filling','need_extraction',\
			'need_sdf','active_infection','soft_issue_finding','need_fv','need_dentist_or_hygienist','encounter_id')

