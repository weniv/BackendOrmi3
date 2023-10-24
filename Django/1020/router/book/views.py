from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = Book.objects.all() # CRUD 대상이 되는 데이터를 지정
    serializer_class = BookSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user) # user는 현재 로그인한 사용자
    # 이렇게 사용할 것이면 model에 user 필드가 있어야 합니다.
