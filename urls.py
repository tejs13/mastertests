from django.contrib import admin
from django.urls import path,include
from api import views
from rest_framework.authtoken.views import obtain_auth_token

# from.views import DetailViewSet
from .views import GenericMaster,LoginView,LogoutView

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('master/login',LoginView.as_view(),name='login'),
    path('master/logout',LogoutView.as_view(),name='logout'),

    path('master/<str:app>.<str:model>/<int:id>', GenericMaster.as_view(), name='master_specific'),

    path('master/<str:app>.<str:model>/', GenericMaster.as_view(), name='master_get'),

    path('master/<str:app>.<str:model>', GenericMaster.as_view(), name='master_post'),

    path('master/<str:app>.<str:model>/<str:list>', GenericMaster.as_view(), name='master_post_filter'),

    path(r'master/<str:app>.<str:model>/<int:id>?<str:field>=(?P<arg>\w+)?$', GenericMaster.as_view(), name='master_delete_fields')

]
