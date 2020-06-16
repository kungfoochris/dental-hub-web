from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from encounterapp.models.modifydelete import ModifyDelete
from encounterapp.serializers.modifydelete import ModifyDeleteSerializer



class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
    	return request.user and request.user.is_authenticated


class ModifyDeleteDetail(APIView):
    permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = ModifyDeleteSerializer

    def get(self,request):
        modify_delete_obj = ModifyDelete.objects.all()
        serializer = ModifyDeleteSerializer(modify_delete_obj,many=True,context={"request":request})
        return Response(serializer.data,status=200)

    def post(self,request):
        serializer = ModifyDeleteSerializer(data=request.data)              
        if serializer.is_valid():
            modify_delete_obj = ModifyDelete()
            modify_delete_obj.encounter = serializer.validated_data['encounter']
            modify_delete_obj.flag = serializer.validated_data['flag']
            if serializer.validated_data['flag'] == "modify":
                modify_delete_obj.reason_for_modification = serializer.validated_data['reason_for_modification']
                modify_delete_obj.modify_status = "pending"
            if serializer.validated_data['flag'] == "delete":
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

