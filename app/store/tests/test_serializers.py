from unittest import TestCase
# from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTEstCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name="Гарри Поттер и философский камень", price=1000, author_name='Джоан Кэтлин Роулинг')
        book2 = Book.objects.create(name="Гарри Поттер и Тайная комната", price=1100, author_name='Джоан Кэтлин Роулинг')
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Гарри Поттер и философский камень',
                'price': '1000.00',
                'author_name' : 'Джоан Кэтлин Роулинг',
            },
            {
                'id': book2.id,
                'name': 'Гарри Поттер и Тайная комната',
                'price': '1100.00',
                'author_name': 'Джоан Кэтлин Роулинг',
            },
        ]

        self.assertEqual(expected_data, data)