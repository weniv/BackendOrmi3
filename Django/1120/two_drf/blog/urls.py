from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet)

urlpatterns = [
    # path('post/', views.post_list),
    # path('post/<int:pk>/', views.post_detail),
    path('', include(router.urls)),
]