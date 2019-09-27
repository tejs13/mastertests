#pylint: disable = C0301,E0401,C0103
""" URLS for the API Access"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from api.views import GenericMaster, LoginView, LogoutView, \
    ListViewDetail, CityTestView, Exe_Test_View



urlpatterns = [

    path('admin/', admin.site.urls),
    path('master/accounts/login/', auth_views.LoginView.as_view()),
    # URL for login and Token Generation
    path('master/login', LoginView.as_view(), name='login'),
    # URL for logout
    path('master/logout', LogoutView.as_view(), name='logout'),
    # spicific operation URL
    path('master/<str:app>.<str:model>/<int:id>', GenericMaster.as_view(), name='master_specific_operate'),
    # URL for actual POST
    path('master/<str:app>.<str:model>', GenericMaster.as_view(), name='master_post'),
    # URL for all the LIST Operations
    path('master/<str:app>.<str:model>/<str:list>', ListViewDetail.as_view(), name='master_post_get_filter'),
    # URL for  Nested Serializer
    path('master/citytest/<str:app>.<str:model>', CityTestView.as_view(), name='citytest'),
    # URL for test
    path('master/exe', Exe_Test_View.as_view(), name='exetest')
# path('master/meta', BookViewSet.as_view(), name='meta')


]
