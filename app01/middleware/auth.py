from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

from app01 import models


class AuthMiddleware(MiddlewareMixin):
    """中间件1"""
    def process_request(self,request):
        #0.排除不需要登录的界面
        if request.path_info in ['/login/','/image/code/',"/user/book/list/"]:
            return
        #1,读取当前访问用户session信息，度得到说明；已经登录
        info_dict = request.session.get('info')
        if info_dict:
            return

        #2.没有登录过，重新回到登录界面
        return redirect('/login/')

class judge(MiddlewareMixin):
    """中间件2"""
    def process_request(self,request):
        info_dict=request.session.get('info')
        dict = ['/admin/list/','/admin/add/',
                '/admin/<int:nid>/edit',
                '/cesi/list/',
                '/admin/<int:nid>/delete',
                '/admin/<int:nid>/reset','/room/list/',
                '/room/add/','/room/<int:nid>/edit',
                '/room/<int:nid>/delete','/user/list/',
                '/user/add/','/user/<int:nid>/edit',
                '/user/<int:nid>/delete',
                '/user/<int:nid>/reset',
                '/book/list/','/book/add/','/book/<int:nid>/edit','/book/<int:nid>/delete']
        if request.path_info in dict:
            if models.User.objects.filter(**info_dict).first():
                return redirect('/user/book/list/')
            return
