import logging
import datetime
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from dateutil import relativedelta
from userapp.models import User
from encounterapp.models import Encounter
from patientapp.models import Patient
from encounterapp.serializers.encounter import (
    EncounterSerializer,
    AllEncounterSerializer,
    EncounterUpdateSerializer,
    EncounterSerializer1,
)
from encounterapp.models.modifydelete import ModifyDelete
from addressapp.models import Ward, Activity
from rest_framework.pagination import PageNumberPagination
from encounterapp.pagination import PaginationHandlerMixin

today_encounter_date = datetime.date.today()
# Get an instance of a logger
logger = logging.getLogger(__name__)
utc = pytz.UTC


class BasicPagination(PageNumberPagination):
    page_size = 20

class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class EncounterView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterSerializer

    def get(self, request, patient_id, format=None):
        if User.objects.filter(id=request.user.id):
            if Patient.objects.filter(id=patient_id):
                if (
                    Encounter.objects.select_related("patient")
                    .filter(patient__id=patient_id)
                    .exists()
                ):
                    encounter_obj = Encounter.objects.select_related("patient").filter(
                        patient__id=patient_id
                    )
                    serializer = AllEncounterSerializer(
                        encounter_obj, many=True, context={"request": request}
                    )
                    return Response(serializer.data)
                return Response(
                    {"message": "encounter not added or not found"}, status=400
                )
            return Response({"message": "patient id does not exist."}, status=400)
        return Response({"message": "permission not allowed"}, status=400)

    def post(self, request, patient_id, format=None):
        serializer = EncounterSerializer(
            data=request.data, context={"request": request}
        )
        if Patient.objects.filter(id=patient_id).exists():
            patient_obj = Patient.objects.get(id=patient_id)
            # # check More then two encounter can not crated for same patient on same date.
            # if Encounter.objects.filter(
            #     patient__id=patient_id, created_at=today_encounter_date
            # ).count() > 1:
            #     return Response(
            #         {
            #             "message": "More then two encounter can not crated for same patient on same date."
            #         },
            #         status=400,
            #     )
            
            if serializer.is_valid():
                date = serializer.validated_data["created_at"].date()
                print(date)
                # check More than two encounter can not created for same patient on same date.
                if Encounter.objects.filter(
                    patient__id=patient_id, created_at__date=date
                ).count() > 1:
                    logger.info("%s %s" % ("Attempted to create more than one encounter for same patient on same date with patient id:", patient_id))
                    return Response(
                        {
                            "message": "More then two encounter can not be created for same patient on same date."
                        },
                        status=400,
                    )
                
                if Encounter.objects.filter(
                    patient__id=patient_id, created_at__date=date,author=request.user
                ).count() > 0:
                    logger.info("%s %s" % ("Attempted to create more than one encounter for same patient by same author on same date with patient id:", patient_id))
                    return Response(
                        {
                            "message": "More than one encounter can not be created for same patient by same author on same date."
                        },
                        status=400,
                    )

                activity_area_obj = serializer.validated_data["activityarea_id"]
                if Activity.objects.filter(id=activity_area_obj).exists():
                    activity_area_obj = Activity.objects.get(id=activity_area_obj)
                geography_obj = serializer.validated_data["geography_id"]
                if Ward.objects.filter(
                    id=serializer.validated_data["geography_id"]
                ).exists():
                    geography_obj = Ward.objects.get(
                        id=serializer.validated_data["geography_id"]
                    )
                encounter_obj = Encounter()
                encounter_obj.encounter_type = serializer.validated_data[
                    "encounter_type"
                ]
                encounter_obj.activity_area = activity_area_obj
                encounter_obj.geography = geography_obj
                encounter_obj.patient = patient_obj
                encounter_obj.author = request.user
                encounter_obj.other_problem = serializer.validated_data["other_problem"]
                encounter_obj.created_at = serializer.validated_data["created_at"]
                encounter_obj.updated_by = request.user
                encounter_obj.updated_at = serializer.validated_data["updated_at"]
                encounter_obj.area = serializer.validated_data["area"]
                encounter_obj.save()
                logger.info(
                    "%s %s"
                    % ("Encounter added successfully by", request.user.full_name)
                )
                return Response(
                    {"message": "Encounter added", "id": encounter_obj.id}, status=200
                )
                # logger.info("Geography id does not exists in encounter section.")
                # return Response({"message":"Geography id does not exists. created by="+request.user.full_name},status=400)
                # logger.info("Activity id does not exists in encounter section.")
                # return Response({"message":"Activity id does not exists."},status=400)
            logger.info(serializer.errors)
            return Response({"message": serializer.errors}, status=400)
        logger.info(
            "%s %s"
            % (
                "Patient id does not exist in encounter section: created by="
                + request.user.full_name,
                patient_id,
            )
        )
        return Response(
            {
                "message": "patient does not exists. created by="
                + request.user.full_name
            },
            status=400,
        )


# class EncounterUpdateView(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = EncounterUpdateSerializer

#     def get(self, request, patient_id, encounter_id, format=None):
#         if Encounter.objects.select_related('patient').filter(id=encounter_id,patient__id=patient_id).exists():
#             encounter_obj = Encounter.objects.get(id=encounter_id)
#             serializer = EncounterSerializer(encounter_obj, many=False, \
#                 context={'request': request})
#             return Response(serializer.data)
#         logger.error('encounter content not found.')
#         return Response({"message":"content not found or parameter not match."},status=400)

