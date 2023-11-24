from django.urls import path
from .views import MyAPIView

urlpatterns = [
    # ... 기존 URL 패턴들
    path('my-api-view/', MyAPIView.as_view(), name='my-api-view'),
]