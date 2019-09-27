#pylint: disable = R0903,E0401,C0111,C0103
"""
Serilizers for Data Conversion
JSON  <--->  Django Objects
"""
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import serializers
from api.decoraters import USER_LOGS
from api.backend import custom_authenticate
from api.models.exe_test import exe


def getGenericSerializer(model_arg):
    """
    Simple generic serializer to serialize all
    the fields of the Model without relation
    """
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            # locals().update(validators_dict)
            model = model_arg
            fields = '__all__'

        def create(self, validated_data):
            obj_create = self.Meta.model
            return obj_create.objects.create(**validated_data)

    return GenericSerializer




def GenericSerializerField(model_arg, validators_dict):
    """
    Special Field Serializer
    Only for PUT method
    """
    class GenericSerialField(serializers.ModelSerializer):
        class Meta:
            locals().update(validators_dict)
            model = model_arg
            fields = '__all__'
            # validators=[CharOnly()]

        def create(self, validated_data):
            obj_create = self.Meta.model
            return obj_create.objects.create(**validated_data)

        def update(self, instance, validated_data):
            # obj_create = self.Meta.model
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance

    return GenericSerialField




def NestedSerializer(model_arg, related_fields, fields_to_fetch):
    """
    Relational Serializer for ONE to MANY
    for models having related fields
    """
    class Testrelationserializer(serializers.ModelSerializer):
        locals().update(related_fields)

        class Meta:
            model = model_arg
            fields = fields_to_fetch

        def create(self, validated_data):
            obj_create = self.Meta.model
            return obj_create.objects.create(**validated_data)

    return Testrelationserializer




def GenericTrackSerializer(model_arg):
    """
    Supported serializer for ONE to MANY relations
    i.e cities = Cityserializer(many=TRUE)
    """

    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_arg
            fields = '__all__'

    return GenericSerializer



def ReverseStringSerializer(model_arg, keys):
    """
    Serializer for relation MANY to ONE Foreignkey Value Serializer
    USED StringRelatedField(many = TRUE)
    """

    class GenericSerializer(serializers.ModelSerializer):
        locals().update(keys)

        class Meta:
            model = model_arg
            fields = '__all__'

    return GenericSerializer





def ReverseNestedSerializer(model_arg):
    """
    Reverese serializer for MANY to ONE for Output
    Nested Json
    """
    class GenericSerializer(serializers.ModelSerializer):
        # locals().update(keys)
        class Meta:
            model = model_arg
            fields = '__all__'

    return GenericSerializer




class LoginSerializer(serializers.Serializer):
    """
    Login Serializer for Username and Password
    provided with POST in JSON
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get("username") and data.get("password"):
            username = data.get("username")
            password = data.get("password")
            try:
                user = authenticate(username=username, password=password)
            except BaseException:
                USER_LOGS.info("Authentication Error " + str(BaseException))
            if user:
                USER_LOGS.info("New User Authenticated -->  " + str(user))
                if user.is_active and user.is_authenticated:
                    data["user"] = user
                else:
                    ms_g = "user is disabled!!!"
                    raise exceptions.ValidationError(ms_g)
            else:
                user = custom_authenticate(username=username, password=password)
                data["user"] = user
                return data
        else:
            message = "Provide Both The Credentials"
            return message


class exe_serializer(serializers.ModelSerializer):
    class Meta:
        model = exe
        fields = "__all__"

        def create(self, validated_data):
            obj_create = self.Meta.model
            return obj_create.objects.create(**validated_data)
