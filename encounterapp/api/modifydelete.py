from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from encounterapp.models.modifydelete import ModifyDelete
from encounterapp.models.encounter import Encounter
from visualizationapp.models import Visualization
from encounterapp.serializers.encounter import AllEncounterSerializer
from encounterapp.serializers.modifydelete import ModifyDeleteSerializer,EncounterAdminStatusSerializer,ModifyDeleteListSerializer,EncounterFlagDeadSerializer
from datetime import datetime, timedelta




class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
    	return request.user and request.user.is_authenticated


class ModifyDeleteDetail(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = ModifyDeleteSerializer

    def get(self, request):
        if request.user.admin:
            modify_delete_obj = ModifyDelete.objects.all().order_by("-id")
        else:
            modify_delete_obj = ModifyDelete.objects.filter(author=request.user).order_by("-id")
        serializer = ModifyDeleteListSerializer(modify_delete_obj,\
            many=True, context={"request":request})
        return Response(serializer.data, status=200)

    def post(self,request):
        serializer = ModifyDeleteSerializer(data=request.data)
        if serializer.is_valid():
            modify_delete_obj = ModifyDelete()
            encounter_obj = Encounter.objects.filter(id=serializer.validated_data['encounter'].id)
            if encounter_obj:
                encounter_obj = Encounter.objects.get(id=serializer.validated_data['encounter'].id)
                if encounter_obj.active == False:
                    return Response({"message":"This encounter has already been deleted."}, status=400)
                if encounter_obj.request_counter >= 3:
                    return Response({"message":"Your request limit already reached."},status=400)
                if ModifyDelete.objects.filter(encounter__id = serializer.validated_data['encounter'].id,flag='delete') or ModifyDelete.objects.filter(encounter__id =serializer.validated_data['encounter'].id,flag='modify'):
                    return Response({"message":"You already have a request sent."}, status=400)
                if serializer.validated_data['flag'] == "modify":
                    if serializer.validated_data['reason_for_modification'] == None:
                        return Response({"message":"Please enter reason for modification."},status=400)
                    modify_delete_obj.reason_for_modification = serializer.validated_data['reason_for_modification']
                    modify_delete_obj.modify_status = "pending"

                if serializer.validated_data['flag'] == "delete":
                    if serializer.validated_data['reason_for_deletion'] == "other" and serializer.validated_data['other_reason_for_deletion'] == None:
                        return Response({"message":"You should enter the field either reason for deletion or other reason for deletion."},status=400)
                    if serializer.validated_data['reason_for_deletion'] == "other":
                        modify_delete_obj.other_reason_for_deletion = serializer.validated_data['other_reason_for_deletion']
                    modify_delete_obj.reason_for_deletion = serializer.validated_data['reason_for_deletion']
                    modify_delete_obj.delete_status = 'pending'
                modify_delete_obj.author = request.user
                modify_delete_obj.encounter = serializer.validated_data['encounter']
                modify_delete_obj.flag = serializer.validated_data['flag']
                modify_delete_obj.save()
                return Response({"message":"Your request sent successfully."},status=200)
            return Response({"message":"Encounter doesn't exists."},status=400)
        return Response(serializer.errors,status=400)


class EncounterAdminStatus(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = EncounterAdminStatusSerializer

    def get(self, request, id):
        if ModifyDelete.objects.filter(id=id):
            mod_obj = ModifyDelete.objects.get(id=id)
            serializer = ModifyDeleteListSerializer(mod_obj, context={"request":request})
            return Response(serializer.data, status=200)
        return Response({"message":"Flag id do not match."}, status=400)

    def put(self, request, id):
        if ModifyDelete.objects.filter(id=id):
            mod_obj = ModifyDelete.objects.get(id=id)
            serializer = EncounterAdminStatusSerializer(mod_obj,\
                data=request.data,context={'request': request},partial=True)
            if request.user.admin:
                if serializer.is_valid():
                    if mod_obj.delete_status == 'pending' and serializer.validated_data['delete_status'] == 'deleted':
                        mod_obj.delete_status = 'deleted'
                        mod_obj.deleted_at = datetime.now()
                        mod_obj.restore_expiry_date = datetime.now()+timedelta(days=30)
                        mod_obj.save()

                        encounter_obj = Encounter.objects.get(id=mod_obj.encounter.id)
                        encounter_obj.active = False
                        encounter_obj.request_counter += 1
                        visual_obj = Visualization.objects.filter(encounter_id=encounter_obj.id)
                        if visual_obj:
                            visual_obj = Visualization.objects.get(encounter_id=encounter_obj.id)
                            visual_obj.delete()
                        encounter_obj.save()
                        return Response({"message":"Encounter deleted successfully."}, status=200)
                    if mod_obj.delete_status == 'pending' and serializer.validated_data['delete_status'] == 'rejected':
                        mod_obj.delete_status = 'rejected'
                        mod_obj.flag = ''
                        mod_obj.save()
                        return Response({"message":"Encounter delete request is rejected."}, status=200)
                    if mod_obj.modify_status == 'pending':
                        if serializer.validated_data['modify_status'] == 'approved':
                            mod_obj.modify_approved_at = datetime.now()
                            mod_obj.modify_expiry_date = datetime.now()+timedelta(days=7)
                            mod_obj.modify_status = 'approved'
                            mod_obj.save()

                            encounter_obj = Encounter.objects.get(id=mod_obj.encounter.id)
                            encounter_obj.request_counter += 1

                            visual_obj = Visualization.objects.filter(encounter_id=encounter_obj.id)
                            if visual_obj:
                                visual_obj = Visualization.objects.get(encounter_id=encounter_obj.id)
                                visual_obj.delete()
                            encounter_obj.save()
                            return Response({"message":"Modification request approved."}, status=200)
                        if serializer.validated_data['modify_status'] == 'rejected':
                            mod_obj.modify_status = 'rejected'
                            mod_obj.flag = ''
                            mod_obj.save()
                            return Response({"message": "Modification request rejected."}, status=200)
                    return Response({"message":"Neither modify nor delete action performed"}, status=200)
                return Response(serializer.errors, status=400)
            return Response({"message":"Only admin can change status."}, status=401)
        return Response({"message":"Flag id do not match."}, status=400)



class EncounterFlagDead(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = EncounterFlagDeadSerializer

    def put(self, request, id):
        mod_obj = ModifyDelete.objects.get(id=id)
        serializer = EncounterFlagDeadSerializer(mod_obj, data=request.data,\
            context={'request': request}, partial=True)
        if serializer.is_valid():
            if mod_obj.modify_status == 'approved':
                if serializer.validated_data['modify_status'] == 'modified':
                    mod_obj.modify_status = 'modified'
                    mod_obj.flag = ''
                    mod_obj.save()
                    return Response({"message":"Encounter modified successfully and flag killed."}, status=200)
                return Response({"message":"Only modify status equals to modified can kill tha flag."},status=400)
            return Response({"message": "modify status most be approved before killing flag."}, status=400)
        return Response(serializer.errors, status=400)



class EncounterRestore(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)

    def put(self, request,encounter_id):
        encounter_obj = Encounter.objects.filter(id=encounter_id, active=False)
        if encounter_obj:
            mod_obj = ModifyDelete.objects.filter(encounter=encounter_id, delete_status='deleted', author=request.user)
            if mod_obj:
                mod_obj = ModifyDelete.objects.get(encounter=encounter_id, delete_status='deleted', author=request.user)
                if datetime.now().timestamp() < mod_obj.restore_expiry_date.timestamp():
                    mod_obj.delete_status = ''
                    mod_obj.flag = ''
                    mod_obj.save()

                    encounter_obj = Encounter.objects.get(id=encounter_id)
                    encounter_obj.active = True
                    visual_obj = Visualization.objects.filter(encounter_id=encounter_obj.id)
                    if visual_obj:
                        visual_obj = Visualization.objects.get(encounter_id=encounter_obj.id)
                        visual_obj.delete()
                    encounter_obj.save()
                    return Response({'messsage':'Encounter restored successfully.'}, status=200)
                return Response({'message':"Restoration time expired."}, status=400)
            return Response({"message":"flag doesn't exists"},status=400)
        return Response({'message':"No encounter deleted found."}, status=400)



class CheckModifyExpiry(APIView):

    def get(self,request):
        mod_obj = ModifyDelete.objects.filter(modify_status='approved')
        if mod_obj:
            for i in mod_obj:
                if datetime.now().timestamp() > i.modify_expiry_date.timestamp():
                    i.modify_status = 'expired'
                    i.flag = ''
                    i.save()
            return Response({'message':'All the encounter flags with modify date expired are killed'},status=200)
        return Response({"message":"No encounter deleted found."}, status=400)


class CheckRestoreExpiry(APIView):

    def get(self,request):
        mod_obj = ModifyDelete.objects.filter(delete_status='deleted')
        if mod_obj:
            for i in mod_obj:
                if datetime.now().timestamp() > i.restore_expiry_date.timestamp():
                    encounter_obj = Encounter.objects.get(id=i.encounter.id)
                    encounter_obj.delete()
            return Response({'message':'All the encounter with restoration date expired are removed from recycle bin'},status=200)
        return Response({"message":"No encounter deleted found."}, status=400)



class Recyclebin(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = AllEncounterSerializer

    def get(self,request):
        encounter_obj = Encounter.objects.filter(active=False)
        serializer = AllEncounterSerializer(encounter_obj,many=True,context={"request":request})
        return Response(serializer.data,status=200)






