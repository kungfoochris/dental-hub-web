import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from addressapp.serializers.address import DistrictSerializer,MunicipalitySerializer,\
WardSerializer,WardSerializerUpdate
from addressapp.models import Address, District, Municipality ,Ward

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class AddressList(APIView):
    def get(self, request, format=None):
        address_obj = District.objects.all().order_by('name')
        serializer = DistrictSerializer(address_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

# class MunicipalityList(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = AddressSerializer

#     def get(self, request, district,format=None):
#         address_obj = Address.objects.filter(district=district)
#         serializer = AddressSerializer(address_obj, many=True, \
#             context={'request': request})
#         return Response(serializer.data)

class WardList(APIView):
    serializer_class = WardSerializer

    def get(self, request,format=None):
    	ward_obj = Ward.objects.all()
    	serializer = WardSerializer(ward_obj, many=True, \
    		context={'request': request})
    	return Response(serializer.data)

class UserWardList(APIView):
    serializer_class = WardSerializer

    def get(self, request,format=None):
        ward_obj = Ward.objects.filter(status=True)
        serializer = WardSerializer(ward_obj, many=True, \
            context={'request': request})
        return Response(serializer.data)

class WardUpdate(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = WardSerializerUpdate

    def get(self, request, ward_id, format=None):
        if request.user.admin:
            if Ward.objects.filter(id=ward_id):
                ward_obj = Ward.objects.get(id=ward_id)
                serializer = WardSerializer(ward_obj, many=False, \
                    context={'request': request})
                return Response(serializer.data)
            return Response({"message":"id do not match"},status=400)
        return Response({"message":"only admin can see."},status=400)

    def put(self, request, ward_id, format=None):
        if request.user.admin:
            if Ward.objects.filter(id=ward_id):
                ward_obj = Ward.objects.get(id=ward_id)
                serializer = WardSerializerUpdate(ward_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    ward_obj.name=serializer.validated_data['name'].capitalize()
                    ward_obj.status=True
                    ward_obj.save()
                    return Response({"district":ward_obj.municipality.district.name,"municipality_name":ward_obj.municipality.name,"ward_number":ward_obj.ward,"name":ward_obj.name},status=200)
                return Response({'message':serializer.errors}, status=400)
            return Response({"message":"content not found"},status=204)
        return Response({"message":"only admin can edit"},status=400)