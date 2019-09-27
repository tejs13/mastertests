from django.http import request
import json

def audit_post(request):
    d={}
    d['Action'] = request.method.upper()
    d['Data'] = json.loads(request.body.decode('utf8'))
    return d

def audit_delete_id(request,*args,**kwargs):
    d={}
    d['Action'] = request.method.upper()
    d['id'] = kwargs.get('id')
    return d

def audit_put(request,*args,**kwargs):
    d={}
    d['Action'] = "UPDATE"
    d['id'] = kwargs.get('id')

    return d




