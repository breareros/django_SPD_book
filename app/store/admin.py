from django.contrib import admin

from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'author_name')
    list_display_links = ('id', 'name', 'price', 'author_name')
    search_fields = ('id', 'name', 'price', 'author_name')

@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    pass