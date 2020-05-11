from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from flagapp.models import Flag



class FlagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flag
		fields = ('id', 'reason', 'other', 'content_type', 'object_id',\
		'created_at', 'status')
		read_only_fields = ('status',)


class FlagUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flag
		fields = ('id', 'status','updated_at')
