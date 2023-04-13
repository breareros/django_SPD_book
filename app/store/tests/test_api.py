from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def test_get(self):
        book1 = Book.objects.create(name="Гарри Поттер и философский камень", price=1100.05)
        book2 = Book.objects.create(name="Гарри Поттер и Тайная комната", price=1200.05)
        url = reverse('book-list')
        print(f"{url}")
        response = self.client.get(url)
        print(f"{response.data}")
        serializer_data = BookSerializer([book1, book2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
