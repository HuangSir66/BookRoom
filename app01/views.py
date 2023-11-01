import datetime

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from app01 import models
from app01.utils.code import check_code
from app01.utils.pagination import Pagination
from app01.utils.encrypt import md5
from app01.utils.form import RoomModelForm, UserModelForm, BookModelForm, UserBookModelForm, UserEditModelForm


# Create your views here.
def admin_list(request):
    """管理员列表"""
    #检查用户是否登录，已登录，继续向下走，未登录，跳转为登录界面
    #用户发来请求，获取cookie随机字符窜，拿着随机字符窜看看session中有没有
    # request.session['info']
    #搜索
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['username__contains'] = search_data


    #根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request,queryset)
    context = {
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
        "search_data":search_data
    }
    return render(request,'admin_list.html',context)



from django import forms
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致，请重新输入')
        return confirm


class AdminResetModelform(BootStrapModelForm):
    # confirm_password = forms.CharField(
    #     label='确认密码',
    #     widget=forms.PasswordInput(render_value=True)
    # )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ['password','confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        #去数据库校验当前的密码是否和新输入的密码一致
        exists = models.Admin.objects.filter(id = self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError('不能与之前的密码相同')
        return md5_pwd
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致，请重新输入')
        return confirm


def admin_add(request):
    """添加管理员"""
    title = '新建管理员'
    if request.method == "GET":
        form = AdminModelForm()
        return render(request,'change.html',{'form':form,'title':title})

    form = AdminModelForm(data= request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request,'change.html',{"form":form,'title':title})


class AdminEditModelForm(BootStrapModelForm):
     class Meta:
         model = models.Admin
         fields = ['username']
def admin_edit(request,nid):
    """编辑管理员"""
    row_object = models.Admin.objects.filter(id = nid).first()
    if not row_object:
        return render(request,'error.html',{'msg':'数据不存在'})
    title = '编辑管理员'
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request,'change.html',{"form":form,'title':title})
    form = AdminEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,'change.html',{'form':form,'title':title})


def admin_delete(request,nid):
    """删除用户"""
    models.Admin.objects.filter(id = nid).delete()
    return redirect("/admin/list/")

def admin_reset(request,nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id = nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = '重置密码 - {}'.format(row_object.username)
    if request.method=="GET":
        form = AdminResetModelform()
        return render(request,'change.html',{'form':form,'title':title})

    form = AdminResetModelform(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request,'change.html',{'form':form,'title':title})

def room_list(request):
    """会议室列表"""
    queryset = models.Room.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, 'room_list.html', context)

def room_add(request):
    """添加会议室"""
    title = '新建会议室'
    if request.method == "GET":
        form = RoomModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = RoomModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/room/list/')
    return render(request, 'change.html', {"form": form, 'title': title})

def room_edit(request,nid):
    """编辑会议室"""
    title = '编辑会议室'
    row_object = models.Room.objects.filter(id=nid).first()
    if request.method == "GET":
        form = RoomModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = RoomModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/room/list/')
    return render(request, 'change.html', {"form": form, 'title': title})

def room_delete(request,nid):
    """删除用户"""
    models.Room.objects.filter(id = nid).delete()
    return redirect("/room/list/")

class UserResetModelform(BootStrapModelForm):
    # confirm_password = forms.CharField(
    #     label='确认密码',
    #     widget=forms.PasswordInput(render_value=True)
    # )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.User
        fields = ['password','confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        #去数据库校验当前的密码是否和新输入的密码一致
        exists = models.User.objects.filter(id = self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError('不能与之前的密码相同')
        return md5_pwd
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致，请重新输入')
        return confirm
def user_reset(request,nid):
    """重置密码"""
    row_object = models.User.objects.filter(id = nid).first()
    if not row_object:
        return redirect('/user/list/')

    title = '重置密码 - {}'.format(row_object.name)
    if request.method=="GET":
        form = UserResetModelform()
        return render(request,'change.html',{'form':form,'title':title})

    form = UserResetModelform(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request,'change.html',{'form':form,'title':title})
def user_delete(request,nid):
    """删除用户"""
    models.User.objects.filter(id = nid).delete()
    return redirect("/user/list/")

def user_edit(request,nid):
    """编辑用户"""
    title = '编辑用户'
    row_object = models.User.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserEditModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = UserEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'change.html', {"form": form, 'title': title})


def user_add(request):
    """添加用户"""
    title = '增加用户'
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'change.html', {"form": form, 'title': title})

def user_list(request):
    """会议室列表"""
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['name__contains'] = search_data
    queryset = models.User.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data':search_data
    }

    return render(request, 'user_list.html', context)

def cheshi(request):
    data_dict = {}
    now_data = datetime.date.today()
    search_data = request.GET.get('q',now_data)
    if search_data:
        data_dict['date__contains'] = search_data
    books = models.Book.objects.filter(**data_dict)
    times = models.Book.time_choies
    rooms = models.Room.objects.all()
    data_list = []
    for time in times:  # 这就是构建表体数据
        data_list.append(mark_safe('<tr><td style="width: 5px">%s</td>' % time[1]))
        for room in rooms:
            for book in books:
                if book.room.id == room.id and time[0] == book.time:
                        tt = mark_safe(
                            '<td rowspan="1" bgcolor="ffcc99"><span >%s</span></td>' % ( book.username.name))
                        break
            else:
                tt = mark_safe('<td ><span></span></td>')
            data_list.append(tt)
        data_list.append('</tr>')
    data = mark_safe(''.join(data_list))
    if request.method == 'GET':
        return render(request,'cesi.html', {"times":times,'rooms':rooms,'data':data,'search_data':search_data})
