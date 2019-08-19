from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from treatmentapp.models import Treatment


class PatientTreatmentSerializer(serializers.ModelSerializer):
	encounter_id = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Treatment
		fields = ('uid','id','teeth1','teeth2','teeth3','teeth4',\
			'teeth5','teeth6','teeth7','teeth8','teeth9',\
			'teeth10','teeth11','teeth12','teeth13','teeth14',\
			'teeth15','teeth16','teeth17','teeth18',\
			'teeth19','teeth20','teeth21','teeth22','teeth23',\
			'teeth24','teeth25','teeth26','teeth27',\
			'teeth28','teeth29','teeth30','teeth31','teeth32',\
			'primary_teeth1','primary_teeth2','primary_teeth3','primary_teeth4',\
			'primary_teeth5','primary_teeth6','primary_teeth7','primary_teeth8',\
			'primary_teeth9','primary_teeth10','primary_teeth11','primary_teeth12',\
			'primary_teeth13','primary_teeth14','primary_teeth15','primary_teeth16',\
			'primary_teeth17','primary_teeth18','primary_teeth19','primary_teeth20',\
			'whole_mouth','fluoride_varnish','treatment_complete','note','encounter_id')
