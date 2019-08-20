from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Refer,Encounter
from patientapp.models import Patient


class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = ('full_name','gender', 'dob', 'age', 'phone',)

class Recall(serializers.ModelSerializer):
	class Meta:
		model = Refer
		fields = ('time','date')


class RecallSerializer(serializers.ModelSerializer):
	patient = PatientSerializer()
	refer = Recall()
	class Meta:
		model = Encounter
		fields = ('id','patient','refer')