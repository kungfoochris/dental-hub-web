from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from addressapp.models import ActivityArea


class ActivityAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityArea
        fields = ('id','area','name')