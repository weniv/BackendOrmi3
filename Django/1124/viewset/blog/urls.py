from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet

router = DefaultRouter()
router.register(r'my-model', MyModelViewSet, basename='my-model')

urlpatterns = [
    # ... 기존 URL 패턴들
    path('', include(router.urls)),
]