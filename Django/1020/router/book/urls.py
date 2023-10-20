from django.urls import path, include
from rest_framework.routers import DefaultRouter # default router는 기능 많고요. simple router는 기능 적어요.
from .views import BookViewSet

router = DefaultRouter()
router.register('', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]