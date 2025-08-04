from django.urls import path,include
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', main , name='main'),
    path('detail/<int:post_id>/', detail, name='detail'),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>/' , delete, name="delete"),
    path('comments-delete/<int:comment_id>/' , delete_comment, name="delete_comment"),
    path('create-comment/<int:post_id>' , create_comment, name='create-comment'),
    path('category/<slug:slug>/', category, name='category'),
    path('like/<int:post_id>/', like , name='like'),
    path('scrap/<int:post_id>/', scrap , name='scrap'),
]

