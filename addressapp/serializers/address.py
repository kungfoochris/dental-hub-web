from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from addressapp.models import Address,Ward,Municipality,District

class WardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ward
		fields = ['id','ward']


class MunicipalitySerializer(serializers.ModelSerializer):
	wards = WardSerializer(source='ward_set',many=True, read_only=True)
	class Meta:
		model = Municipality
		fields = ['id','name', 'category', 'wards']

class DistrictSerializer(serializers.ModelSerializer):
	municipalities = MunicipalitySerializer(source='municipality_set',many=True, read_only=True)
	class Meta:
		model = District
		fields = ['id','name','municipalities']

class MunicipalitySerializer1(serializers.ModelSerializer):
	class Meta:
		model = Municipality
		fields = ['name',]


class GeoSerializer(serializers.ModelSerializer):
	municipality = MunicipalitySerializer1(read_only=True)
	class Meta:
		model = Ward
		fields = ['id','district','municipality','ward','location']

# class DistrictSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = District
# 		fields = ('district',)


# class MunicipalitySerializer(serializers.ModelSerializer):
# 	district = DistrictSerializer()
# 	class Meta:
# 		model = Municipality
# 		fields = ('district','municipality','municipality_type')

# class AddressSerializer(serializers.ModelSerializer):
# 	municipality = MunicipalitySerializer()
# 	class Meta:
# 		model = Ward
# 		fields = ('municipality','ward')