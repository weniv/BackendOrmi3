from .models import Post
from .serializers import PostSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterView(generics.CreateAPIView): #CreateAPIView는 post요청을 받아서 새로운 객체를 생성
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

userregister = RegisterView.as_view()

class PostListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return Response(serializer.data)
    def post(self, request):
        # request에 headers에 있는 Authorization: Bearer ${token}로 넘어온 토큰 확인하여 post 처리
        print(request.headers)
        print(request.headers['Authorization'])
        print(request.headers['Authorization'].split(' ')[1])
        token = request.headers.get('Authorization', None)
        print(token)
        if token:
            print('토큰 존재!')
            try:
                token_key = token.split()[1]
                # 유효한 토근인지 확인합니다. 아래 코드에서 token이 유효하지 않으면 애러 발생하면 except로 넘어갑니다.
                token = Token.objects.get(key=token_key)
                print('사용자:', token.user.username)
            except:
                print('토큰이 유효하지 않습니다.')
                return Response({'error':'애러야!!'}, status=400)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
postlist = PostListAPIView.as_view()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # 유효성 검사
        token = serializer.validated_data
        return Response({
            'token': token.key,
        }, status=status.HTTP_200_OK)
    
userlogin = LoginView.as_view()