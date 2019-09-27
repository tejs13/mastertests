from django.http import request
from logger import init_logging
import inspect
import os
import json
import functools
import pickle
from .logger_directory import requests_logger,user_logger
from rest_framework.response import Response
from .models import Audit
from . import views


req_logs = requests_logger()
user_logs = user_logger()
# cnt=0
# def inc():
#     global cnt
#     cnt = cnt+1
#     return cnt

def SpecificDecorator(func):
    # global cnt
    # cnt = cnt+1
    @functools.wraps(func)
    def wrapper(self,request,*args,**kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        id = kwargs.get('id')
        print("In Sepicific Decorator Wrapper")
        print(func.__name__)
        if app and model and id:
            print("in IF wrapper")
            # print("the counter variable",cnt)
            # if cnt <= 2:
            #     views.flag=False
            # else:
            #     views.flag=True
            views.flag=False

            return func(self,request,app,model,id)
        else:
            return func(self,request,app,model)
    return wrapper


def ListViewDecorator(func):
    @functools.wraps(func)
    def wrapper(self,request,*args,**kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        list = kwargs.get('list')
        print(app,model,list)
        print("In listview wrapper")
        print(func.__name__)
        if app and model and list:
            return func(self,request,app,model)
        else:
            return func(self,request,app,model)
    return wrapper


def Logger_create(func):
    @functools.wraps(func)
    def wrap(self,request,*args,**kwargs):
        print("In logger create wrapper")
        if kwargs.get('id'):
            req_logs.info(func.__name__.upper() + " by " + " --> " +str(request.user) + " for id = " + str(kwargs.get('id')))
        else:
            print("in logger create wrapper without ID")
            req_logs.info(func.__name__.upper() + " by " + " --> " + str(request.user))
        return func(self,request,*args,**kwargs)
    return wrap



def audit_log(func):
    # @functools.wraps(func)
    def WrapperForAudit(self,request,*args,**kwargs):

        print(func.__name__)
        print(kwargs.get('app'))
        print(kwargs.get('model'))
        print(kwargs.get('id'))
        print("from audit deco " + str(request.user))
        print("from audit the method is" + str(request.method))
        print("from audit the data:" )
        # print(request.body.decode('utf8'))
        # data = request.body.decode('utf8')
        print(request.method)
        # print(data)
        # print(type(data))
        # print(json.loads(data))
        # print(type(json.loads(data)))
        d={}
        if request.method=="POST":
            print("in AUDIT POST")
            d['Action']=request.method.upper()
            d['Data']=json.loads(request.body.decode('utf8'))
            print(d)
            a=Audit(App=kwargs.get('app'),Module=kwargs.get('model'),View="staticfornow",User=request.user,Modifiers=d)
            a.save()
            return func(self, request, *args, **kwargs)
        elif request.method=="DELETE" and kwargs.get('id'):
            print("in AUDIT DELETE with ID")
            id=kwargs.get('id')
            print("Id from If Delete!!!!",id)
            ex=func(self,request,*args,**kwargs)
            print("the ex")
            print(ex)
            print(type(ex))
            d['Action'] = request.method.upper()
            d['id']=id
            d['Data'] = ex
            a=Audit(App=kwargs.get('app'),Module=kwargs.get('model'),View="staticfornow",User=request.user,Modifiers=d)
            a.save()
            return func(self,request,*args,**kwargs)
        elif request.method == "DELETE" and not kwargs.get('id'):
            print("in AUDIT DELETE WITHOUT ID")
            print("the yield generator output")
            data = func(self,request,*args,**kwargs)
            # for i in data:
            #     print(i)
            print(data)
            print(data['req_query'])
            print(data['deleted_data'])
            # req_data = json.loads(data.decode('utf8'))
            d['Action'] = request.method.upper()
            d['id'] = "Conditional Delete"
            d['Data'] = data
            a = Audit(App=kwargs.get('app'),Module=kwargs.get('model'),View="staicfornow",User=request.user,Modifiers=d)
            a.save()
            return func(self,request,*args,**kwargs)

        elif request.method == "PUT":
            print("in PUT audit")
            id = kwargs.get('id')
            data = func(self,request,*args,**kwargs)
            print(data)
            print(data['org_data'])
            print(data['updated_data'])
            d['Action'] = "UPDATE"
            d['id'] = id
            d['Data']= data
            a = Audit(App=kwargs.get('app'),Module=kwargs.get('model'),View="staticfornow",User=request.user,Modifiers=d)
            a.save()
            return func(self,request,*args,**kwargs)
    return WrapperForAudit


def User_Logger_create(func):
    @functools.wraps(func)
    def wrap(self,request,*args,**kwargs):
        req_dict = request.data
        print(req_dict['username'])
        user_logs.info("Data by " + func.__name__.upper() + " for Incoming Login Request " + " --> " + str(req_dict['username']))
        print("in logger create wrapper")
        # name = func.__name__
        # print(name)
        return func(self,request,*args,**kwargs)
    return wrap





