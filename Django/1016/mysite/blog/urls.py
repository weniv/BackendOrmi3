from django.urls import path
from . import views

urlpatterns = [
    path('', views.postlist, name='postlist'),
    path('<int:pk>/', views.postdetail, name='postdetail'),
    path('write/', views.write, name='write'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('test/', views.test, name='test'),
]