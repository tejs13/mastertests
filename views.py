from django.shortcuts import render
from django.http import Http404
import json
from django.http import JsonResponse
from django.http import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers
from rest_framework.renderers import JSONRenderer
from django.http import request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.contrib.auth import login,logout
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import getGenericSerializer,GenericSerializerField,LoginSerializer
from django.apps import apps
from django.shortcuts import get_object_or_404
from logger import *
import os
from django.contrib.auth.decorators import login_required

try:
    os.mkdir(os.path.join(os.getcwd(),'API_REQUESTS_LOGS'))
    print("Directory Created")
except FileExistsError as e:
    print('Directory already in existance')



requests_logger=logger_create(os.path.join(os.getcwd(),'API_REQUESTS_LOGS'))

try:
    os.mkdir(os.path.join(os.getcwd(),'TOKEN_LOGS'))
    print("Directory Created")
except FileExistsError as e:
    print('Directory already in existance')



token_logger=logger_create(os.path.join(os.getcwd(),'TOKEN_LOGS'))


"""
 Generic Master
 """
class GenericMaster(APIView):

    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # @login_required(login_url='master/login')
    def dispatch(self, request, *args, **kwargs):
        print(request.body)
        model=kwargs.get('model')
        app= kwargs.get('app')
        id = kwargs.get('id')
        list = kwargs.get('list')
        print(model,app,id,list)
        print(request.user.is_authenticated)
        print(request.user)
        if request.method.lower() == "get" and request.user.is_authenticated and request.user.has_permission(IsAuthenticated):
            print("get thru dispatch")
            return self.get(request,model,app,id)
        elif request.method.lower() == "post" and request.user.is_authenticated and request.user.has_permission(IsAuthenticated):
            return self.post(request,app,model,list)
        elif request.method.lower() == "put" and request.user.is_authenticated and request.user.has_permission(IsAuthenticated):
            return self.put(request,app,model,id)
        elif request.method.lower() == "delete" and request.user.is_authenticated and request.user.has_permission(IsAuthenticated):
            return self.delete(request,app,model,id)
        return super().dispatch(request,model=model,app=app,id=id)



    def get(self,request,model,app,id):
        print("get from dispatch")
        requests_logger.log.info("GET by " + str(request.user) + " for " +str(app)+ "."+ str(model))
        model = apps.get_model(app,model)
        if id:
            dataset = model.objects.all()
            dept_name = get_object_or_404(dataset, id=id)
            GenericSzl = getGenericSerializer(model)
            serializer = GenericSzl(dept_name)
            return JsonResponse(serializer.data,safe=False)
            # return Response(serializer.data)
        objs = model.objects.all()
        GenericSzl = getGenericSerializer(model)
        serializer = GenericSzl(objs, many=True)
        print(serializer.data)
        dataset=serializer.data
        return JsonResponse(dataset,safe=False)
        # return Response(serializer.data)


    def post(self, request,app,model,list):
        if list:
            dict_header=request.body
            print(dict_header)
            d=json.loads(dict_header)
            print(d)
            dict_mapp = dict(d)
            model = apps.get_model(app, model)
            obj_filter = model.objects.filter(**dict_mapp)
            GenericSzl = getGenericSerializer(model)
            serializer = GenericSzl(obj_filter, many=True)
            return JsonResponse(serializer.data,safe=False)
            # return Response(serializer.data)

        print("IN actual POST")
        model = apps.get_model(app,model)
        print(request.body)
        d=json.loads(request.body)
        serialize = getGenericSerializer(model)
        serial_data = serialize(data=d)
        if serial_data.is_valid():
            serial_data.save()
            return JsonResponse(serial_data.data,safe=False,status=status.HTTP_201_CREATED)
            # return Response(serial_data.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serial_data.errors,status=status.HTTP_400_BAD_REQUEST)
        # return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)





    def put(self, request, app, model, id,):
        d=json.loads(request.body)
        model = apps.get_model(app,model)
        obj = model.objects.get(id=id)
        serializer = GenericSerializerField(model)
        serial_data = serializer(obj, data=d,partial=True)
        if serial_data.is_valid():
            serial_data.save()
            return JsonResponse(serial_data.data)
            # return Response(serial_data.data)
        return JsonResponse(serial_data.errors,status=status.HTTP_400_BAD_REQUEST)
        # return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request,app,model,id):
        parser_classes = [parsers.JSONParser]
        if not request.GET.get('field') and id:
            model = apps.get_model(app,model)
            obj = model.objects.get(id=id)
            obj.delete()
            msg={}
            msg['message']="Deleted Successfully!!"
            return JsonResponse({"Received Data" : dict(json.loads(msg))},status=status.HTTP_204_NO_CONTENT)
            # return Response(status=status.HTTP_204_NO_CONTENT)

        elif request.GET.get('field') and id:
            model = apps.get_model(app,model)
            obj = model.objects.get(id=id)
            for i in request.GET.get('field').split(','):
                print(i)
                setattr(obj,i,None)
                obj.save()
            msg={}
            msg['message']= "Deleted Successfully!!1"
            # json_str = json.dumps(msg)
            return JsonResponse({"Received data" : msg})
            # return Response("success")

        else:
            d = json.loads(request.body)
            dict_mapp = dict(d)
            model = apps.get_model(app,model)
            for key,val in dict_mapp.items():
                print(key,val)
            model.objects.filter(**dict_mapp).delete()
            return JsonResponse({"Received data": dict_mapp})
            # return Response({'Received data': request.data})


class LoginView(APIView):
    def post(self,request):
        requests_logger.log.info("New Request Coming --> "+str(request.data))
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            if user:
                login(request,user)
                requests_logger.log.info(str(user)+"Logged in Succesfully!!")
                token,created = Token.objects.get_or_create(user=user)
                token_logger.log.info(user,token.key)
                token_logger.log.info(str(user)+"-->"+str(token.key))
                return Response({"Your Token":token.key},status=200)

            else:
                return Response("Given User is not valid !!! Either wrong Credentials!!!!!!!")

        else:
            return Response("Plz Give Both the Credentials!!!")


class LogoutView(APIView):
    authentication_classes =[TokenAuthentication]

    def post(self,request):
        logout(request)
        return Response("User Logged OUT!!!!!!")



















