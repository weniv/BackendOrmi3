from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:pk>/', views.post, name='post'),
    path('test/', views.test, name='test'),
    path('posttest/<int:pk>/', views.posttest, name='posttest'),
    path('postdel/<int:pk>/', views.postdel, name='postdel'),
]