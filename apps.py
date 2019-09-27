from django.apps import AppConfig
import sys

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        print("        ###########                 on   START UP      ##################")
        # django.setup()
        from django.core.cache import cache
        from api.models.country import country
        # from api.serializers import LoginSerializer
        # from api.serializers import ReverseStringSerializer
        # serializer = getGenericSerializer(country)
        # cache.set('serial_key',serializer,None)
        cache.set('key',"mycache",None)
        cache.set('model_key',country,None)



















