from django.urls import path
from .views import *

app_name ='map'

urlpatterns = [

    path('',list,name='list'), #모두 보기
    path("mine/", mine, name="mine"),  # 내 것만
]