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
    # 学生操作
    path('get-student', views.getStudent, name='getStudent'),
    # 房间操作
    path('get-room', views.getRoom, name='getRoom'),
    # 预约操作
    path('add-appoint', views.addAppoint, name='addAppoint'),
    path('cancel-appoint', views.cancelAppoint, name='cancelAppoint'),
    path('get-appoint', views.getAppoint, name='getAppoint'),

    # 部署后需要删除的操作
    path('add-student', views.addStudent, name='addStudent'),
    path('add-room', views.addRoom, name='addRoom'),

    # csrf验证操作（待完善）
    path('get-csrf', views.getToken, name='getToken'),
]
