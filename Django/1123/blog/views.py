from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def postlist(request):
    posts = [
        {'title':'1', 'content':'111'},
        {'title':'2', 'content':'222'},
        {'title':'3', 'content':'333'},
    ]
    serializer = posts
    return Response(serializer)

@api_view(['POST'])
def a(request):
    posts = [
        {'title':'1', 'content':'111'},
        {'title':'2', 'content':'222'},
        {'title':'3', 'content':'333'},
    ]
    serializer = posts
    return Response(serializer)

@api_view(['GET', 'POST'])
def b(request):
    # 만약 요청이 GET이면
    if request.method == 'GET':
        posts = [
            {'title':'GET!', 'content':'GET!!'},
        ]
        serializer = posts
        return Response(serializer)
    # 만약 요청이 POST면
    elif request.method == 'POST':
        posts = [
            {'title':'POST!', 'content':'POST!!'},
        ]
        serializer = posts
        return Response(serializer)
    
@api_view(['GET', 'PUT', 'DELETE'])
def c(request, pk):
    # 만약 요청이 GET이면
    if request.method == 'GET':
        posts = [
            {'title':f'{pk} GET!', 'content':'GET!!'},
        ]
        serializer = posts
        return Response(serializer)
    # 만약 요청이 PUT이면
    elif request.method == 'PUT':
        posts = [
            {'title':f'{pk} PUT!', 'content':'PUT!!'},
        ]
        serializer = posts
        return Response(serializer)
    # 만약 요청이 DELETE이면
    elif request.method == 'DELETE':
        posts = [
            {'title':f'{pk} DELETE!', 'content':'DELETE!!'},
        ]
        serializer = posts
        return Response(serializer)
    
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=1000)

@extend_schema(
    methods=['POST'], 
    request=PostSerializer,
    responses={200: PostSerializer}
)
@api_view(['POST'])
def d(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        # 요청 데이터 처리
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)