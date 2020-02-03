from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Appointment.models import Student, Room, Appoint
import json


# 响应函数都在这里
# 路由关系在urls.py中定义
# HttpResponse()直接返回字符串
# render()返回模板
def home(request):
    print(request)
    return HttpResponse("hello")


# Django数据库操作：https://www.cnblogs.com/happy-king/p/8338404.html
def addStudent(request):
    print(request)
    if (request.method == 'GET'):
        print('addStudent using GET method')
        student = Student()
        student.Sid = '2333'
        student.Sname = 'Jerry'
        student.Scredit = 3
        student.save()
        return HttpResponse('Add Jerry to Student')
    elif (request.method == 'POST'):
        print('addStudent using POST method')
        concat = request.POST
        postBody = request.body
        # 如果json.loads报错，尝试用postBody=str(postBody, encoding='utf-8')
        jsonContent = json.loads(postBody)
        try:
            print(concat)
            print(postBody)
            print(jsonContent)
        except Exception as identifier:
            print(identifier)

        # https://blog.csdn.net/u011072037/article/details/92832638
        # 这篇文章我没看懂，但感觉我写的肯定有点问题。。
        student = Student.objects.create(**concat.dict())
        return JsonResponse({'ret': 'False', 'data': {}})


def deleteStudent(request):
    print(request)
    pass


def updateStudent(request):
    print(request)
    pass


def selectStudent(request):
    print(request)
    if (request.method == 'GET'):
        print('selectStudent using GET method')
        student = Student.objects.get(Sid='2333')
        appoints = student.appoint_list.all()
        context = {'student': student, 'appoints': appoints}
        return render(request, 'selectStudent.html', context=context)


def addRoom(request):
    print(request)
    if (request.method == 'GET'):
        print('addRoom using GET method')
        room = Room()
        room.Rid = 'B102'
        room.Rtitle = '小讨论室'
        room.Rmin = '3'
        room.Rmax = '15'
        room.Rstatus = 0
        room.save()  # 必须有这一句才能存储信息
        return HttpResponse('Add B102 to Room')
    elif (request.method == 'POST'):
        print('addRoom using POST method')
        room = Room.objects.create(**request.POST.dict())
        return JsonResponse({'ret': 'False', 'data': {}})


def deleteRoom(request):
    print(request)
    pass


def updateRoom(request):
    print(request)
    pass


def selectRoom(request):
    print(request)
    if (request.method == 'GET'):
        rooms = Room.objects.all()
        context = {'rooms': rooms}
        for room in rooms:
            print('something')
            print(room.Rtitle)
        return render(request, 'selectRoom.html', context=context)


def addAppoint(request):
    print(request)
    pass


def deleteAppoint(request):
    print(request)
    pass


def updateAppoint(request):
    print(request)
    pass


def selectAppoint(request):
    print(request)
    if (request.method == 'GET'):
        print('selectAppoint using GET method')
        appoints = Appoint.objects.all()
        context = {'appoints': appoints}
        return render(request, 'selectAppoint.html', context=context)
    elif (request.method == 'POST'):
        print("using POST method")
        return JsonResponse({'ret': 'False', 'data': {}})
