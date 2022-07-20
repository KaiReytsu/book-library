from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField()

    class Meta:
        model = Book
        fields = ('book_name', 'author')