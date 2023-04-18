import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book1 = Book.objects.create(name="Гарри Поттер и философский камень", price=1000,
                                         author_name='Джоан Кэтлин Роулинг', owner=self.user)
        self.book2 = Book.objects.create(name="Гарри Поттер и Тайная комната", price=1100,
                                         author_name='Джоан Кэтлин Роулинг', owner=self.user)
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
                                         author_name='Владимир Дронов', owner=self.user)
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

    def test_create(self):
        self.assertEqual(10, Book.objects.all().count())
        url = reverse('book-list')
        data = {"name": "Programming in Python 3",
                "price": "1500.00",
                "author_name": "Mark Summerfield"}
        json_data = json.dumps(data)

        self.client.force_login(user=self.user)

        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        print(f"{response.data=}")
        self.assertEqual(11, Book.objects.all().count())
        print(Book.objects.last().owner)
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {"name": self.book1.name,
                "price": 9500.00,
                "author_name": self.book1.author_name}
        json_data = json.dumps(data)

        self.client.force_login(user=self.user)

        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book1 = Book.objects.get(id=self.book1.id) == self.book1.refresh_from_db()
        self.book1.refresh_from_db()
        self.assertEqual(9500, self.book1.price)
        print(f"{response.data=}")

    def test_update_not_owner(self):
        print(f"test_update_not_owner: ")
        self.user2 = User.objects.create(username='test_username_2')
        url = reverse('book-detail', args=(self.book2.id,))
        data = {"name": self.book2.name,
                "price": 9500,
                "author_name": self.book2.author_name}
        json_data = json.dumps(data)

        self.client.force_login(user=self.user2)

        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book2.refresh_from_db()
        self.assertEqual(1100, self.book2.price)
        print(f"{data=}\n{response.data=} \n{self.book2.price=}")

    def test_update_not_owner_but_stuff(self):
        print(f"test_update_not_owner_but_stuff:")
        self.user2 = User.objects.create(username='test_username_2', is_staff=True)
        url = reverse('book-detail', args=(self.book2.id,))
        data = {"name": self.book2.name,
                "price": 9500,
                "author_name": self.book2.author_name}
        json_data = json.dumps(data)

        self.client.force_login(user=self.user2)

        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book2.refresh_from_db()
        self.assertEqual(9500, self.book2.price)
        print(f"{response.data=}")

    def test_delete(self):
        self.assertEqual(10, Book.objects.all().count())
        url = reverse('book-detail', args=(10,))

        self.client.force_login(user=self.user)

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        print(f"{response.data=}")
        self.assertEqual(9, Book.objects.all().count())

    def test_delete_not_owner(self):
        self.user = User.objects.create(username='test_username_2')
        self.assertEqual(10, Book.objects.all().count())
        url = reverse('book-detail', args=(10,))

        self.client.force_login(user=self.user)

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        print(f"{response.data=}")
        self.assertEqual(10, Book.objects.all().count())

    def test_delete_not_owner_but_stuff(self):
        self.user = User.objects.create(username='test_username_2', is_staff=True)
        self.assertEqual(10, Book.objects.all().count())
        url = reverse('book-detail', args=(10,))

        self.client.force_login(user=self.user)

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        print(f"{response.data=}")
        self.assertEqual(9, Book.objects.all().count())