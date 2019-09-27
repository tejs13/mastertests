from django.http import request
from logger import *
# from .views import ListViewDetail
import inspect
import os
import functools
from .logger_directory import requests_logger
# try:
#     os.mkdir(os.path.join(os.getcwd(), 'API_REQUESTS_LOGS'))
#     print("Directory Created")
# except FileExistsError as e:
#     print('Directory already in existance')
# requests_logger=logger_create(os.path.join(os.getcwd(),'API_REQUESTS_LOGS'))
req_logs = requests_logger()

def SpecificDecorator(func):
    def wrapper(self,request,*args,**kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        id = kwargs.get('id')
        # list = kwargs.get('list')
        # if args:
        #     list = True
        #     post = True
        # else:
        #     list = False
        #     post = False
        # post = kwargs.get('post')
        print(app,model,id)
        print("In Wrapper")
        # res = func(self,request,app,model,id)
        # print("wrapper result down")
        # print(res)

        if app and model and id:
            print("in IF wrapper")
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


# @functools.wraps(ListViewDecorator)
def Logger_create(func):
    # @functools.wraps(func)
    def wrap(self,request,*args,**kwargs):
        print("in logger create wrapper")
        #
        # try:
        #     os.mkdir(os.path.join(os.getcwd(),'API_REQUESTS_LOGS'))
        #     print("Directory Created")
        # except FileExistsError as e:
        #     print('Directory already in existance')
        # requests_logs = logger_create(os.path.join(os.getcwd(),'API_REQUESTS_LOGS'))

        # call_obj = stack[1][0].f_locals["self"]
        name = func.__name__
        print(name)

        # print(stack)
        # print(str(call_obj))
        # print(dir(call_obj))
        req_logs.log.info( name.upper() + " by " + " --> " + str(request.user))
        return func(self,request,*args,**kwargs)


    return wrap



