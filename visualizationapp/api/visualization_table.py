import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from patientapp.models import Patient

from rest_framework import filters
from userapp.models import User, CustomUser
import os
from django.http import JsonResponse
from treatmentapp.models import Treatment
from encounterapp.models import Screeing,Encounter,Refer

from nepali.datetime import NepaliDate
from django.db.models import DurationField, F, ExpressionWrapper
import datetime
from django.db.models import Q
from django.db.models import Count


from encounterapp.models import Encounter,History,Refer,Screeing
from treatmentapp.models import Treatment
from patientapp.models import Patient
from visualizationapp.models import Visualization

from nepali.datetime import NepaliDate
import datetime
today = NepaliDate()



	#
	# 	self.age=age




class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class TableVisualization(APIView):
	permission_classes = (IsPostOrIsAuthenticated,)
	def get(self, request,format=None):
		if User.objects.filter(id=request.user.id,admin=True).exists():
			encounter_obj = Encounter.objects.all()
			for en in encounter_obj:
				if History.objects.filter(encounter_id__id=en.id) and Screeing.objects.filter(encounter_id__id=en.id) and Treatment.objects.filter(encounter_id__id=en.id) and Refer.objects.filter(encounter_id__id=en.id):
					history_obj = History.objects.get(encounter_id__id=en.id)
					screeing_obj = Screeing.objects.get(encounter_id__id=en.id)
					treatment_obj = Treatment.objects.get(encounter_id__id=en.id)
					refer_obj = Refer.objects.get(encounter_id__id=en.id)
					dob = en.patient.dob
					if Visualization.objects.filter(patiend_id=en.patient.id,encounter_id=en.id).count()==0:
						visualization_obj=Visualization()
						visualization_obj.patiend_id = en.patient.id
						visualization_obj.encounter_id = en.id
						visualization_obj.age = today.npYear() - dob.year - ((today.npMonth(), today.npDay()) < (dob.month, dob.day))
						visualization_obj.gender = en.patient.gender
						visualization_obj.activities_id = en.activity_area.id
						visualization_obj.geography_id = en.geography.id
						visualization_obj.created_at = en.patient.created_at
						if Treatment.objects.filter(Q(tooth11='EXO') | Q(tooth12='EXO')|Q(tooth13='EXO') | Q(tooth14='EXO')|Q(tooth15='EXO') | Q(tooth16='EXO')|Q(tooth17='EXO') | Q(tooth18='EXO')\
							|Q(tooth21='EXO') | Q(tooth22='EXO')|Q(tooth23='EXO') | Q(tooth24='EXO')|Q(tooth25='EXO') | Q(tooth26='EXO')|Q(tooth27='EXO') | Q(tooth28='EXO')\
							|Q(tooth31='EXO') | Q(tooth32='EXO')|Q(tooth33='EXO') | Q(tooth34='EXO')|Q(tooth35='EXO') | Q(tooth36='EXO')|Q(tooth37='EXO') | Q(tooth38='EXO')\
		                    |Q(tooth41='EXO') | Q(tooth42='EXO')|Q(tooth43='EXO') | Q(tooth44='EXO')|Q(tooth45='EXO') | Q(tooth46='EXO')|Q(tooth47='EXO') | Q(tooth48='EXO')\
		                    |Q(tooth51='EXO') | Q(tooth52='EXO')|Q(tooth53='EXO') | Q(tooth54='EXO')|Q(tooth55='EXO')\
		                    |Q(tooth61='EXO') | Q(tooth62='EXO')|Q(tooth63='EXO') | Q(tooth64='EXO')|Q(tooth65='EXO')\
		                    |Q(tooth71='EXO') | Q(tooth72='EXO')|Q(tooth73='EXO') | Q(tooth74='EXO')|Q(tooth75='EXO')\
		                    |Q(tooth81='EXO') | Q(tooth82='EXO')|Q(tooth83='EXO') | Q(tooth84='EXO')|Q(tooth85='EXO')).filter(encounter_id__id=en.id).count()==1:
							visualization_obj.ext = True
						if Treatment.objects.filter(Q(tooth11='SDF') | Q(tooth12='SDF')|Q(tooth13='SDF') | Q(tooth14='SDF')|Q(tooth15='SDF') | Q(tooth16='SDF')|Q(tooth17='SDF') | Q(tooth18='SDF')\
		                    |Q(tooth21='SDF') | Q(tooth22='SDF')|Q(tooth23='SDF') | Q(tooth24='SDF')|Q(tooth25='SDF') | Q(tooth26='SDF')|Q(tooth27='SDF') | Q(tooth28='SDF')\
		                    |Q(tooth31='SDF') | Q(tooth32='SDF')|Q(tooth33='SDF') | Q(tooth34='SDF')|Q(tooth35='SDF') | Q(tooth36='SDF')|Q(tooth37='SDF') | Q(tooth38='SDF')\
		                    |Q(tooth41='SDF') | Q(tooth42='SDF')|Q(tooth43='SDF') | Q(tooth44='SDF')|Q(tooth45='SDF') | Q(tooth46='SDF')|Q(tooth47='SDF') | Q(tooth48='SDF')\
		                    |Q(tooth51='SDF') | Q(tooth52='SDF')|Q(tooth53='SDF') | Q(tooth54='SDF')|Q(tooth55='SDF')\
		                    |Q(tooth61='SDF') | Q(tooth62='SDF')|Q(tooth63='SDF') | Q(tooth64='SDF')|Q(tooth65='SDF')\
		                    |Q(tooth71='SDF') | Q(tooth72='SDF')|Q(tooth73='SDF') | Q(tooth74='SDF')|Q(tooth75='SDF')\
		                    |Q(tooth81='SDF') | Q(tooth82='SDF')|Q(tooth83='SDF') | Q(tooth84='SDF')|Q(tooth85='SDF')).filter(encounter_id__id=en.id).count()==1:
							visualization_obj.sdf = True
						if Treatment.objects.filter(Q(tooth11='SEAl') | Q(tooth12='SEAL')|Q(tooth13='SEAL') | Q(tooth14='SEAL')|Q(tooth15='SEAL') | Q(tooth16='SEAL')|Q(tooth17='SEAL') | Q(tooth18='SEAL')\
		                    |Q(tooth21='SEAL') | Q(tooth22='SEAL')|Q(tooth23='SEAL') | Q(tooth24='SEAL')|Q(tooth25='SEAL') | Q(tooth26='SEAL')|Q(tooth27='SEAL') | Q(tooth28='SEAL')\
		                    |Q(tooth31='SEAL') | Q(tooth32='SEAL')|Q(tooth33='SEAL') | Q(tooth34='SEAL')|Q(tooth35='SEAL') | Q(tooth36='SEAL')|Q(tooth37='SEAL') | Q(tooth38='SEAL')\
		                    |Q(tooth41='SEAL') | Q(tooth42='SEAL')|Q(tooth43='SEAL') | Q(tooth44='SEAL')|Q(tooth45='SEAL') | Q(tooth46='SEAL')|Q(tooth47='SEAL') | Q(tooth48='SEAL')\
		                    |Q(tooth51='SEAL') | Q(tooth52='SEAL')|Q(tooth53='SEAL') | Q(tooth54='SEAL')|Q(tooth55='SEAL')\
		                    |Q(tooth61='SEAL') | Q(tooth62='SEAL')|Q(tooth63='SEAL') | Q(tooth64='SEAL')|Q(tooth65='SEAL')\
		                    |Q(tooth71='SEAL') | Q(tooth72='SEAL')|Q(tooth73='SEAL') | Q(tooth74='SEAL')|Q(tooth75='SEAL')\
		                    |Q(tooth81='SEAL') | Q(tooth82='SEAL')|Q(tooth83='SEAL') | Q(tooth84='SEAL')|Q(tooth85='SEAL')).filter(encounter_id__id=en.id).count()==1:
							visualization_obj.seal = True
						if Treatment.objects.filter(Q(tooth11='ART') | Q(tooth12='ART')|Q(tooth13='ART') | Q(tooth14='ART')|Q(tooth15='ART') | Q(tooth16='ART')|Q(tooth17='ART') | Q(tooth18='ART')\
		                    |Q(tooth21='ART') | Q(tooth22='ART')|Q(tooth23='ART') | Q(tooth24='ART')|Q(tooth25='ART') | Q(tooth26='ART')|Q(tooth27='ART') | Q(tooth28='ART')\
		                    |Q(tooth31='ART') | Q(tooth32='ART')|Q(tooth33='ART') | Q(tooth34='ART')|Q(tooth35='ART') | Q(tooth36='ART')|Q(tooth37='ART') | Q(tooth38='ART')\
		                    |Q(tooth41='ART') | Q(tooth42='ART')|Q(tooth43='ART') | Q(tooth44='ART')|Q(tooth45='ART') | Q(tooth46='ART')|Q(tooth47='ART') | Q(tooth48='ART')\
		                    |Q(tooth51='ART') | Q(tooth52='ART')|Q(tooth53='ART') | Q(tooth54='ART')|Q(tooth55='ART')\
		                    |Q(tooth61='ART') | Q(tooth62='ART')|Q(tooth63='ART') | Q(tooth64='ART')|Q(tooth65='ART')\
		                    |Q(tooth71='ART') | Q(tooth72='ART')|Q(tooth73='ART') | Q(tooth74='ART')|Q(tooth75='ART')\
		                    |Q(tooth81='ART') | Q(tooth82='ART')|Q(tooth83='ART') | Q(tooth84='ART')|Q(tooth85='ART')).filter(encounter_id__id=en.id).count()==1:
							visualization_obj.art = True
						visualization_obj.fv = treatment_obj.fv_applied
						visualization_obj.refer_hp = refer_obj.health_post
						visualization_obj.refer_hyg = refer_obj.hygienist
						visualization_obj.refer_dent = refer_obj.general_physician
						visualization_obj.refer_dr = refer_obj.dentist
						if Refer.objects.filter(encounter_id__id=en.id).values('other').annotate(Count('other')).count()==1:
							visualization_obj.refer_other = True
						visualization_obj.carries_risk=screeing_obj.carries_risk
						visualization_obj.decayed_primary_teeth=True
						visualization_obj.decayed_permanent_teeth=True
						visualization_obj.cavity_permanent_posterior_teeth=screeing_obj.cavity_permanent_posterior_teeth
						visualization_obj.cavity_permanent_anterior_teeth=screeing_obj.cavity_permanent_anterior_teeth
						visualization_obj.active_infection=screeing_obj.active_infection
						visualization_obj.reversible_pulpitis = screeing_obj.reversible_pulpitis
						visualization_obj.need_art_filling = screeing_obj.need_art_filling
						visualization_obj.need_extraction = screeing_obj.need_extraction
						visualization_obj.need_sdf = screeing_obj.need_sdf
						visualization_obj.save()
			# return Response({"message":"data is added to the visualization table"},status=200)
		return Response({"message":"onky admin can"},status=400)
