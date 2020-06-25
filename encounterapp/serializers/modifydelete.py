from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Encounter
from encounterapp.models.modifydelete import ModifyDelete
from patientapp.models.patient import Patient


class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = ('id','full_name',)

class EncounterSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = Encounter
        fields = ('id', 'encounter_type','patient')

class EncounterPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        query = Encounter.objects.all()
        return query


class ModifyDeleteListSerializer(serializers.ModelSerializer):
    encounter = EncounterSerializer(read_only=True)
    modify_status = serializers.StringRelatedField()
    delete_status = serializers.StringRelatedField()
    class Meta:
        model = ModifyDelete
        fields = ('id', 'encounter', 'reason_for_modification', 'modify_status', 'reason_for_deletion','other_reason_for_deletion','delete_status', 'flag','modify_approved_at')
        read_only_fields = ('modify_status','delete_status','modify_approved_at')



class ModifyDeleteSerializer(serializers.ModelSerializer):
    encounter = EncounterPKField(many=False)
    modify_status = serializers.StringRelatedField()
    delete_status = serializers.StringRelatedField()
    class Meta:
        model = ModifyDelete
        fields = ('id', 'encounter', 'reason_for_modification', 'modify_status', 'reason_for_deletion','other_reason_for_deletion','delete_status', 'flag','modify_approved_at')
        read_only_fields = ('modify_status','delete_status','modify_approved_at')



class EncounterAdminStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModifyDelete
        fields = ('id','modify_status','delete_status')

