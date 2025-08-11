from django.urls import path
from .views import *

app_name = "post"
urlpatterns = [
    path("create/", create, name="create"),
]