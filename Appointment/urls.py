"""YPUnderground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from Appointment import views
app_name = 'Appointment'

urlpatterns = [
    # home 用来测试
    # 运行程序python manage.py runserver
    # url尽量符合规范，例如全部使用小写字母
    # 学生操作
    path('add-student', views.addStudent, name='addStudent'),
    path('delete-student', views.deleteStudent, name='deleteStudent'),
    path('update-student', views.updateStudent, name='updateStudent'),
    path('get-student', views.getStudent, name='getStudent'),
    # 房间操作
    path('add-room', views.addRoom, name='addRoom'),
    path('delete-room', views.deleteRoom, name='deleteRoom'),
    path('update-room', views.updateRoom, name='updateRoom'),
    path('get-room', views.getRoom, name='getRoom'),
    # 预约操作
    path('add-appoint', views.addAppoint, name='addAppoint'),
    path('delete-appoint', views.deleteAppoint, name='deleteAppoint'),
    path('update-appoint', views.updateAppoint, name='updateAppoint'),
    path('get-appoint', views.getAppoint, name='getAppoint'),
    # 学生端交互操作
    # getstudent - 查询学生所有预约记录（包括历史和未来）
    # getappoint - 查询所有预约信息
    # addappoint - 添加预约信息
    # updateappoint - 改变预约信息（预约状态）
    # 管理员端操作
    # （大概是以上所有操作）
]
