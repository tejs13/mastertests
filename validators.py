#pylint: disable = R0903,E0401
"""
Validators Hooks Classes
for Various FIELDS as Per
the Requirements
"""
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from .decoraters import REQ_LOGS


class CharOnly():
    """Validators Hooks for the FIELDS of the model"""
    # def __init__(self, base):
    #     self.base = base
    def __call__(self, value):
        try:
            req_data = dict(value)
            if not req_data:
                raise ParseError("Invalid JSON for PUT")
        except ParseError:
            REQ_LOGS.error("Invalid JSON for PUT")
            return Response("Invalid JSON")
        if not req_data['name'].isalpha():
            message = "The Data should be Characters ONly"
            raise serializers.ValidationError(message)
        return value


class UpperCaseOnly():
    """Validators hooks For the FIELDS of the Model"""
    def __call__(self, value):
        try:
            req_data = dict(value)
            if not req_data:
                raise ParseError("Invalid JSON")
        except ParseError:
            REQ_LOGS.error("Invalid JSON for PUT")
            return Response("Invalid JSON")
        if not req_data['code'].isupper():
            message = "The Code should be in UPPERCASE ONly"
            raise serializers.ValidationError(message)
        return value

# def test(value):
#     d = value
#     print(" ##########################     in TEST")
#     print(d)
#     if not d['name'].isalpha():
#         message = "The Data should be Characters ONly"
#         raise serializers.ValidationError(message)
#     return d
