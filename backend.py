# pylint: disable = E0401,R0903

"""
Backend for Portable User Authentication
for API requests other than Django
"""
from django.contrib.auth.models import User
from rest_framework import authentication
from .decoraters import USER_LOGS
from django_auth_ldap.backend import LDAPBackend


class ExampleAuthentication(authentication.BaseAuthentication):
    """
    rest_framework Custom Authentication Class
    for Incoming API requests
    """

    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        password = request.META.get('HTTP_X_PASSWORD')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
            if user:
                USER_LOGS.info("Got the Django USER", user)
                return (user, None)
        except User.DoesNotExist:
            USER_LOGS.error("Error creating User or User doesnt exist !!")
            if username == password[::-1]:
                USER_LOGS.info("creating the new USER with given uname and password")
                user = User.objects.create_user(username=username, password=username[::-1])
                USER_LOGS.info("New USER created", user)
                return (user, None)

            return None


def custom_authenticate(username=None, password=None):
    """
    Custom Django User Authentication
    for Token Genearation
    """
    try:
        if password == username[::-1]:
            user = User.objects.create_user(username=username, password=username[::-1])
            return user
    except User.DoesNotExist:
        return None


#
class CustomLDAPBackend(LDAPBackend):

    def authenticate_ldap_user(self, username, password):

        user = LDAPBackend.authenticate(username,password)
        if user:
            print(" #######################  ",user)
            print(" ###############   in  CUSTOM LDAP")

            return user
        else:
            print("&&&&&&&&&&&&&&&&&&&    errrorrrr    ")