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

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','first_name', 'middle_name','last_name','full_name', 'image')
		# read_only_fields = ('notification_count','qrcode')


class UpdateUserSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(required=True)
	class Meta:
		model = User
		fields = ('image',)


		
class PasswordChangeSerializer(serializers.ModelSerializer):
	old_password = serializers.CharField(required=True,write_only=True)
	new_password = serializers.CharField(required=True,write_only=True)
	confirm_password = serializers.CharField(required=True,write_only=True)
	class Meta:
		model = User
		fields = ('old_password','new_password','confirm_password')

class CheckUSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(write_only=True)
	class Meta:
		model = User
		fields = ('email',)