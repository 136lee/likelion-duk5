from django.urls import path
from .views import *
app_name="post"

urlpatterns = [
    path('matching/<int:pk>/', matching, name="matching"),
    path('ai-feedback/<int:post_id>/', ai_feedback, name="ai_feedback"),
    path("recom-now/<int:post_id>/", recom_now, name="recom_now"),
    path("recom-later/<int:post_id>/", recom_later, name="recom_later"),
    path("post-detail/<int:post_id>/", post_detail, name="post_detail"),
    path("create/", create, name="create"),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>/' , delete, name="delete"),
    path("ai/photo/", ai_photo, name="ai_photo"),
]