from django.urls import path
from .views import *

app_name = "post"
urlpatterns = [
    path("create/", create_post, name="create"),
    path("place/<int:place_id>/", list_by_place, name="list_by_place"),
]