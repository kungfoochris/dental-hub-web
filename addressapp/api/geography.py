import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from userapp.models import User

from addressapp.serializers.geography import GeographySerializer
from addressapp.models import Geography

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class IsPostOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        # if request.method == 'GET':
        #     return True
        return request.user and request.user.is_authenticated


class GeographyListView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = GeographySerializer

    def get(self, request, format=None):
        if request.user.admin:
            geography_obj = Geography.objects.filter(status=True)
            serializer = GeographySerializer(geography_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)
        else:
            geography_obj = Geography.objects.filter(user=request.user)
            serializer = GeographySerializer(geography_obj, many=True, \
                context={'request': request})
            return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.admin:
            serializer = GeographySerializer(data=request.data,\
                context={'request': request})
            if serializer.is_valid():
                if re.match("^[a-zA-Z]+$", serializer.validated_data['street_address']):
                    if Geography.objects.filter(state=serializer.validated_data['state'],\
                        city=serializer.validated_data['city'],\
                        street_address=serializer.validated_data['street_address']).exists():
                        return Response({"message":"This location already exists"},status=400)
                    geography_obj = Geography()
                    geography_obj.state = serializer.validated_data['state']
                    geography_obj.city = serializer.validated_data['city']
                    geography_obj.street_address = serializer.validated_data['street_address']. capitalize()
                    geography_obj.country = serializer.validated_data['country']
                    geography_obj.save()
                    return Response({"message":"Geography location added."},status=200)
                return Response({"message":"Street Address should only contain String With out space"},status=400)
            return Response({'message':serializer.errors}, status=400)
        return Response({"message":"only admin can add"},status=400)


class GeographyUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = GeographySerializer

    def get(self, request, pk, format=None):
        if request.user.admin:
            if Geography.objects.filter(id=pk,status=True).exists():  
                geography_obj = Geography.objects.get(id=pk,status=True)
                serializer = GeographySerializer(geography_obj, many=False, \
                    context={'request': request})
                return Response(serializer.data)
            return Response({"message":"content not found"},status=204)
        return Response({"message":"only admin can see"},status=400)

    def put(self, request, pk, format=None):
        if request.user.admin:
            if Geography.objects.filter(id=pk,status=True).exists():
                geography_obj = Geography.objects.get(id=pk)
                serializer = GeographySerializer(geography_obj,data=request.data,\
                    context={'request': request},partial=True)
                if serializer.is_valid():
                    if re.match("^[a-zA-Z]+$", serializer.validated_data['street_address']):
                        if Geography.objects.filter(state=serializer.validated_data['state'],\
                            city=serializer.validated_data['city'],\
                            street_address=serializer.validated_data['street_address']).exists():
                            return Response({"message":"This location already exists"},status=400)
                        geography_obj.city = serializer.validated_data['city']
                        geography_obj.state = serializer.validated_data['state']
                        geography_obj.country = serializer.validated_data['country']
                        geography_obj.street_address = serializer.validated_data['street_address'].capitalize()
                        geography_obj.save()
                        return Response({"message":"geography update"},status=200)
                    return Response({"message":"Street Address should only contain String With out space"},status=400)
                logger.error(serializer.errors)
                return Response({'message':serializer.errors}, status=400)
            logger.error("content not found")
            return Response({"message":"content not found"},status=204)
        logger.error("only admin can edit")
        return Response({"message":"only admin can edit"},status=400)


    def delete(self, request, pk, format=None):
        if request.user.admin:
            if Geography.objects.filter(id=pk,status=True).exists():
                geography_obj = Geography.objects.get(id=pk)
                geography_obj.status = False
                geography_obj.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"message":"no content found"},status=204)
        return Response({'errors': 'Permission Denied'},status=400)  