import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User,CustomUser
from addressapp.serializers.address import GeoSerializer
from addressapp.models import Ward

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from addressapp.serializers.address import WardSerializer

class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # if request.method == 'GET':
        #     return True
        return request.user and request.user.is_authenticated


class GeographyListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = WardSerializer

    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id,admin=True).exists():
            geography_obj = Ward.objects.filter(status=True)
            serializer = WardSerializer(geography_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
        elif User.objects.filter(id=request.user.id).exists():
            geography_obj = Ward.objects.filter(customuser=request.user,status=True)
            serializer = WardSerializer(geography_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
