from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),  # 실제로는 blog/
    path('<int:pk>/', views.post, name='post'), # 실제로는 blog/1, blog/2, blog/3...
    path('bookinfo/', views.bookinfo, name='bookinfo'),
]