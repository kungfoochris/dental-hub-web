from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Refer


class PatientReferSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Refer
		fields = ('id','no_referal','health_post','dentist','general_physician',\
			'hygienist','other','encounter_id')
		read_only_fields = ('updated_at',)


class PatientReferUpdateSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Refer
		fields = ('id','no_referal','health_post','dentist','general_physician',\
			'hygienist','other','encounter_id')