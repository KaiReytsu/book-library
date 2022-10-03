import uuid

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    user_image = models.ImageField(verbose_name='Изображение профиля', upload_to = 'user_img', null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, null=True, blank=True)
    biography = models.CharField(verbose_name='Опишите себя', max_length=140, null=True, blank=True)

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
        RESERVED = 'reserved', gettext_lazy('забронировано')
        ISSUED = 'issued', gettext_lazy('выдано')
        CLOSED = 'closed', gettext_lazy('возвращено')
        OVERDUE = 'overdue', gettext_lazy('просрочено')
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=50)
    user = models.ForeignKey(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Забронированная книга', on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(verbose_name='Дата бронирования')
    date_of_return = models.DateTimeField(verbose_name='Дата возврата')
    status = models.CharField('Статус бронирования', max_length=10, choices=Status.choices, default=Status.RESERVED)


# class BookRating(models.Model):
#     class Meta:
#         verbose_name = 'Оценка книги'
#         verbose_name_plural = 'Оценки книг'

#     user = models.ForeignKey(User, verbose_name='Оценка от пользователя', on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, verbose_name='Оценка для книги', on_delete=models.CASCADE)
#     grade = models.PositiveIntegerField('Оценка')

# class FavouritesBooks(models.Model):
#     class Meta:
#         verbose_name = 'Избранная книга'
#         verbose_name_plural = 'Избранные книги'
    
#     user = models.ForeignKey(User, verbose_name='Избранное пользователя', on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, verbose_name='Избранная книга', on_delete=models.CASCADE)

# class FavouritesAuthor(models.Model):
#     class Meta:
#         verbose_name = 'Избранный автор'
#         verbose_name_plural = 'Избранные авторы'
    
#     user = models.ForeignKey(User, verbose_name='Избранное пользователя', on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, verbose_name='Избранный автор', on_delete=models.CASCADE)
    
# class FavouritesGenre(models.Model):
#     class Meta:
#         verbose_name = 'Избранный жанр'
#         verbose_name_plural = 'Избранные жанры'
    
#     user = models.ForeignKey(User, verbose_name='Избранное пользователя', on_delete=models.CASCADE)
#     genre = models.ForeignKey(Genre, verbose_name='Избранный жанр', on_delete=models.CASCADE)

User._meta.get_field('email')._unique = True