from django.views.generic import FormView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from store.models import Book
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'price']  # Не как в видео! Другая версия Django
    search_fields = ['name', 'author_name']
    search_fields = ['name', 'author_name']


    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


# @login_required(login_url="/login/")
# class BookGPViewSet(LoginRequiredMixin, BookViewSet):
class BookGPViewSet(BookViewSet):
    queryset = Book.objects.filter(author_name='Джоан Кэтлин Роулинг')
    ordering_fields = ['price', 'name']
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    # permission_classes = [IsAuthenticated]


from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
class LDAPLogin(FormView):
    """
    Class to authenticate a user via LDAP and
    then creating a login session
    """
    authentication_classes = ()
    def post(self, request):
        """
        Api to login a user
        :param request:
        :return:
        """
        user_obj = authenticate(username=request.data['username'],
                                password=request.data['password'])
        login(request, user_obj)
        data={'detail': 'User logged in successfully'}
        return Response(data, status=200)

class LDAPLogout(APIView):
    """
    Class for logging out a user by clearing his/her session
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        Api to logout a user
        :param request:
        :return:
        """
        logout(request)
        data={'detail': 'User logged out successfully'}
        return Response(data, status=200)