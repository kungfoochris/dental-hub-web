from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Encountertype


class EncountertypeSerializer(serializers.ModelSerializer):
	encounter_id = serializers.CharField(max_length=250,write_only=True,required=True)
	class Meta:
		model = Encountertype
		fields = ('id','encounter_id','screeing','pain', 'check', 'treatment')