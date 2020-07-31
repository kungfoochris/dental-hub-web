from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from encounterapp.models import Encounter
from encounterapp.models.modifydelete import ModifyDelete
from patientapp.models.patient import Patient
from userapp.models import User


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

class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'full_name')


class ModifyDeleteListSerializer(serializers.ModelSerializer):
	encounter = EncounterSerializer(read_only=True)
	modify_status = serializers.StringRelatedField()
	delete_status = serializers.StringRelatedField()
	author = AuthorSerializer(read_only=True)
	class Meta:
		model = ModifyDelete
		fields = ('id', 'encounter', 'reason_for_modification', 'modify_status', 'reason_for_deletion','other_reason_for_deletion','delete_status', 'flag','modify_approved_at','modify_expiry_date','restore_expiry_date','author')
		read_only_fields = ('modify_status', 'delete_status', 'modify_approved_at')



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




class EncounterFlagDeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModifyDelete
        fields = ('modify_status',)
