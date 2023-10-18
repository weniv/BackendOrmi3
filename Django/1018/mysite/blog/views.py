from django.shortcuts import render
from .models import Post
from django.http import JsonResponse
# rest_framework 추가 후 추가된 코드
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from django.middleware.csrf import get_token
from django.http import HttpResponse


@api_view(['GET', 'POST'])
def postlist(request):
    if request.method == 'GET':
        postlist = Post.objects.all()
        serializer = PostSerializer(postlist, many=True) # 다수의 Queryset을 넘길 때는 many=True
        # return Response(100)
        # return Response('hello world')
        # return Response(postlist) # Queryset을 넘길 때 앞에서 직렬화 하는 코드 있어야 함
        return Response(serializer.data)
        # return HttpResponse(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def csrf(request):
    token = get_token(request)
    return JsonResponse({"csrftoken": token})
