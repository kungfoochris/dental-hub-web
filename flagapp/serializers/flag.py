from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from flagapp.models import Flag

from django.contrib.contenttypes.models import ContentType

from userapp.models import User




class FlagAuthor(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'username')


class ContentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContentType
		fields = ('id','app_label','model')


class AllFlagSerializer(serializers.ModelSerializer):
	content_type = ContentTypeSerializer(read_only=True)
	author = FlagAuthor(read_only=True)
	class Meta:
		model = Flag
		fields = ('id', 'reason', 'other', 'content_type', 'object_id',\
		'created_at', 'status', 'author', 'patient_name')
		read_only_fields = ('status',)


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
