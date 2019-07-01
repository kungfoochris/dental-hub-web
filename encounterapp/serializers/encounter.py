from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Encounter 
from encounterapp.serializers.history import PatientHistorySerializer
from encounterapp.serializers.refer import PatientReferSerializer
from encounterapp.serializers.screeing import PatientScreeingSerializer    

class EncounterSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False,read_only=True)
    patient = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
    class Meta:
        model = Encounter
        fields = ('id', 'date', 'author','encounter_type','patient')

class AllEncounterSerializer(serializers.ModelSerializer):
	author = serializers.StringRelatedField(many=False,read_only=True)
	patient = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	history = PatientHistorySerializer(read_only=True,many=True)
	screeing = PatientScreeingSerializer(read_only=True,many=True)
	refer = PatientReferSerializer(read_only=True,many=True)
	class Meta:
		model = Encounter
		fields = ('id','patient','author','date','encounter_type','history','screeing','refer')