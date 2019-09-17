from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from treatmentapp.models import Treatment


class PatientTreatmentSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	updated_by = serializers.StringRelatedField()
	class Meta:
		model = Treatment
		fields = ('id','tooth18','tooth17','tooth16','tooth15',\
			'tooth14','tooth13','tooth12','tooth11','tooth21',\
			'tooth22','tooth23','tooth24','tooth25','tooth26',\
			'tooth27','tooth28','tooth48','tooth47',\
			'tooth46','tooth45','tooth44','tooth43','tooth42',\
			'tooth41','tooth31','tooth32','tooth33',\
			'tooth34','tooth35','tooth36','tooth37','tooth38',\
			'tooth55','tooth54','tooth53','tooth52',\
			'tooth51','tooth61','tooth62','tooth63',\
			'tooth64','tooth65','tooth85','tooth84',\
			'tooth83','tooth82','tooth81','tooth71',\
			'tooth72','tooth73','tooth74','tooth75',\
			'sdf_whole_mouth','fv_applied','treatment_plan_complete',\
			'notes','encounter_id','updated_by','updated_at','created_at')
