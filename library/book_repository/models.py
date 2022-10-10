import hashlib
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy


class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    author_name = models.CharField('Авторы', max_length=100)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)
    author_photo = models.ImageField(verbose_name='Фотография автора',upload_to = 'author_img/', null=True, blank=True)
    def __str__(self):
        return self.author_name

class Genre(models.Model):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    genre_name = models.CharField('Жанры', max_length=50)
    genre_description = models.CharField('Описание жанра', max_length=140)
    
    def __str__(self):
        return self.genre_name

class Publisher(models.Model):
    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

    publisher_name = models.CharField('Наименование', max_length=100)
    
    def __str__(self):
        return self.publisher_name

class Language(models.Model):
    class Meta:
            verbose_name = 'Язык'
            verbose_name_plural = 'Языки'
    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Book(models.Model):
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['book_name']
    
    book_name = models.CharField('Наименование', max_length=100)
    book_description = models.CharField('Описание книги', max_length=1000)
    book_image = models.ImageField(verbose_name='Обложка книги',upload_to = 'book_img/', null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13,  unique=True, null=True, blank=True)
    books_in_stock = models.PositiveIntegerField('Количество книг в библиотеке')
    publication_year = models.PositiveIntegerField('Год публикации')
    publication_language = models.ForeignKey(Language, verbose_name='Язык издания', max_length=20, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, verbose_name='Автор книги', on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, verbose_name='Издательство', on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    
    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.genre_name for genre in self.genre.all()[:3]])

    def __str__(self):
        return self.book_name

class Reservation(models.Model):
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    class Status(models.TextChoices):
        RESERVED = 'забронировано', gettext_lazy('забронировано')
        ISSUED = 'выдано', gettext_lazy('выдано')
        CLOSED = 'возвращено', gettext_lazy('возвращено')
        OVERDUE = 'просрочено', gettext_lazy('просрочено')
    
    user = models.ForeignKey(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Забронированная книга', on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(verbose_name='Дата бронирования')
    date_of_return = models.DateTimeField(verbose_name='Дата возврата')
    status = models.CharField('Статус бронирования', max_length=20, choices=Status.choices, default=Status.RESERVED)
    hash = models.CharField(default='',
                            max_length=5, 
                            unique=True)
    def save(self, *args, **kwargs):
        self.hash = hashlib.md5((str(self.id) +
                                str(self.user) + 
                                str(self.book) + 
                                str(self.date_of_issue) + 
                                str(self.date_of_return)
                                ).encode('utf-8')).hexdigest()[-5:]
        return super().save(*args, **kwargs)
        
User._meta.get_field('email')._unique = True