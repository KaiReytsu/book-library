# Generated by Django 4.1 on 2022-10-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_repository', '0006_alter_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='hash',
            field=models.CharField(default='', max_length=5, unique=True, verbose_name='Номер бронирования'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('забронировано', 'забронировано'), ('выдано', 'выдано'), ('возвращено', 'возвращено'), ('просрочено', 'просрочено'), ('испорчено', 'испорчено')], default='забронировано', max_length=20, verbose_name='Статус бронирования'),
        ),
    ]