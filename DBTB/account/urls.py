from django.urls import path
from .views import *

app_name='account'

urlpatterns=[
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('mypage/', mypage, name='mypage'),
    path('mypost/', mypost, name='mypost'),
    path('user-info/', user_info, name='user-info'),
    path('myscrap/', myscrap, name='myscrap'),
    #path('mytodo/', mytodo, name="mytodo")
]