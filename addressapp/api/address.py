import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from addressapp.serializers.address import DistrictSerializer,MunicipalitySerializer,WardSerializer
from addressapp.models import Address, District, Municipality ,Ward

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class AddressList(APIView):
    def get(self, request, format=None):
        address_obj = District.objects.filter(status=True).order_by('name')
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
    	ward_obj = Ward.objects.filter(status=True)
    	serializer = WardSerializer(ward_obj, many=True, \
    		context={'request': request})
    	return Response(serializer.data)