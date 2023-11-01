from django.db import models

# Create your models here.
class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    def __str__(self):
        return self.username

class User(models.Model):
    """用户表"""
    name=models.CharField(verbose_name='姓名',max_length=32)
    username = models.CharField(verbose_name='账号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    def __str__(self):
        return self.name

class Room(models.Model):
    """会议室"""
    room = models.CharField(verbose_name='会议室名称', max_length=32)
    num = models.IntegerField(verbose_name='容纳人数')
    def __str__(self):
        return self.room
class Book(models.Model):
    """预约"""
    username = models.ForeignKey(to="User",on_delete=models.CASCADE,verbose_name='用户名')
    room = models.ForeignKey(to = 'Room', to_field='id', null=True, blank=True, on_delete=models.SET_NULL,verbose_name='会议室名称')
    date = models.DateField(verbose_name='预约日期')
    time_choies=(
        (1,'8:00-9:00'),
        (2,'9:00-10:00'),
        (3,'10:00-11:00'),
        (4,'11:00-12:00'),
        (5,'12:00-13:00'),
        (6,'13:00-14:00'),
        (7,'14:00-15:00'),
        (8,'15:00-16:00'),
        (9,'16:00-17:00'),
        (10,'17:00-18:00'),
        (11,'18:00-19:00'),
        (12,'19:00-20:00'),
        (13,'20:00-21:00'),
        (14,'21:00-22:00'),
        (15,'22:00-23:00'),
    )
    time = models.IntegerField(verbose_name='预约时间',choices=time_choies)


