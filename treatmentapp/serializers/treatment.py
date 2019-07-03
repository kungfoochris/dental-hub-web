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
			'fluoride_varnish','treatment_complete','note','encounter_id')