def book_list(request):
    """会议室预约表"""
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['date__contains'] = search_data
    queryset = models.Book.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }

    return render(request, 'book_list.html', context)

def book_add(request):
    """添加预约"""
    title = '预约'
    if request.method == "GET":
        form = BookModelForm()
        return render(request, 'book_change.html', {'form': form, 'title': title})
    form = BookModelForm(data=request.POST)
    # exsits = models.Book.objects.filter(book_date=data.book_data).exists()
    if form.is_valid():
        form.save()
        return redirect('/cesi/list/')
    return render(request, 'book_change.html', {"form": form, 'title': title})

def book_edit(request,nid):
    """编辑预约"""
    title = '编辑预约'
    row_object = models.Book.objects.filter(id=nid).first()
    if request.method == "GET":
        form = BookModelForm(instance=row_object)
        return render(request, 'book_change.html', {'form': form, 'title': title})

    form = BookModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/book/list/')
    return render(request, 'book_change.html', {"form": form, 'title': title})

def book_delete(request,nid):
    """删除用户"""
    models.Book.objects.filter(id = nid).delete()
    return redirect("/book/list/")

#登录
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(),
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )
    # class LoginModelForm(forms.ModelForm):
    #     class Meta:
    #         model = models.Admin
    #         fields = ['username','password']
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    # print(models.Admin.objects.filter(**form.cleaned_data).first())
    if form.is_valid():
        # 验证成功获取的用户名和密码
        # print(form.cleaned_data)
        #验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code',"")
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        # 数据库校验用户名密码是否正确
        # admin_object = models.Admin.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        user_object = models.User.objects.filter(**form.cleaned_data).first()
        print('管理员：',admin_object)
        print('用户：',user_object)
        if not admin_object and not user_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        # 密码正确
        # 网站生成随机字符串，写入用户浏览器cooki中，希尔session中
        elif admin_object:
            request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
            #session可以保存7天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/admin/list/')
        elif user_object:
            request.session['info'] = {'id': user_object.id, 'name': user_object.name}
            #session可以保存7天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/user/book/list/')
    return render(request, 'login.html', {'form': form})

from io import BytesIO
def image_code(request):
    """生成图片验证码"""
    #调用PIl
    img,code_string = check_code()

    #写入自己session中以便后续进行校验
    request.session['image_code'] = code_string
    #给session设置60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""

    request.session.clear()

    return redirect('/login/')

def user_book_list(request):
    """用户预约列表"""
    data_dict = {}
    now_data = datetime.date.today()
    search_data = request.GET.get('q', now_data)
    if search_data:
        data_dict['date__contains'] = search_data
    books = models.Book.objects.filter(**data_dict)
    times = models.Book.time_choies
    rooms = models.Room.objects.all()
    data_list = []
    for time in times:  # 这就是构建表体数据
        data_list.append(mark_safe('<tr><td style="width: 5px">%s</td>' % time[1]))
        for room in rooms:
            for book in books:
                if book.room.id == room.id and time[0] == book.time:
                        tt = mark_safe(
                            '<td rowspan="1" bgcolor="#D1FFFC"><span >%s</span></td>' % ( book.username.name))
                        break
            else:
                tt = mark_safe('<td id="box"><span></span></td>')
            data_list.append(tt)
        data_list.append('</tr>')
    data = mark_safe(''.join(data_list))
    if request.method == 'GET':
        return render(request,'user_book_list.html', {"times":times,'rooms':rooms,'data':data,'search_data':search_data,'now_date':now_data})


def user_book(request):
    """会议室预约表"""
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['date__contains'] = search_data
    info = request.session.get('info')

    queryset = models.Book.objects.filter(**data_dict).filter(username_id=request.session['info']['id'] )
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data,
    }

    return render(request, 'user_book.html', context)

def user_book_add(request):
    """添加预约"""
    title = '用户预约'
    if request.method == "GET":
        form = UserBookModelForm()
        return render(request, 'user_book_change.html', {'form': form, 'title': title})
    form = UserBookModelForm(data=request.POST)
    # exsits = models.Book.objects.filter(book_date=data.book_data).exists()
    if form.is_valid():
        form.instance.username_id = request.session['info']['id']
        form.save()
        return redirect('/user/book/list/')
    return render(request, 'user_book_change.html', {"form": form, 'title': title})

def user_book_edit(request):
    """编辑用户"""
    title = '编辑用户'
    info = request.session.get('info')
    print(info)
    row_object = models.User.objects.filter(id = request.session['info']['id']).first()
    if request.method == "GET":
        form = UserEditModelForm(instance = row_object)
        return render(request,'user_book_change.html',{'form':form,'title':title})
    form = UserEditModelForm(data=request.POST,instance = row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/book/list/')
    return render(request,'user_book_change.html',{'form':form,'title':title})

def user_book_reset(request):
    """用户端重置密码"""
    row_object = models.User.objects.filter(id=request.session['info']['id']).first()
    title = '重置密码 - {}'.format(row_object.name)
    if request.method=="GET":
        form = UserResetModelform()
        return render(request,'user_book_change.html',{'form':form,'title':title})

    form = UserResetModelform(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request,'user_book_change.html',{'form':form,'title':title})
