from django.urls import path
from .views import *

app_name="feed"

urlpatterns=[
    path("test/", test, name="test"),
    path("", feed, name="feed_all"),              # 전체
    path("<str:dong>/", feed, name="feed_by_dong"),  # 동별
    path("<int:post_id>/scrap/", scrap, name="scrap"),
]