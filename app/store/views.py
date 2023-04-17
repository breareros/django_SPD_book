from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from store.models import Book
from store.serializers import BookSerializer


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'price']  # Не как в видео! Другая версия Django
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

class BookGPViewSet(BookViewSet):
    queryset = Book.objects.filter(author_name='Джоан Кэтлин Роулинг')
    ordering_fields = ['price', 'name']
    permission_classes = [IsAuthenticatedOrReadOnly]