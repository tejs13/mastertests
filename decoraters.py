"""
Create Decorators for Various
Requests methods i.e GET,POST,PUT,DELETE
"""
import functools
from api.logger_directory import requests_logger, user_logger
from api.models.Audit_trails import Audit

REQ_LOGS = requests_logger()
USER_LOGS = user_logger()


def SpecificDecorator(func):
    """
    Decorator for GenericMaster Class to Differentitiate
    Specific data requests and to fetch the Common Variables Commonly
    """
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        id = kwargs.get('id')
        if app and model and id:
            return func(self, request, app, model, id)
        else:
            return func(self, request, app, model)

    return wrapper


def ListViewDecorator(func):
    """
    Decorator for ListView Class
    to fetch all the Common variabls Commonly
    """

    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        list = kwargs.get('list')
        if app and model and list:
            return func(self, request, app, model)
        else:
            return func(self, request, app, model)

    return wrapper


def Logger_create(func):
    """
    Common Decorator for Both view Classes
    to create LOGS in the File
    """
    @functools.wraps(func)
    def wrap(self, request, *args, **kwargs):
        if kwargs.get('id'):
            REQ_LOGS.info(
                func.__name__.upper() + " by " + " --> " + str(request.user) + " for id = " + str(kwargs.get('id')))
        else:
            REQ_LOGS.info(func.__name__.upper() + " by " + " --> " + str(request.user))
        return func(self, request, *args, **kwargs)

    return wrap


def audit_log_id(org, updated, request, app, model, id):
    """
    Common Audit Log For ListView and Genericmaster Class Views
    for DATA manipulation requests
    i.e POST , DELETE , PUT
    """
    if request.method == "PUT":
        d = {}
        d['ACTION'] = "UPDATE"
        d['ID'] = id
        d['ORIGINAL'] = org
        # print(d['Original'])
        d['UPDATED'] = updated
        # print(d['Updated'])
        audit_obj = Audit(App=app, Module=model, View="staticfornow", User=request.user, Modifiers=d)
        audit_obj.save()

    elif request.method == "DELETE":
        d = {}
        d['ACTION'] = "DELETE"
        d['ID'] = id
        d['DATA'] = org
        audit_obj = Audit(App=app, Module=model, View="staticfornow", User=request.user, Modifiers=d)
        audit_obj.save()


def audit_log_list(org, request, app, model):
    if request.method == "POST":
        d = {}
        d['ACTION'] = request.method.upper()
        d['DATA'] = org
        audit_obj = Audit(App=app, Module=model, View="staticfornow", User=request.user, Modifiers=d)
        audit_obj.save()

    elif request.method == "DELETE":
        d = {}
        d['ACTION'] = "DELETE"
        d['Id'] = "CONDITIONAL DELETE"
        d['DATA'] = org
        audit_obj = Audit(App=app, Module=model, View="staticfornow", User=request.user, Modifiers=d)
        audit_obj.save()


def User_Logger_create(func):
    """
    Decorator for Login And Logout View Class to create logs of the
    New and Authenticated User
    """
    @functools.wraps(func)
    def wrap(self, request, *args, **kwargs):
        req_dict = request.data
        USER_LOGS.info(
            "Data by " + func.__name__.upper() + " for Incoming Login Request " + " --> " + str(req_dict['username']))
        return func(self, request, *args, **kwargs)

    return wrap
