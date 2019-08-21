from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from userapp.models import User, Role, CustomUser
from addressapp.models import Geography, Ward
from addressapp.serializers.address import GeoSerializer

class LocationPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
    	queryset = Ward.objects.all()
    	return queryset


class AreaPKField(serializers.StringRelatedField):
    def get_queryset(self):
    	queryset = Ward.objects.all()
    	return queryset


class GeographySerializeronly(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ('id','location')
        read_only_fields = ('location',)

class RolePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
    	queryset = Role.objects.all()
    	return queryset

class UserSerializer(serializers.HyperlinkedModelSerializer):
	area = LocationPKField(many=True,write_only=True)
	location = GeographySerializeronly(read_only=True,many=True)
	password = serializers.CharField(max_length=250,write_only=True,min_length=8)
	role = RolePKField(many=False)
	class Meta:
		model = CustomUser
		fields = ('id','first_name', 'middle_name', 'last_name', 'username', 'active',
			'staff', 'admin','full_name','password', 'role','location','area')
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
	location=GeoSerializer(many=True)
	class Meta:
		model = CustomUser
		fields = ('id','first_name', 'middle_name','last_name','full_name', 'image','location')
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

class WardSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username',)


class UpdateUserDataSerializer(serializers.ModelSerializer):
	area = LocationPKField(many=True,write_only=True)
	location = AreaPKField(many=True,read_only=True)
	class Meta:
		model = CustomUser
		fields = ('first_name','last_name','middle_name','username','location','area')

class UserStatusSerializer(serializers.ModelSerializer):
	status_obj=serializers.CharField(max_length=7,write_only=True,required=True)
	class Meta:
		model = CustomUser
		fields = ('status_obj',)

class AdminPasswordResetSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=50,write_only=True,required=True)
	new_password = serializers.CharField(max_length=50,write_only=True,required=True)
	confirm_password = serializers.CharField(max_length=50,write_only=True,required=True)
	class Meta:
		model = CustomUser
		fields = ("username","new_password","confirm_password")
