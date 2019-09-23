from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Encounter 
from encounterapp.serializers.history import PatientHistorySerializer
from encounterapp.serializers.refer import PatientReferSerializer
from encounterapp.serializers.screeing import PatientScreeingSerializer
from treatmentapp.serializers.treatment import PatientTreatmentSerializer  

from addressapp.serializers.activity import ActivityAreaSerializer
from addressapp.serializers.geography import GeographySerializer


from patientapp.serializers.patient import AuthorField

class EncounterSerializer(serializers.ModelSerializer):
	activity_area = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	geography = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	activityarea_id = serializers.CharField(max_length=250,write_only=True,required=True)
	geography_id = serializers.CharField(max_length=250,write_only=True,required=True)
	author = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	patient = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = Encounter
		fields = ('id','geography_id','activityarea_id','geography',\
			'activity_area', 'date', 'author','encounter_type','patient','other_detail','updated_by','updated_at','created_at')
		read_only_fields = ('updated_at',)
		

class AllEncounterSerializer(serializers.ModelSerializer):
	activity_area = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	geography = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	author = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	patient = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	history = PatientHistorySerializer(read_only=True,many=False)
	screening = PatientScreeingSerializer(read_only=True,many=False)
	referral = PatientReferSerializer(read_only=True,many=False)
	treatment = PatientTreatmentSerializer(read_only=True,many=False)
	class Meta:
		model = Encounter
		fields = ('id','geography','activity_area','patient','author','date','encounter_type', 'other_detail', 'created_at', 'updated_by','updated_at', 'history','screening','treatment','referral')





class EncounterUpdateSerializer(serializers.ModelSerializer):
	activity_area = serializers.StringRelatedField(many=False,read_only=True)
	geography = serializers.StringRelatedField(many=False,read_only=True)
	author = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	patient = serializers.StringRelatedField(many=False,read_only=True)
	updated_by = AuthorField(many=False)
	class Meta:
		model = Encounter
		fields = ('id','geography',\
			'activity_area', 'date', 'author','encounter_type','patient','other_detail','updated_by','updated_at')
