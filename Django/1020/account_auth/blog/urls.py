# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.postlist, name='postlist'),
    path('register/', views.userregister, name='userregister'),
    path('login/', views.userlogin, name='userlogin'),
]