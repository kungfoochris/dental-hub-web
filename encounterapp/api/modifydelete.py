from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from encounterapp.models.modifydelete import ModifyDelete
from encounterapp.models.encounter import Encounter
from encounterapp.serializers.encounter import AllEncounterSerializer
from encounterapp.serializers.modifydelete import ModifyDeleteSerializer,EncounterAdminStatusSerializer,ModifyDeleteListSerializer,EncounterFlagDeadSerializer
from datetime import datetime, timedelta




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
            encounter_obj = Encounter.objects.filter(id = serializer.validated_data['encounter'].id)
            if encounter_obj:
                encounter_obj = Encounter.objects.get(id = serializer.validated_data['encounter'].id)
                if encounter_obj.active == False:
                    return Response("This encounter has already been deleted.",status=400)
                if encounter_obj.request_counter >=3:
                    return Response("You already have requested 3 times for modify or delete for this counter.",status=400) 
                if ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='delete') or ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='modify'):
                    return Response("You already have a request sent.",status=400)
                if serializer.validated_data['flag'] == "modify":
                    if serializer.validated_data['reason_for_modification'] == "":
                        return Response("Please enter reason for modification",status=400)
                    modify_delete_obj.reason_for_modification = serializer.validated_data['reason_for_modification']
                    modify_delete_obj.modify_status = "pending"

                if serializer.validated_data['flag'] == "delete":
                    if serializer.validated_data['reason_for_deletion'] == "other" and serializer.validated_data['other_reason_for_deletion'] =="":
                        return Response("You should enter the field either reason for deletion or other reason for deletion.",status=400)
                    if serializer.validated_data['reason_for_deletion'] == "other":
                        modify_delete_obj.other_reason_for_deletion = serializer.validated_data['other_reason_for_deletion']
                    modify_delete_obj.reason_for_deletion = serializer.validated_data['reason_for_deletion']
                    modify_delete_obj.delete_status = 'pending'
                modify_delete_obj.author = request.user
                modify_delete_obj.encounter = serializer.validated_data['encounter']
                modify_delete_obj.flag = serializer.validated_data['flag']
                modify_delete_obj.save()
                return Response(serializer.data,status=200)
            return Response("Encounter doesn't exists.",status=400)
        return Response(serializer.errors,status=400)

    # def post(self,request):
    #     serializer = ModifyDeleteSerializer(data=request.data)
    #     if serializer.is_valid():
    #         modify_delete_obj = ModifyDelete()
    #         modify_delete_obj.author=request.user
    #         modify_delete_obj.encounter = serializer.validated_data['encounter']
    #         mod_obj = ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='modify')
    #         modify_delete_obj.flag = serializer.validated_data['flag']
    #         if serializer.validated_data['flag'] == "modify":
    #             if ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='delete'):
    #                 return Response("You have sent delete request so you cannot send modify request.",status=400)
    #             if mod_obj:
    #                 mod = ModifyDelete.objects.get(encounter__id =serializer.validated_data['encounter'].id,flag='modify')
    #                 if mod.modify_status != "modified" or mod.modify_status != "expired":
    #                     return Response("You cannot send modify request before you response to previous request.",status=400)
    #             modify_delete_obj.reason_for_modification = serializer.validated_data['reason_for_modification']
    #             modify_delete_obj.modify_status = "pending"

    #         del_obj = ModifyDelete.objects.filter(flag='delete',encounter__id =serializer.validated_data['encounter'].id)
    #         if serializer.validated_data['flag'] == "delete":
    #             if del_obj:
    #                 return Response("You already have a delete request sent for this encounter.",status=400)
    #             if serializer.validated_data['reason_for_deletion'] == "other" and serializer.validated_data['other_reason_for_deletion'] =="":
    #                 return Response("You should enter the field either reason for deletion or other reason for deletion.",status=400)
    #             if serializer.validated_data['reason_for_deletion'] == "other":
    #                 modify_delete_obj.reason_for_deletion = serializer.validated_data['reason_for_deletion']
    #                 modify_delete_obj.other_reason_for_deletion = serializer.validated_data['other_reason_for_deletion']
    #             else:
    #                 modify_delete_obj.reason_for_deletion = serializer.validated_data['reason_for_deletion']
    #             modify_delete_obj.delete_status = 'pending'
    #         modify_delete_obj.save()
    #         return Response(serializer.data,status=200)
    #     return Response(serializer.errors,status=400)


