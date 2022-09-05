# Generated by Django 4.1 on 2022-09-01 18:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100, verbose_name='Авторы')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('date_of_death', models.DateField(blank=True, null=True, validators=[django.core.validators.RegexValidator('((0?[1-9])|([12]\\d)|(3[01]))\\.((0?[1-9])|(1[0-2]))\\.(1[0-9]{3})|(20[01]\\d)|(202[0-2])')], verbose_name='Дата смерти')),
                ('author_photo', models.ImageField(blank=True, null=True, upload_to='author_img/', verbose_name='Фотография автора')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('book_description', models.CharField(max_length=1000, verbose_name='Описание книги')),
                ('book_image', models.ImageField(blank=True, null=True, upload_to='book_img/', verbose_name='Обложка книги')),
                ('isbn', models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='ISBN')),
                ('books_in_stock', models.PositiveIntegerField(verbose_name='Количество книг в библиотеке')),
                ('publication_year', models.PositiveIntegerField(verbose_name='Год публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_repository.author', verbose_name='Автор книги')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['book_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=50, verbose_name='Жанры')),
                ('genre_description', models.CharField(max_length=140, verbose_name='Описание жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Язык',
                'verbose_name_plural': 'Языки',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher_name', models.CharField(max_length=100, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Издательство',
                'verbose_name_plural': 'Издательства',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='user_img', verbose_name='Изображение профиля')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('biography', models.CharField(blank=True, max_length=140, null=True, verbose_name='Опишите себя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_of_issue', models.DateTimeField(verbose_name='Дата бронирования')),
                ('date_of_return', models.DateTimeField(verbose_name='Дата возврата')),
                ('status', models.CharField(choices=[('reserved', 'забронировано'), ('issued', 'выдано'), ('closed', 'возвращено'), ('overdue', 'просрочено')], default='reserved', max_length=10, verbose_name='Статус бронирования')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_repository.book', verbose_name='Забронированная книга')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='book_repository.genre', verbose_name='Жанры'),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_language',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.CASCADE, to='book_repository.language', verbose_name='Язык издания'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_repository.publisher', verbose_name='Издательство'),
        ),
    ]
