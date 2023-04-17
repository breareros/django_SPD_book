from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name="Гарри Поттер и философский камень", price=1000,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book2 = Book.objects.create(name="Гарри Поттер и Тайная комната", price=1100,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book3 = Book.objects.create(name="Гарри Поттер и узник Азкабана", price=1200,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book4 = Book.objects.create(name="Гарри Поттер и Кубок огня", price=1300,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book5 = Book.objects.create(name="Гарри Поттер и Орден Феникса", price=1400,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book6 = Book.objects.create(name="Гарри Поттер и Принц-полукровка", price=1500,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book7 = Book.objects.create(name="Гарри Поттер и Дары Смерти", price=1600,
                                         author_name='Джоан Кэтлин Роулинг')
        self.book8 = Book.objects.create(name="Приключения двух друзей", price=2000,
                                         author_name='Мальцев Станислав Владимирович')
        self.book9 = Book.objects.create(name="Грокаем алгоритмы", price=600,
                                         author_name='Адитья Бхаргава')
        self.book10 = Book.objects.create(name="Django 3.0 Практика создания вею-сайтов на Python", price=700,
                                         author_name='Владимир Дронов')
    def test_get(self):
        url = reverse('book-list')
        print(f"{url}")
        response = self.client.get(url)
        # print(f"{response.data}")
        serializer_data = BookSerializer([self.book1, self.book2, self.book3, self.book4, self.book5, self.book6, self.book7, self.book8, self.book9, self.book10], many=True).data
        # serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(f"{serializer_data=}")
        print(f"{response.data=}")
        self.assertEqual(serializer_data, response.data)

    def test_get_gp(self):
        url = reverse('gp-list')
        print(f"{url}")
        response = self.client.get(url)
        serializer_data = BookSerializer(
            [self.book1, self.book2, self.book3, self.book4, self.book5, self.book6, self.book7], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(f"test_get_gp: {serializer_data=}")
        print(f"test_get_gp: {response.data=}")
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        print(f"{url}")
        response = self.client.get(url, data={'search': 'Грокаем алгоритмы'})
        serializer_data = BookSerializer([self.book9], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(f"test_get_search: {serializer_data=}")
        print(f"test_get_search: {response.data=}")
        self.assertEqual(serializer_data, response.data)