class EncounterAdminStatus(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = EncounterAdminStatusSerializer

    def get(self,request,id):
        mod_obj = ModifyDelete.objects.get(id=id)
        serializer = ModifyDeleteListSerializer(mod_obj,context={"request":request})
        return Response(serializer.data,status=200)

    def put(self,request,id):
        mod_obj = ModifyDelete.objects.get(id=id)
        serializer = EncounterAdminStatusSerializer(mod_obj,data=request.data,context={'request': request},partial=True)
        if request.user.admin:
            if serializer.is_valid():
                if mod_obj.delete_status == 'pending' and serializer.validated_data['delete_status'] == 'deleted':
                    mod_obj.delete_status = 'deleted'
                    mod_obj.deleted_at = datetime.now()
                    mod_obj.restore_expiry_date = datetime.now()+timedelta(days=30)
                    mod_obj.save()

                    encounter_obj = Encounter.objects.get(id=mod_obj.encounter.id)
                    encounter_obj.active = False
                    encounter_obj.request_counter  += 1
                    encounter_obj.save()
                    return Response("Encounter deleted successfully.", status=200)
                if mod_obj.modify_status == 'pending':
                    if serializer.validated_data['modify_status'] == 'approved':
                        mod_obj.modify_approved_at = datetime.now()
                        mod_obj.modify_expiry_date = datetime.now()+timedelta(minutes=1)
                        mod_obj.modify_status = 'approved'
                        mod_obj.save()

                        encounter_obj = Encounter.objects.get(id=mod_obj.encounter.id)
                        encounter_obj.request_counter  += 1
                        encounter_obj.save()
                        return Response("Modification request approved.", status=200)
                    if serializer.validated_data['modify_status'] == 'rejected':
                        mod_obj.modify_status = 'rejected'
                        mod_obj.flag = ''
                        mod_obj.save()
                        return Response("Modification request rejected.", status=200)
                return Response("Nothing done.",status=200)
            return Response(serializer.errors, status=400)
        return Response("Only admin can change status.", status=401)



class EncounterFlagDead(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = EncounterFlagDeadSerializer

    def put(self,request,id):
        mod_obj = ModifyDelete.objects.get(id=id)
        serializer = EncounterFlagDeadSerializer(mod_obj,data=request.data,context={'request': request},partial=True)
        if serializer.is_valid():
            if mod_obj.modify_status == 'approved':
                if serializer.validated_data['modify_status'] == 'modified':
                    mod_obj.modify_status = 'modified'
                    mod_obj.flag = ''
                    mod_obj.save()
                    return Response("Encounter modified successfully.", status=200)
            return Response("Nothing done.", status=400)
        return Response(serializer.errors, status=400)



class EncounterRestore(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)

    def put(self,request,encounter_id):
        mod_obj = ModifyDelete.objects.filter(encounter=encounter_id,delete_status='deleted',author=request.user)
        if mod_obj:
            mod_obj = ModifyDelete.objects.get(encounter=encounter_id,delete_status='deleted',author=request.user)
            if datetime.now().timestamp() < mod_obj.restore_expiry_date.timestamp():
                mod_obj.delete_status = ''
                mod_obj.flag = ''
                mod_obj.save()

                encounter_obj = Encounter.objects.get(id=encounter_id)
                encounter_obj.active = True
                encounter_obj.save()
                return Response('Encounter restored successfully.', status=200)
            return Response("Restoration time expired.",status=400)
        return Response("This encounter is not deleted yet.", status=400)



class CheckModifyExpiry(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)

    def post(self,request):
        mod_obj = ModifyDelete.objects.filter(modify_status='approved')
        if mod_obj:
            for i in mod_obj:
                if datetime.now().timestamp() > i.modify_expiry_date.timestamp():
                    i.modify_status = 'expired'
                    i.flag = ''
                    i.save()
            return Response('All the encounter flags with modify date expired are killed',status=200)
        return Response("No encounter deleted found.", status=400)


class CheckRestoreExpiry(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)

    def post(self,request):
        mod_obj = ModifyDelete.objects.filter(delete_status='deleted')
        if mod_obj:
            for i in mod_obj:
                if datetime.now().timestamp() > i.restore_expiry_date.timestamp():
                    encounter_obj = Encounter.objects.get(id=i.encounter.id)
                    encounter_obj.delete()
            return Response('All the encounter with restoration date expired are removed from recycle bin',status=200)
        return Response("No encounter deleted found.", status=400)



class Recyclebin(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = AllEncounterSerializer

    def get(self,request):
        encounter_obj = Encounter.objects.filter(active=False)
        serializer = AllEncounterSerializer(encounter_obj,many=True,context={"request":request})
        return Response(serializer.data,status=200)






