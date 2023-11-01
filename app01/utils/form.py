from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from django import forms
from app01.utils.encrypt import md5


class RoomModelForm(BootStrapModelForm):
    room = forms.CharField(min_length=3, label='会议室名')
    class Meta:
        model = models.Room
        fields = '__all__'


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(label='用户名')
    username = forms.CharField(min_length=8,label='账号')
    # password = forms.CharField(
    #     label='密码',
    #     widget=forms.PasswordInput(render_value=True),
    #     # min_length=8
    #     # validators=[RegexValidator("(.*[0-9]{1,}.*)(.*[a-zA-Z]{1,}.*)", '密码格式错误，必须包含数字以及字母')],
    # )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.User
        fields = '__all__'
        widgets = {
            "password": forms.PasswordInput(render_value=True),
            'confirm_password':forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if len(pwd)<8:
            raise ValidationError('密码长度至少为8位')
        Shu,Mu=[],[]
        for i in pwd:
            if i.isdigit():Shu.append(i)
            if i.isalpha():Mu.append(i)
        if Shu==[] or Mu==[]:
            raise ValidationError('密码需为字母与数字的组合')
        return md5(pwd)
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致，请重新输入')
        return confirm

class UserEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.User
        fields = ['name']
class BookModelForm(BootStrapModelForm):
    class Meta:
        model = models.Book
        # exclude = ['book_name']
        fields ='__all__'
    def clean_time(self):
        room = self.cleaned_data.get('room')
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        exit = models.Book.objects.filter(date=date,room=room,time = time).exists()
        if exit:
            raise ValidationError('您所选的时间段已被选')
        return time

class UserBookModelForm(BootStrapModelForm):
    class Meta:
        model = models.Book
        exclude = ['username']
        # fields ='__all__'
    def clean_time(self):
        room = self.cleaned_data.get('room')
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        exit = models.Book.objects.filter(date=date,room=room,time = time).exists()
        if exit:
            raise ValidationError('您所选的时间段已被选')
        return time