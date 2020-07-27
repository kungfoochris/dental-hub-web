from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from encounterapp.models.modifydelete import ModifyDelete
from encounterapp.serializers.modifydelete import ModifyDeleteSerializer,EncounterAdminStatusSerializer,ModifyDeleteListSerializer
from datetime import datetime


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
    	return request.user and request.user.is_authenticated


class ModifyDeleteDetail(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = ModifyDeleteSerializer

    def get(self,request):
        modify_delete_obj = ModifyDelete.objects.all()
        serializer = ModifyDeleteListSerializer(modify_delete_obj,many=True,context={"request":request})
        return Response(serializer.data,status=200)

    def post(self,request):
        serializer = ModifyDeleteSerializer(data=request.data)
        if serializer.is_valid():
            modify_delete_obj = ModifyDelete()
            modify_delete_obj.author=request.user
            modify_delete_obj.encounter = serializer.validated_data['encounter']
            mod_obj = ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='modify')
            modify_delete_obj.flag = serializer.validated_data['flag']
            if serializer.validated_data['flag'] == "modify":
                if ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='delete'):
                    return Response("You have sent delete request so you cannot send modify request.",status=400)
                if mod_obj:
                    mod = ModifyDelete.objects.get(encounter__id =serializer.validated_data['encounter'].id,flag='modify')
                    if mod.modify_status != "modified" or mod.modify_status != "expired":
                        return Response("You cannot send modify request before you response to previous request.",status=400)
                modify_delete_obj.reason_for_modification = serializer.validated_data['reason_for_modification']
                modify_delete_obj.modify_status = "pending"

            del_obj = ModifyDelete.objects.filter(flag='delete',encounter__id =serializer.validated_data['encounter'].id)
            if serializer.validated_data['flag'] == "delete":
                if del_obj:
                    return Response("You already have a delete request sent for this encounter.")
                if serializer.validated_data['reason_for_deletion'] == "other" and serializer.validated_data['other_reason_for_deletion'] =="":
                    return Response("You should enter the field either reason for deletion or other reason for deletion.")
                if serializer.validated_data['reason_for_deletion'] == "other":
                    modify_delete_obj.reason_for_deletion = serializer.validated_data['reason_for_deletion']
                    modify_delete_obj.other_reason_for_deletion = serializer.validated_data['other_reason_for_deletion']
                else:
                    modify_delete_obj.reason_for_deletion = serializer.validated_data['reason_for_deletion']
                modify_delete_obj.delete_status = 'pending'
            modify_delete_obj.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)


class EncounterAdminStatus(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = EncounterAdminStatusSerializer

    def get(self,request,id):
        mod_obj = ModifyDelete.objects.get(id=id)
        serializer = ModifyDeleteSerializer(mod_obj,context={"request":request})
        return Response(serializer.data,status=200)

    def put(self,request,id):
        mod_obj = ModifyDelete.objects.get(id=id)
        serializer = EncounterAdminStatusSerializer(mod_obj,data=request.data,context={'request': request},partial=True)
        if request.user.admin:
            if serializer.is_valid():
                if mod_obj.delete_status == 'pending' and serializer.validated_data['delete_status'] == 'deleted':
                    mod_obj.delete_status = 'deleted'
                    mod_obj.save()
                    return Response("Encounter deleted successfully.", status=200)
                if serializer.validated_data['modify_status'] == 'approved':
                    mod_obj.modify_approved_at = datetime.now()
                mod_obj.modify_status = serializer.validated_data['modify_status']
                mod_obj.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response("Only admin can change status.", status=401)
