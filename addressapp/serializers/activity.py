from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from addressapp.models import Activity,ActivityArea


class ActivityPKFIeld(serializers.PrimaryKeyRelatedField):
	def get_queryset(self):
		queryset = Activity.objects.all()
		return queryset


class ActivityPKFIeld1(serializers.StringRelatedField):
	def get_queryset(self):
		queryset = Activity.objects.all()
		return queryset


class ActivityAreaSerializer(serializers.ModelSerializer):
	activity_id = ActivityPKFIeld(many=False,write_only=True)
	activity = ActivityPKFIeld1(many=False,read_only=True)
	class Meta:
		model = ActivityArea
		fields = ('id','activity','activity_id','area')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id','name')

# class SchoolSeminarSerializer(serializers.ModelSerializer):
# 	activity_id = ActivityPKFIeld(many=False,write_only=True)
# 	activity = ActivityPKFIeld1(many=False,read_only=True)
# 	class Meta:
# 		model = ActivityArea
# 		fields = ('id','activity','activity_id','area')


# class CommunitySerializer(serializers.ModelSerializer):
# 	activity_id = ActivityPKFIeld(many=False,write_only=True)
# 	activity = ActivityPKFIeld1(many=False,read_only=True)
# 	class Meta:
# 		model = ActivityArea
# 		fields = ('id','activity','activity_id','area')

# class TrainingSerializer(serializers.ModelSerializer):
# 	activity_id = ActivityPKFIeld(many=False,write_only=True)
# 	activity = ActivityPKFIeld1(many=False,read_only=True)
# 	class Meta:
# 		model = ActivityArea
# 		fields = ('id','activity','activity_id','area')


