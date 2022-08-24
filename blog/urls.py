from django.urls import path, include
from . import views


urlpatterns = [
    # API to post a comment 
    path('', views.blogHome, name="blogHome"),
    path('postcomment', views.postComment, name='postComment'),
    path('<str:slug>', views.blogPost, name="blogPost"),

]