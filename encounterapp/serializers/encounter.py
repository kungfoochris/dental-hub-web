from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Encounter 
from encounterapp.serializers.history import PatientHistorySerializer
from encounterapp.serializers.refer import PatientReferSerializer
from encounterapp.serializers.screeing import PatientScreeingSerializer
from treatmentapp.serializers.treatment import PatientTreatmentSerializer  

from addressapp.serializers.activity import ActivityAreaSerializer
from addressapp.serializers.geography import GeographySerializer

class EncounterSerializer(serializers.ModelSerializer):
	activity_area = serializers.StringRelatedField(many=False,read_only=True)
	geography = serializers.StringRelatedField(many=False,read_only=True)
	activityarea_id = serializers.CharField(max_length=250,write_only=True,required=True)
	geography_id = serializers.CharField(max_length=250,write_only=True,required=True)
	author = serializers.StringRelatedField(many=False,read_only=True)
	patient = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = Encounter
		fields = ('id','geography_id','activityarea_id','geography',\
			'activity_area', 'date', 'author','encounter_type','patient','other_detail','updated_by','updated_at')
		read_only_fields = ('updated_at',)
		

class AllEncounterSerializer(serializers.ModelSerializer):
	activity_area = serializers.StringRelatedField(many=False,read_only=True)
	geography = serializers.StringRelatedField(many=False,read_only=True)
	author = serializers.StringRelatedField(many=False,read_only=True)
	patient = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	history = PatientHistorySerializer(read_only=True,many=True)
	screeing = PatientScreeingSerializer(read_only=True,many=True)
	refer = PatientReferSerializer(read_only=True,many=True)
	treatment = PatientTreatmentSerializer(read_only=True,many=True)
	class Meta:
		model = Encounter
		fields = ('id','geography','activity_area','patient','author','date','encounter_type', 'other_detail', 'updated_by','updated_at', 'history','screeing','treatment','refer')





class EncounterUpdateSerializer(serializers.ModelSerializer):
	activity_area = serializers.StringRelatedField(many=False,read_only=True)
	geography = serializers.StringRelatedField(many=False,read_only=True)
	author = serializers.StringRelatedField(many=False,read_only=True)
	patient = serializers.StringRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = Encounter
		fields = ('id','geography',\
			'activity_area', 'date', 'author','encounter_type','patient','other_detail','updated_by','updated_at')
