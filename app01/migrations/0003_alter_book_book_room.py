# Generated by Django 4.1.4 on 2023-04-10 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_room_user_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.room', verbose_name='会议室名称'),
        ),
    ]