#     def put(self, request, patient_id, encounter_id, format=None):
#         today_date = datetime.now()
#         if Encounter.objects.select_related('patient').filter(id=encounter_id,patient__id=patient_id).exists():
#             encounter_obj=Encounter.objects.select_related('patient').get(id=encounter_id,patient__id=patient_id)
#             serializer = EncounterUpdateSerializer(encounter_obj,data=request.data,\
#                 context={'request': request},partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 logger.info("%s %s" %("Encounter update successfully by", request.user.full_name))
#                 return Response({"message":"encounter update"},status=200)
#             logger.info(serializer.errors)
#             return Response({'message':serializer.errors}, status=400)
#         logger.info("%s %s" %("Patient id does not  exists in encounter section : ", patient_id))
#         return Response({"message":"id do not match"},status=400)



class EncounterUpdate(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterSerializer1

    def get(self, request, patient_id, encounter_id, format=None):
        if Encounter.objects.select_related('patient').filter(id=encounter_id,patient__id=patient_id).exists():
            encounter_obj = Encounter.objects.get(id=encounter_id)
            serializer = EncounterSerializer1(encounter_obj, many=False,context={'request': request})
            return Response(serializer.data)
        return Response({"message":"content not found or parameter not match."},status=400)

    def put(self, request, patient_id, encounter_id, format=None):
        today_date = datetime.date.today()
        if Encounter.objects.select_related('patient').filter(id=encounter_id,patient__id=patient_id).exists():
            encounter_obj=Encounter.objects.select_related('patient').get(id=encounter_id,patient__id=patient_id)
            serializer = EncounterSerializer1(encounter_obj,data=request.data,context={'request': request},partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"encounter update"},status=200)
            return Response({'message':serializer.errors}, status=400)
        return Response({"message":"patient id or encounter id do not match"},status=400)



class EncounterList(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    
    def get(self, request, format=None, *args, **kwargs):
        encounter_obj = Encounter.objects.all()
        page = self.paginate_queryset(encounter_obj)
        if page is not None:
            serializer = self.get_paginated_response(AllEncounterSerializer(page,\
                many=True, context={"request":request}).data)
        else:
            serializer = AllEncounterSerializer(encounter_obj, many=True)
        return Response(serializer.data,status=200)



class EncounterUpdateView(APIView):
    permission_classes = (IsPostOrIsAuthenticated,)
    serializer_class = EncounterUpdateSerializer

    def get(self, request, patient_id, encounter_id, format=None):
        if (
            Encounter.objects.select_related("patient")
            .filter(id=encounter_id, patient__id=patient_id)
            .exists()
        ):
            encounter_obj = Encounter.objects.get(id=encounter_id)
            serializer = EncounterSerializer(
                encounter_obj, many=False, context={"request": request}
            )
            return Response(serializer.data)
        logger.error("encounter content not found.")
        return Response(
            {"message": "content not found or parameter not match."}, status=400
        )

    def put(self, request, patient_id, encounter_id, format=None):
        today_date = datetime.now()
        if (
            Encounter.objects.select_related("patient")
            .filter(id=encounter_id, patient__id=patient_id)
            .exists()
        ):
            encounter_obj = Encounter.objects.select_related("patient").get(
                id=encounter_id, patient__id=patient_id
            )
            serializer = EncounterUpdateSerializer(
                encounter_obj,
                data=request.data,
                context={"request": request},
                partial=True,
            )
            if serializer.is_valid():
                en_obj = Encounter.objects.get(id=encounter_id, patient__id=patient_id)
                time = int(
                    relativedelta.relativedelta(
                        datetime.now().replace(tzinfo=utc),
                        en_obj.created_at.replace(tzinfo=utc),
                    ).hours
                )
                if time < 24:
                    serializer.save()
                    return Response({"message": "encounter update"}, status=200)
                obj = ModifyDelete.objects.filter(
                    encounter__id=encounter_id, modify_status="approved", flag="modify"
                )
                if obj:
                    obj = ModifyDelete.objects.get(
                        encounter__id=encounter_id,
                        modify_status="approved",
                        flag="modify",
                    )
                    t = int(
                        relativedelta.relativedelta(
                            datetime.now().replace(tzinfo=utc),
                            obj.modify_approved_at.replace(tzinfo=utc),
                        ).days
                    )
                    if t < 7:
                        obj.modify_status = "modified"
                        obj.flag = ""
                        obj.save()
                        serializer.save()
                        logger.info(
                            "%s %s"
                            % (
                                "Encounter update successfully by",
                                request.user.full_name,
                            )
                        )
                        return Response({"message": "encounter updated"}, status=200)
                    obj.modify_status = "expired"
                    obj.flag = ""
                    obj.save()
                    logger.info("Encounter modification time expired.")
                    return Response(
                        "Modification time has been expired. Please send a new modification request.",
                        status=400,
                    )
                logger.info(
                    "Modification request has not been done or admin has not approved the request."
                )
                return Response(
                    "Modification request has not been done or admin has not approved the request.",
                    status=400,
                )
            logger.info(serializer.errors)
            return Response({"message": serializer.errors}, status=400)
        logger.info(
            "%s %s"
            % ("Patient id does not  exists in encounter section : ", patient_id)
        )
        return Response({"message": "id do not match"}, status=400)
