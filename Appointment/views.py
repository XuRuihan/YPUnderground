# from django.shortcuts import render
from django.http import JsonResponse
from Appointment.models import Student, Room, Appoint
from django.core.serializers import serialize
import json

from django.views.decorators.csrf import csrf_exempt

# 响应函数都在这里
# 路由关系在urls.py中定义


def obj2json(obj):
    return json.loads(serialize('json', obj.only()))
    # return list(obj.values())


# Django数据库操作：https://www.cnblogs.com/happy-king/p/8338404.html
# 推荐接口规范：https://www.cnblogs.com/guiyishanren/p/11132444.html
# 返回数据的接口规范如下：
# return JsonResponse({
#     "data": {},
#     "status": 0,  # 0 表示成功
#     "statusInfo": {
#         "message": "给用户的提示信息",
#         "detail": "用于排查错误的详细错误信息"
#     }
# })
@csrf_exempt
def addStudent(request):
    if (request.method == 'GET'):
        student = Student()
        student.Sid = '2333'
        student.Sname = 'Jerry'
        student.Scredit = 3
        student.save()
        student = Student().objects.filter(Sid='2333')
        return JsonResponse({'status': 0, 'data': obj2json(student)})
    elif (request.method == 'POST'):
        contents = json.loads(request.body)
        try:
            Sid = contents['Sid']
            Sname = contents['Sname']
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '缺少参数',
                    'detail': str(type(e))
                }
            })
        if Sid == '' or Sname == '':
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '参数不能为空',
                    'detail': ''
                }
            })
        student = Student.objects.filter(Sid=Sid)
        if student.exists():
            return JsonResponse({
                'status': 400,
                'statusInfo': {
                    'message': '学号已存在',
                    'detailed': obj2json(student)
                },
            })

        try:
            Student.objects.create(Sid=Sid, Sname=Sname)
            student = Student.objects.filter(Sid=contents['Sid'])
            return JsonResponse({'status': 0, 'data': obj2json(student)})
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '学生创建失败',
                    'detail': str(type(e))
                }
            })


def deleteStudent(request):
    print(request)
    pass


def updateStudent(request):
    print(request)
    pass


@csrf_exempt
def getStudent(request):
    if request.method == 'GET':
        students = Student.objects.all()
        return JsonResponse({'status': 0, 'data': obj2json(students)})
    elif request.method == 'POST':
        contents = json.loads(request.body)
        student = Student.objects.filter(contents['Sid'])
        return JsonResponse({'status': 0, 'data': obj2json(student)})


@csrf_exempt
def addRoom(request):
    if (request.method == 'GET'):
        print('addRoom using GET method')
        room = Room.objects.create(Rid='B102',
                                   Rtitle='小讨论室',
                                   Rmin='3',
                                   Rmax='15',
                                   Rstatus=0)
        room.save()  # 必须有这一句才能存储信息
        room = Room.objects.filter(Rid='B102')
        return JsonResponse({'status': 0, 'data': obj2json(room)})
    elif (request.method == 'POST'):
        contents = json.loads(request.body)
        try:
            Rid = contents['Rid'],
            Rtitle = contents['Rtitle'],
            Rmin = contents['Rmin'],
            Rmax = contents['Rmax'],
            Rstatus = contents['Rstatus']
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '缺少参数',
                    'detail': str(type(e))
                }
            })
        if Rid == '' or Rtitle == '':
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '参数不能为空',
                    'detail': ''
                }
            })

        try:
            room = Room.objects.create(Rid=Rid,
                                       Rtitle=Rtitle,
                                       Rmin=Rmin,
                                       Rmax=Rmax,
                                       Rstatus=Rstatus)
            return JsonResponse({'status': 0, 'data': obj2json(room)})
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '房间创建失败',
                    'detail': str(type(e))
                }
            })


def deleteRoom(request):
    print(request)
    pass


def updateRoom(request):
    print(request)
    pass


@csrf_exempt
def getRoom(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        return JsonResponse({'status': 0, 'data': obj2json(rooms)})
    elif request.method == 'POST':
        contents = json.loads(request.body)
        room = Room.objects.filter(Rid=contents['Rid'])
        return JsonResponse({'status': 0, 'data': obj2json(room)})


# 新增预约的接口参数推荐：
data: {
    'students': [
        {
            'Sid': '1700017793',
            'Sname': 'Xrh'
        },
        {
            'Sid': '1700017795',
            'Sname': 'Ky'
        },
    ],
    'appoint': {
        'Rid': 'B102',
        'Astart': '2020-5-1 15:30',
        'Afinish': '2020-5-1 16:40',
    }
}


@csrf_exempt
def addAppoint(request):
    if (request.method == 'GET'):
        return JsonResponse({
            'status': 400,
            'statusInfo': {
                'message': 'add-appoint 没有GET方法',
                'detail': 'using POST method instead'
            }
        })
    elif (request.method == 'POST'):
        contents = json.loads(request.body)


def deleteAppoint(request):
    print(request)
    pass


def updateAppoint(request):
    print(request)
    pass


def getAppoint(request):
    if (request.method == 'GET'):  # 获取所有预约信息
        appoints = Appoint.objects.all()
        return JsonResponse({'status': 0, 'data': obj2json(appoints)})
    elif (request.method == 'POST'):  # 获取某条预约信息
        contents = json.loads(request.body)
        appoint = Appoint.objects.filter(Aid=contents['Aid'])
        return JsonResponse({'status': 0, 'data': obj2json(appoint)})
