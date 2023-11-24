# blog > views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import PostSerializer

class MyAPIView(APIView):

    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer}
    )
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # 요청 데이터 처리
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    @extend_schema(
        parameters=[
            OpenApiParameter(name='param', description='파라미터 설명', required=False, type=str)
        ],
        responses={200: {"description": "성공!!"},}
    )
    def get(self, request):
        param = request.query_params.get('param', None)
        return Response({"message": "GET 요청 처리됨", "param": param})

    # PUT, DELETE 등 다른 메서드에 대해서도 유사하게 적용 가능
