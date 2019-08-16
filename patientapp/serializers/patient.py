from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from patientapp.models import Patient
from addressapp.models import Geography, ActivityArea
from addressapp.serializers.activity import ActivityAreaSerializer
from addressapp.serializers.geography import GeographySerializer


class PatientSerializer(serializers.ModelSerializer):
	activity_area = serializers.StringRelatedField(many=False,read_only=True)
	geography = serializers.StringRelatedField(many=False,read_only=True)
	activityarea_id = serializers.CharField(max_length=250,write_only=True,required=True)
	geography_id = serializers.CharField(max_length=250,write_only=True,required=True)
	class Meta:
		model = Patient
		fields = ('uid','id','geography_id','activityarea_id','first_name', 'middle_name', 'last_name', 'full_name',\
         'gender', 'dob', 'age', 'phone','municipality','district', 'ward', 'author', 'latitude' ,'longitude', 'date','geography','activity_area')
		read_only_fields = ('author','full_name','date','age')