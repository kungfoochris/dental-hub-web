from django.contrib.auth.models import Group, Permission

from rest_framework import serializers


from visualizationapp.models import Visualization
from encounterapp.models import Encounter
from addressapp.models import Ward,Activity



class LocationPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = Ward.objects.filter(status=True)
        return queryset

class ActivityPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = Activity.objects.all()
        return queryset

class DataVisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = '__all__'



class OverViewVisualization(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    location = LocationPKField(write_only=True, many=True,allow_null=True)
    # location = serializers.CharField(write_only=True,required=True)
    activities = ActivityPKField(write_only=True,many=True,allow_null=True)
    # health_post = serializers.CharField(allow_null=True,write_only=True)
    # seminar = serializers.CharField(allow_null=True,write_only=True)
    # outreach = serializers.CharField(allow_null=True,write_only=True)
    # training = serializers.CharField(allow_null=True,write_only=True)
    class Meta:
        model = Encounter
        fields = ("start_date","end_date","location","activities")



class TreatMentBarGraphVisualization(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    location = LocationPKField(write_only=True, many=True,allow_null=True)
    # location = serializers.CharField(write_only=True,default="All Location")
    age_group = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = Visualization
        fields = ("start_date","end_date","location",'age_group')

class WardlineVisualizationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    class Meta:
        model = Visualization
        fields = ("start_date",)

class SectionalVisualizationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    reason_for_visit = serializers.CharField(write_only=True,required=True)
    referral_type = serializers.CharField(write_only=True,required=True)
    health_post = serializers.CharField(allow_null=True,write_only=True)
    seminar = serializers.CharField(allow_null=True,write_only=True)
    outreach = serializers.CharField(allow_null=True,write_only=True)
    training = serializers.CharField(allow_null=True,write_only=True)
    class Meta:
        model = Encounter
        fields = ("start_date","end_date","reason_for_visit",'referral_type',\
        'health_post','seminar','outreach','training')

class LongitudinalVisualizationSerializer(serializers.ModelSerializer):
    frame1_start_date = serializers.DateField(write_only=True,required=True)
    frame1_end_date = serializers.DateField(write_only=True,required=True)
    frame2_start_date = serializers.DateField(write_only=True,required=True)
    frame2_end_date = serializers.DateField(write_only=True,required=True)
    reason_for_visit = serializers.CharField(write_only=True,required=True)
    referral_type = serializers.CharField(write_only=True,required=True)
    health_post = serializers.CharField(allow_null=True,write_only=True)
    seminar = serializers.CharField(allow_null=True,write_only=True)
    outreach = serializers.CharField(allow_null=True,write_only=True)
    training = serializers.CharField(allow_null=True,write_only=True)
    class Meta:
        model = Encounter
        fields = ("frame1_start_date","frame1_end_date","frame2_start_date","frame2_end_date","reason_for_visit",'referral_type',\
        'health_post','seminar','outreach','training')



class TreatmentStrategicDataSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    location = LocationPKField(write_only=True, many=True,allow_null=True)
    # location = serializers.CharField(write_only=True,required=True)
    health_post = serializers.CharField(allow_null=True,write_only=True)
    seminar = serializers.CharField(allow_null=True,write_only=True)
    outreach = serializers.CharField(allow_null=True,write_only=True)
    training = serializers.CharField(allow_null=True,write_only=True)
    class Meta:
        model = Encounter
        fields = ("start_date","end_date","location","health_post",'seminar',\
        'outreach','training')
