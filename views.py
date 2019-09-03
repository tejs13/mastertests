from django.shortcuts import render

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer, GenericSerializer
from django.apps import apps

# from django.db.models.loading import get_model


class GenericMaster(APIView):
    """
    Generic Master
    """
    def get(self, request, app,model,format=None):
        modelToLoad = model
        print("model to load", modelToLoad, app)
        model = apps.get_model(app, modelToLoad)
        # model = get_model('app_name', 'model_name')
        objs = model.objects.all()
        serializer = GenericSerializer(objs, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)