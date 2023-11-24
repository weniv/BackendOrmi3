# blog > views.py

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import PostSerializer

class MyModelViewSet(ViewSet):
    
    @extend_schema(request=PostSerializer, responses={200: PostSerializer})
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(responses={200: PostSerializer})
    def list(self, request):
        # 임시 데이터를 생성하여 반환
        data = [
            {'title': 'Sample Title 1', 'content': 'Sample Content 1'},
            {'title': 'Sample Title 2', 'content': 'Sample Content 2'},
        ]
        return Response(data)

    # 'retrieve', 'update', 'partial_update', 'destroy' 등 다른 액션에 대해서도 유사하게 적용 가능
