from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from patientapp.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id','first_name', 'middle_name', 'last_name', 'full_name',\
         'gender', 'dob', 'phone', 'education', 'city', 'state', 'country',\
         'author', 'latitude' ,'longitude', 'date')
        read_only_fields = ('author','full_name','date')