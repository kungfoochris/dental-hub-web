from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from addressapp.models import Geography, Ward


# class GeographySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Geography
#         fields = ('id','district', 'municipality','ward','tole','location')




class WardPKField(serializers.PrimaryKeyRelatedField):
	def get_queryset(self):
		queryset = Ward.objects.filter(status=True)
		return queryset

class GeographySerializer(serializers.ModelSerializer):
	ward = WardPKField(many=False)
	class Meta:
		model = Geography
		fields = ('id','district','municipality','ward','ward_number','tole','status','location')
		read_only_fields = ('status',)

