from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from userapp.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'middle_name', 'last_name', 'email', 'active', 
            'staff', 'admin','full_name')
        read_only_fields = ('active','staff','admin','full_name')


class ForgetPasswordSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email',)

class PasswordResetSerializer(serializers.ModelSerializer):
	password = serializers.CharField(required=True)
	confirm_password = serializers.CharField(required=True)
	class Meta:
		model = User
		fields = ('token', 'password','confirm_password')