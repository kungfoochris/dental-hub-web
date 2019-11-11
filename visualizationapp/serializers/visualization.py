from django.contrib.auth.models import Group, Permission

from rest_framework import serializers


from visualizationapp.models import Visualization

class DataVisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = '__all__'
