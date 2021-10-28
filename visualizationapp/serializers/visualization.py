from django.contrib.auth.models import Group, Permission

from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from visualizationapp.models import Visualization
from encounterapp.models import Encounter
from addressapp.models import Ward,Activity



REASON_CHOICES = (
    ("Checkup / Screening", _("Checkup / Screening")),
    ("Relief of pain", _("Relief of pain")),
    ("Continuation of treatment plan", _("Continuation of treatment plan")),
    ("Other Problem", _("Other Problem")),
)

REFER_CHOICES = (
    ("Refer Other", _("Refer Other")),
    ("Refer Hp", _("Refer Hp")),
    ("Refer Dent", _("Refer Dent")),
    ("Refer Hyg", _("Refer Hyg")),
    ("Refer Dr", _("Refer Dr")),
)


AGE_CHOICES = (
    ("Child ≤12 Y", _("Child ≤12 Y")),
    ("Teen 13-18 Y", _("Teen 13-18 Y")),
    ("Adult 19-60 Y", _("Adult 19-60 Y")),
    ("Older Adult ≥61 Y", _("Older Adult ≥61 Y")),
    ("6 Y", _("6 Y")),
    ("12 Y", _("12 Y")),
    ("15 Y", _("15 Y")),
)


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


class TestLongitudinalVisualizationSerializer(serializers.ModelSerializer):
    frame1_start_date = serializers.DateField(write_only=True,required=True)
    frame1_end_date = serializers.DateField(write_only=True,required=True)
    frame2_start_date = serializers.DateField(write_only=True,required=True)
    frame2_end_date = serializers.DateField(write_only=True,required=True)

    reason_for_visit = serializers.ChoiceField(choices = REASON_CHOICES,write_only=True)
    referral_type = serializers.ChoiceField(choices = REFER_CHOICES,write_only=True,allow_null=True)
    activity = ActivityPKField(write_only=True, many=True)
    location = LocationPKField(write_only=True, many=True)
    age_group = serializers.ChoiceField(choices = AGE_CHOICES,write_only=True)
    class Meta:
        model = Encounter
        fields = ("frame1_start_date","frame1_end_date","frame2_start_date","frame2_end_date","reason_for_visit",'referral_type',"activity","location","age_group")


class TestCrosssectionVisualizationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True,required=True)
    end_date = serializers.DateField(write_only=True,required=True)
    reason_for_visit = serializers.ChoiceField(choices = REASON_CHOICES,write_only=True)
    referral_type = serializers.ChoiceField(choices = REFER_CHOICES,write_only=True,allow_null=True)
    activity = ActivityPKField(write_only=True, many=True)
    location = LocationPKField(write_only=True, many=True)
    class Meta:
        model = Encounter
        fields = ("start_date","end_date","reason_for_visit",'referral_type',"activity","location")



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
