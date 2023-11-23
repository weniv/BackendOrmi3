from django.urls import path
from . import views

urlpatterns = [
    path('', views.postlist, name='postlist'),
    path('a/', views.a, name='a'),
    path('b/', views.b, name='b'),
    path('c/<int:pk>/', views.c, name='c'),
    path('d/', views.d, name='d'),
]