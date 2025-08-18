from django.urls import path
from .views import *

app_name = "explore"

urlpatterns = [
    path("chat_ai/", chat_ai, name="chat_ai"),
    path("chat_api/", chat_ai, name="chat_api"),
]


