# Generated by Django 4.1.4 on 2023-04-07 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=32, verbose_name='会议室名称')),
                ('num', models.IntegerField(verbose_name='容纳人数')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('username', models.CharField(max_length=32, verbose_name='账号')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_date', models.DateField()),
                ('time', models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '13:00'), (7, '14:00'), (8, '15:00'), (9, '16:00'), (10, '17:00'), (11, '18:00'), (12, '19:00'), (13, '20:00'), (14, '21:00'), (15, '22:00')], verbose_name='预定时间序列')),
                ('book_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
                ('book_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.room')),
            ],
        ),
    ]
