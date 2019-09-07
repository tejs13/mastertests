from rest_framework import serializers
from .models import Department,State,City
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from rest_framework import exceptions

from rest_framework import serializers
from logger import *
import os
try:
    os.mkdir(os.path.join(os.getcwd(),'USER_LOGS'))
    print("Directory Created")
except FileExistsError as e:
    print('Directory already in existance')


user_logger=logger_create(os.path.join(os.getcwd(),'USER_LOGS'))

def getGenericSerializer(model_arg):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_arg
            fields = '__all__'
        def create(self,validated_data):
            m=self.Meta.model
            return m.objects.create(**validated_data)
        def update(self,Instance,validated_data):
            pass
    return GenericSerializer

def GenericSerializerField(model_arg):
    class GenericSerialField(serializers.ModelSerializer):
        class Meta:
            model = model_arg
            fields='__all__'
        def create(self,validated_data):
            m=self.Meta.model
            return m.objects.create(**validated_data)
        def update(self,instance,validated_data):
            m=self.Meta.model

            for attr, value in validated_data.items():
                print(attr)
                print(value)
                setattr(instance, attr, value)
            instance.save()
            return instance
    return GenericSerialField


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        if data.get("username") and data.get("password"):
            username = data.get("username")
            password = data.get("password")
            user = authenticate(username=username,password=password)
            if user:
                user_logger.log.info("New User Arriving-->  ",str(user))
                if user.is_active and user.is_authenticated:
                    data["user"] = user
                else:
                    ms="user is disabled!!!"
                    raise exceptions.ValidationError(ms)
            else:
                ms="unable to login"
                data["user"] = None

            return data


        else:
            message="Provide Both The Credentials"
            return message


