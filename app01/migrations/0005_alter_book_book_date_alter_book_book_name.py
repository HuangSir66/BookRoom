# Generated by Django 4.1.4 on 2023-04-10 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_book_book_name_alter_book_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_date',
            field=models.DateField(verbose_name='预约日期'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user'),
        ),
    ]
