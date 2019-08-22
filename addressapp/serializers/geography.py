from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from addressapp.models import Geography


class GeographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Geography
        fields = ('id','district', 'municipality','ward','tole','location')