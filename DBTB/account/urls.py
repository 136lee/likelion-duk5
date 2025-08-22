from django.urls import path
from .views import *

app_name='account'

urlpatterns=[
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('mypage/', mypage, name='mypage'),
    path('user-info/', user_info, name='user-info'),
    #path('mytodo/', mytodo, name="mytodo")
]