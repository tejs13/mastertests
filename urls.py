from django.contrib import admin
from django.urls import path, include

from rest_framework import renderers

from .views import GenericMaster


# master_list = GenericMaster.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# question_list = QuestionsViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })



urlpatterns = [
    path('master/<str:app>/<str:model>/', GenericMaster.as_view(), name='master_list-api'),
    
]

