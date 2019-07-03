from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Refer


class PatientReferSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Refer
		fields = ('uid','id','no_referal','health_post','dentist','physician',\
			'hygienist','other','encounter_id')