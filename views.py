# pylint: disable = E0401,C0301,C0111,R0903,R0201
""" Django Views """
import datetime
import json
from django.db import models
from django.contrib.auth import login, logout
from django.apps import apps
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from reversion import revisions as reversion
from api.models.exe_test import exe
from api.serializers import getGenericSerializer, GenericSerializerField, \
    LoginSerializer, NestedSerializer, GenericTrackSerializer, \
    ReverseStringSerializer, ReverseNestedSerializer, exe_serializer
from .decoraters import SpecificDecorator, ListViewDecorator, \
    Logger_create, User_Logger_create, USER_LOGS, \
    audit_log_list, audit_log_id
from .validators import CharOnly, UpperCaseOnly
from .decoraters import REQ_LOGS
from .backend import ExampleAuthentication,CustomLDAPBackend
# from drf_metadata.meta import MetaData,CustomMetadata,AbstractField
# from api.models.ui_demo import ui_demo
# from rest_framework.metadata import SimpleMetadata


class GenericMaster(APIView):
    """
    Generic Master for all the Specific operations
    GET     --->  /id
    POST    --->  post
    PUT     --->  /id (update)
    DELETE  --->  /id
    """

    authentication_classes = [ExampleAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET for Speific
    record
    i.e GET /id
    """

    @Logger_create
    @SpecificDecorator
    def get(self, request, app, model, id):
        model = apps.get_model(app, model)
        if id:
            dataset = model.objects.all()
            try:
                dept_name = get_object_or_404(dataset, id=id)
            except ObjectDoesNotExist:
                REQ_LOGS.error("Requested Object Doesnt Exist" + str(ObjectDoesNotExist))
            foreign_keys = {}
            related_fields = {}
            simple_fields = []
            for field in model._meta.get_fields():
                if isinstance(field, models.ForeignKey):
                    serial = ReverseNestedSerializer(field.related_model)
                    foreign_keys[field.name] = serial(read_only=True)
                    continue
                elif field.is_relation:
                    serial = GenericTrackSerializer(field.related_model)
                    related_fields[field.name] = serial(many=True)
                    continue
                else:
                    simple_fields.append(field.name)
                    continue
            if foreign_keys:
                serializer_uniq = ReverseStringSerializer(model, foreign_keys)
                serializer = serializer_uniq(dept_name)
                return Response(serializer.data)
            elif related_fields:
                fields_to_fetch = [field.name for field in model._meta.get_fields()]
                GenericSzl = NestedSerializer(model, related_fields, fields_to_fetch)
                serializer = GenericSzl(dept_name)
                return Response(serializer.data)
            else:
                serializer = getGenericSerializer(model)
                serial = serializer(dept_name)
                return Response(serial.data)

    """
    POST the DATA
    i.e   Actual POST
    Works only for the Dedicated Model Fields
    No Relational Data POST
    """

    # @audit_log_id
    @Logger_create
    @SpecificDecorator
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        org = json.loads(request.body.decode('utf8'))
        try:
            d = request.data
            print("###################3 bahar", d)
            if not d:
                print("#########################3333", d)
                REQ_LOGS.error("In valid Json provided for POST")
                raise json.JSONDecodeError("InValid JSON provided", doc=request.data, pos=0)
        except json.JSONDecodeError:
            REQ_LOGS.error("In valid Json provided for POST")
            return Response("Invalid JSON for the POST")

        validators_d = {}
        # validators_d['validators'] = [CharOnly(), UpperCaseOnly()]
        serialize = getGenericSerializer(model)
        serial_data = serialize(data=d)
        if serial_data.is_valid():
            with transaction.atomic(), reversion.create_revision():
                reversion.set_user(request.user)
                reversion.set_comment(request.method)
                reversion.set_date_created(date_created=datetime.datetime.now())
                serial_data.save()
            audit_log_list(org, request, app, model)

            return Response(serial_data.data, status=status.HTTP_201_CREATED)
        return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    PUT the DATA for specific ID
    i.e    /id
    Updates the DATA for model 
    Only for Dedicated fields
    NO UPDATE for Relational Fields
    """

    # @audit_log_id
    @Logger_create
    @SpecificDecorator
    def put(self, request, app, model, id):
        try:

            d = request.data
            # if not d:
            #     raise json.JSONDecodeError("InValid JSON provided",doc=,pos=0)
        except json.JSONDecodeError:
            REQ_LOGS.error("In valid Json provided for POST")
            # return Response("Invalid JSON for the POST")

        model = apps.get_model(app, model)
        obj = model.objects.get(id=id)
        validators_d = {}
        validators_d['validators'] = [CharOnly(), UpperCaseOnly()]
        serializer_org = getGenericSerializer(model)
        serial_org_data = serializer_org(obj)
        serializer = GenericSerializerField(model, validators_d)
        serial_data = serializer(obj, data=d, partial=True)
        if serial_data.is_valid():
            with transaction.atomic(), reversion.create_revision():
                reversion.set_user(request.user)
                reversion.set_comment(request.method)
                reversion.set_date_created(date_created=datetime.datetime.now())
                serial_data.save()
                audit_log_id(serial_org_data.data, serial_data.data, request, app, model, id)

            return Response(serial_data.data)
        return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE for Specific ID
    i.e   /id
    Deletes the Whole Record
    """

    @Logger_create
    @SpecificDecorator
    def delete(self, request, app, model, id):
        parser_classes = [parsers.JSONParser]
        if id:
            model = apps.get_model(app, model)
            try:
                obj = model.objects.get(id=id)
                if not obj:
                    raise ObjectDoesNotExist
                with transaction.atomic(), reversion.create_revision():
                    obj = model.objects.get(id=id)
                    obj.save()
                    reversion.set_user(request.user)
                    reversion.set_comment(request.method)
                    reversion.set_date_created(date_created=datetime.datetime.now())
                GenericSzl = getGenericSerializer(model)
                serializer = GenericSzl(obj)
                org = serializer.data
                obj.delete()
                updated = None
                audit_log_id(org, updated, request, app, model, id)
                return Response({"Deleted successfully": "Deleted Successfully!!!", "data": serializer.data},
                                status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist:
                REQ_LOGS.error("Object Doesnt Exist for DELETE " + " " + str(id) + " " + " by " + str(request.user))
                return Response("The Given Object Doesnt Exist!")


class ListViewDetail(APIView):
    """
    ListViewDetail for all the /LIST Operations
    GET     --->   /list
    POST    --->   /list (Conditional GET)
    DELETE  --->  /list (Conditional DELETE)
    """
    # authentication_classes = [SessionAuthentication, ExampleAuthentication, TokenAuthentication]
    authentication_classes = [CustomLDAPBackend]
    permission_classes = [IsAuthenticated]

    """
    GET for all
    i.e   /list
    """

    @Logger_create
    @ListViewDecorator
    def get(self, request, app, model):
        model = apps.get_model(app, model)
        field_list = [field.name for field in model._meta.get_fields()]
        foreign_keys = {}
        related_fields = {}
        simple_fields = []
        objs = model.objects.all()
        for field in model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                serial = ReverseNestedSerializer(field.related_model)
                foreign_keys[field.name] = serial(read_only=True)
                continue
            elif field.is_relation:
                serial = GenericTrackSerializer(field.related_model)
                related_fields[field.name] = serial(many=True)
                continue
            else:
                simple_fields.append(field.name)
                continue
        if foreign_keys:
            serializer_uniq = ReverseStringSerializer(model, foreign_keys)
            serializer = serializer_uniq(objs, many=True)
            return Response(serializer.data)
        elif related_fields:
            fields_to_fetch = [field.name for field in model._meta.get_fields()]
            GenericSzl = NestedSerializer(model, related_fields, fields_to_fetch)
            serializer = GenericSzl(objs, many=True)
            return Response(serializer.data)
        else:
            serializer = getGenericSerializer(model)
            serial = serializer(objs, many=True)
            return Response(serial.data)

    """
    POST for Conditional GET
    i.e    /list
    """

    @Logger_create
    @ListViewDecorator
    def post(self, request, app, model):
        dict_mapp = request.data
        model = apps.get_model(app, model)
        obj_filter = model.objects.filter(**dict_mapp)
        foreign_keys = {}
        related_fields = {}
        simple_fields = []
        for field in model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                serial = ReverseNestedSerializer(field.related_model)
                foreign_keys[field.name] = serial(read_only=True)
                continue
            elif field.is_relation:
                serial = GenericTrackSerializer(field.related_model)
                related_fields[field.name] = serial(many=True)
                continue
            else:
                simple_fields.append(field.name)
                continue

        if foreign_keys:
            serializer_uniq = ReverseStringSerializer(model, foreign_keys)
            serializer = serializer_uniq(obj_filter, many=True)
            return Response(serializer.data)
        elif related_fields:
            fields_to_fetch = [field.name for field in model._meta.get_fields()]
            GenericSzl = NestedSerializer(model, related_fields, fields_to_fetch)
            serializer = GenericSzl(obj_filter, many=True)
            return Response(serializer.data)
        else:
            serializer = getGenericSerializer(model)
            serial = serializer(obj_filter, many=True)
            return Response(serial.data)

    """
    DELETE for Contidional DELETE
    i.e    /list
    """

    # @audit_log_id
    @Logger_create
    @ListViewDecorator
    def delete(self, request, app, model):
        if request.data:
            dict_mapp = request.data
            model = apps.get_model(app, model)
            objs = model.objects.filter(**dict_mapp)
            with transaction.atomic(), reversion.create_revision():
                [objs[i].save() for i in range(len(objs))]
                reversion.set_user(request.user)
                reversion.set_comment(request.method)
                reversion.set_date_created(date_created=datetime.datetime.now())
            GenericSzl = getGenericSerializer(model)
            serializer = GenericSzl(objs, many=True)
            org = serializer.data
            objs.delete()
            audit_log_list(org, request, app, model)
            return Response({'Received data': request.data})

        else:
            return Response({"return none instead": "return none instead"})


class LoginView(APIView):
    """
    Login view for user Login and Authentication
    provided the username and Password in Json via POST
    and Token Generation
    """

    @User_Logger_create
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                USER_LOGS.info("Token Successfully generated for the ---> " + str(user))
                return Response({"Your Token": token.key}, status=200)
            else:
                return Response("Given User is not valid !!! Either wrong Credentials!!!!!!!")
        else:
            return Response("Plz Give Both the Credentials!!!")


class LogoutView(APIView):
    """
    User logoutView and
    Session Destroy
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        USER_LOGS.info("user --> " + str(request.user) + "Logged Out Successfully!!!!")
        return Response("User Logged OUT!!!!!!")


###################################           TEST PART         ###########################################################



# class MyCustomMetadata(SimpleMetadata):
#
#     def determine_metadata(self, request, view):
#         metadata = super(MyCustomMetadata, self).determine_metadata(request, view)
#         metadata['myatt'] = 'blablabla' # add extra attribute to metadata
#         return metadata # return the metadata with the extra attribute set in it

class CityTestView(APIView):
    authentication_classes = [ExampleAuthentication,SessionAuthentication,  TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # metadata_class = [MyCustomMetadata]

    @Logger_create
    @ListViewDecorator
    def get(self, request, app, model):
        print("####################     the cache value       ####################")
        print(cache.get('key'))
        print(cache.get('model_key'))
        model = apps.get_model(app, model)
        field_list = [field.name for field in model._meta.get_fields()]
        print("the fields of the model", field_list)
        print("the model relation#############")
        print(model.__dict__)
        foreign_keys = {}
        related_fields = {}
        simple_fields = []
        objs = model.objects.all()
        for field in model._meta.get_fields():
            print(field.name)
            print(field.is_relation)
            print(field.related_model)
            print(isinstance(field, models.ForeignKey))

            # if isinstance(field,models.ForeignKey):
            #     foreign_keys[field.name + " value"]  = serializers.StringRelatedField(source=field.name,read_only=True)
            #     print("in is instance")
            #     continue

            if isinstance(field, models.ForeignKey):
                serial = ReverseNestedSerializer(field.related_model)
                foreign_keys[field.name] = serial(read_only=True)
                continue
            elif field.is_relation:
                serial = GenericTrackSerializer(field.related_model)
                related_fields[field.name] = serial(many=True)
                print(" in is_relation")
                continue
            else:
                simple_fields.append(field.name)
                print("  in simple   ")
                continue

        # if foreign_keys:
        #     serializer_uniq = ReverseStringSerializer(model, foreign_keys)
        #     serializer = serializer_uniq(objs, many=True)
        #     return Response(serializer.data)
        # elif related_fields:
        #     fields_to_fetch = [field.name for field in model._meta.get_fields()]
        #     GenericSzl = NestedSerializer(model, related_fields, fields_to_fetch)
        #     serializer = GenericSzl(objs, many=True)
        #     return Response(serializer.data)
        # else:
        #     serializer = getGenericSerializer(model)
        #     serial = serializer(objs, many=True)
        #     return Response(serial.data)

        combine = {**foreign_keys, **related_fields}
        serializer_uniq = ReverseStringSerializer(model, combine)
        serializer = serializer_uniq(objs, many=True)
        return Response(serializer.data)
    @Logger_create
    @SpecificDecorator
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        org = json.loads(request.body.decode('utf8'))
        try:
            d = request.data
            print("###################3 bahar", d)
            if not d:
                print("#########################3333", d)
                REQ_LOGS.error("In valid Json provided for POST")
                raise json.JSONDecodeError("InValid JSON provided", doc=request.data, pos=0)
        except json.JSONDecodeError:
            REQ_LOGS.error("In valid Json provided for POST")
            return Response("Invalid JSON for the POST")

        validators_d = {}
        # validators_d['validators'] = [CharOnly(), UpperCaseOnly()]
        serialize = getGenericSerializer(model)
        serial_data = serialize(data=d)
        if serial_data.is_valid():
            # with transaction.atomic(), reversion.create_revision():
            #     reversion.set_user(request.user)
            #     reversion.set_comment(request.method)
            #     reversion.set_date_created(date_created=datetime.datetime.now())
            serial_data.save()
            # audit_log_list(org, request, app, model)

            return Response(serial_data.data, status=status.HTTP_201_CREATED)
        return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)


class Exe_Test_View(APIView):
    def post(self, request):
        model = exe
        # org = json.loads(request.body.decode('utf8'))
        d = request.data
        validators_d = {}
        # validators_d['validators'] = [CharOnly(), UpperCaseOnly()]
        # serialize = getGenericSerializer(model)
        # serial_data = serialize(data=d)
        serial_data = exe_serializer(data=d)
        if serial_data.is_valid():
            # with transaction.atomic(), reversion.create_revision():
            #     reversion.set_user(request.user)
            #     reversion.set_comment(request.method)
            #     reversion.set_date_created(date_created=datetime.datetime.now())
            serial_data.save()
            # audit_log_list(org, request, app, model)

            return Response(serial_data.data, status=status.HTTP_201_CREATED)
        return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)





# class BookViewSet(APIView):
#     # @list_route()
#     def get(self, request):
#         md = metadata.ui_meta().determine_metadata(request, self)
#         return Response(md)
