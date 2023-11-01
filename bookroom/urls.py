"""bookroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/list/',views.admin_list),
    # path('',views.cheshi),
    path('admin/add/',views.admin_add),
    path('admin/<int:nid>/edit', views.admin_edit),
    path('admin/<int:nid>/delete', views.admin_delete),
    path('admin/<int:nid>/reset', views.admin_reset),
    path('room/list/',views.room_list),
    path('room/add/', views.room_add),
    path('room/<int:nid>/edit', views.room_edit),
    path('room/<int:nid>/delete', views.room_delete),
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/edit', views.user_edit),
    path('user/<int:nid>/delete', views.user_delete),
    path('user/<int:nid>/reset', views.user_reset),

    path('cesi/list/',views.cheshi),
    path('book/list/', views.book_list),
    path('book/add/', views.book_add),
    path('book/<int:nid>/edit', views.book_edit),
    path('book/<int:nid>/delete', views.book_delete),
    # path('house/',views.houseorder)

    # 登录
    path('login/', views.login),
    path('logout/', views.logout),
    path('image/code/', views.image_code),


    path('user/book/list/', views.user_book_list),
    path('user/book/',views.user_book),
    path('user/book/add/',views.user_book_add),
    path('user/book/edit/',views.user_book_edit),
    path('user/book/reset/',views.user_book_reset)


]
