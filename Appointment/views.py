# from django.shortcuts import render
from django.http import JsonResponse
from Appointment.models import Student, Room, Appoint
from datetime import datetime, time
import json

from django.views.decorators.csrf import csrf_exempt

# 响应函数都在这里
# 路由关系在urls.py中定义
# 查询的时候推荐使用 filter 方法代替 get 方法，因为 get 方法遇到
# 多个查询结果或没有查询结果时会抛出异常
# 如果使用 try/except 则可以使用 get 方法


def obj2json(obj):
    # 我TM真的服了这个serializers了
    # from django.core.serializers import serialize
    # return json.loads(serialize('json', obj.only()))
    # from django.core.serializers.json import DjangoJSONEncoder
    # return list(obj.values(), cls=DjangoJSONEncoder)
    return list(obj.values())


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
    # GET 方法用于在数据库中添加测试数据，不是正式接口
    if (request.method == 'GET'):
        student = Student()
        student.Sid = '1700017793'
        student.Sname = 'Xrh'
        student.save()
        student = Student.objects.filter(Sid='1700017793')
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
        try:
            student = Student.objects.get(Sid=contents['Sid'])
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '学生查询失败',
                    'detail': str(type(e))
                }
            })
        appoints = student.appoint_list.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'status': 0, 'data': data})


@csrf_exempt
def addRoom(request):
    # get 方法用于在数据库中添加测试数据，不是正式接口
    if request.method == 'GET':
        return JsonResponse({'status': 1, 'data': 'GET method not allowed'})
    elif request.method == 'POST':
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
        rooms = Room.objects.all()
        # 修改，异常处理
        try:
            room = rooms.objects.filter(Rid=contents['Rid'])
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '房间不存在',
                    'detail': str(type(e))
                }
            })
        appoints = room.appoint_list.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'status': 0, 'data': data})


@csrf_exempt
def addAppoint(request):
    # get 方法用于在数据库中添加测试数据，不是正式接口
    if (request.method == 'GET'):
        room = Room.objects.get(Rid='B102')
        student = Student.objects.get(Sid='1700017793')
        appoint = Appoint(Room=room,
                          Astart=datetime(2020, 1, 1, 8, 0, 0),
                          Afinish=datetime(2020, 1, 1, 9, 0, 0),
                          Ausage='do something')
        appoint.save()
        appoint.students.add(student)
        appoint.save()
        return JsonResponse({'status': 0, 'data': {}})
    elif (request.method == 'POST'):
        contents = json.loads(request.body)
        # 首先检查房间是否存在
        try:
            room = Room.objects.get(Rid=contents['Rid'])
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '房间不存在',
                    'detail': str(type(e))
                }
            })
        # 再检查学号对不对
        students = []
        ideqstu = True
        noeq = ''
        try:
            for stu in contents['students']:
                student = Student.objects.get(Sid=stu['Sid'])
                if student.Sname != stu['Sname']:
                    ideqstu = False
                    noeq.join(str(student.Sid))
                    noeq.join(' ')
                students.append(student)
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '学号不存在',
                    'detail': str(type(e))
                }
            })
        # 再检查学号和人对不对
        if ideqstu is False:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '学生和学号不匹配',
                    'detail': noeq
                }
            })
        # 学号对了，人对了，房间是真实存在的，那就开始预约了
        appoints = room.appoint_list.all()
        for appoint in appoints:
            # 等待确认的和结束的肯定是当下时刻已经弄完的，所以不用管
            if appoint.Astatus == 4 or appoint.Astatus == 3:
                continue
            start = appoint.Astart
            finish = appoint.Afinish
            # 第零种可能，愚蠢的预约，确保约定前小于后
            if start >= finish:
                return JsonResponse({
                    'status': 1,
                    'statusInfo': {
                        'message': '愚蠢',
                        'detail': str(appoint.Aid)
                    }
                })
            # 第一种可能，开始在开始之前，只要结束的比开始晚就不行
            if start <= contents['Astart'] and finish >= contents['Astart']:
                return JsonResponse({
                    'status': 1,
                    'statusInfo': {
                        'message': '冲突',
                        'detail': str(appoint.Aid)
                    }
                })
            # 第二种可能，开始在开始之后，只要在结束之前就都不行
            elif start >= contents['Astart'] and start < contents['Afinish']:
                return JsonResponse({
                    'status': 1,
                    'statusInfo': {
                        'message': '冲突',
                        'detail': str(appoint.Aid)
                    }
                })
        # 合法，可以返回了
        appoint = Appoint(Room=room,
                          Astart=contents['Astart'],
                          Afinish=contents['Afinish'],
                          Ausage=contents['Ausage'])
        appoint.save()
        for student in students:
            appoint.students.add(student)
        appoint.save()
        return JsonResponse({
            'status': 0,
            'data': {
                'message': '成功',
                'detail': ''
            }
        })


def deleteAppoint(request):
    return JsonResponse({'delete all appoint'})


def updateAppoint(request):
    print(request)


def getAppoint(request):
    if (request.method == 'GET'):  # 获取所有预约信息
        appoints = Appoint.objects.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'status': 0, 'data': data})
    elif (request.method == 'POST'):  # 获取某条预约信息
        contents = json.loads(request.body)
        try:
            Aid = contents['Aid']
            assert contents['Aid'] != '', 'Aid is empty'
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': 'Appointment id error',
                    'detail': e,
                }
            })
        appoints = Appoint.objects.filter(Aid=Aid)
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'status': 0, 'data': data})
