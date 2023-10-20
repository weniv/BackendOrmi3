from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() # CRUD 대상이 되는 데이터를 지정
    serializer_class = BookSerializer