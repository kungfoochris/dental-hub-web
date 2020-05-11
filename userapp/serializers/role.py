from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from userapp.models import User, Role




class RoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Role
		fields = ('id','name')