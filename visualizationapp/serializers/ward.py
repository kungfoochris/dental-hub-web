from django.contrib.auth.models import Group, Permission

from rest_framework import serializers


from visualizationapp.models import Visualization
from encounterapp.models import Encounter
from addressapp.models import Ward,Activity



class ActivityPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = Activity.objects.all()
        return queryset



class WardFilterVisualization(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    activities = ActivityPKField(write_only=True,many=True,allow_null=True)
    class Meta:
        model = Encounter
        fields = ("start_date","end_date","activities")


class ContactAgeGenderVisualization(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    class Meta:
        model = Encounter
        fields = ("start_date","end_date")
