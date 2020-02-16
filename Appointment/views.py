# from django.shortcuts import render
from django.http import JsonResponse
from Appointment.models import Student, Room, Appoint
from datetime import datetime
import json

from django.views.decorators.csrf import csrf_exempt


def obj2json(obj):
    return list(obj.values())


# Django数据库操作：https://www.cnblogs.com/happy-king/p/8338404.html
# 返回数据的接口规范如下：
# return JsonResponse({
#     "data": {},
#     "status": 0,  # 0 表示成功
#     "statusInfo": {
#         "message": "给用户的提示信息",
#         "detail": "用于排查错误的详细错误信息"
#     }
# })
# status 状态响应码规范：
# 0：成功
# 1：缺少参数或参数不符合规范（开始时间晚于结束时间等）
# 2：数据库错误（条目不存在或者插入内容错误等）
# 3：不允许使用的方法（GET or POST）
# 4：未登录
@csrf_exempt
def addStudent(request):
    if (request.method == 'GET'):
        return JsonResponse({
            'status': 3,
            'statusInfo': {
                'message': '不允许使用GET方法',
                'detail': 'Get method not allowed',
            },
        })
    elif (request.method == 'POST'):
        contents = json.loads(request.body)
        # 判断参数是否符合规范
        try:
            Sid = contents['Sid']
            Sname = contents['Sname']
            assert Sid != '' and Sname != '', 'empty parameters'
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '缺少参数或参数不符合规范',
                    'detail': e,
                }
            })
        # 插入数据库
        try:
            student = Student.objects.filter(Sid=Sid)
            assert not student.exists(), 'Sid already exists'
            Student.objects.create(Sid=Sid, Sname=Sname)
            return JsonResponse({'status': 0, 'data': 'success'})
        except Exception as e:
            return JsonResponse({
                'status': 2,
                'statusInfo': {
                    'message': '学号已存在',
                    'detailed': e,
                },
            })


def deleteStudent(request):
    print(request)


def updateStudent(request):
    print(request)


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
                'status': 2,
                'statusInfo': {
                    'message': '学生查询失败',
                    'detail': e,
                }
            })
        appoints = student.appoint_list.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'status': 0, 'data': data})


@csrf_exempt
def addRoom(request):
    # get 方法用于在数据库中添加测试数据，不是正式接口
    if request.method == 'GET':
        return JsonResponse({
            'status': 3,
            'statusInfo': {
                'message': '不允许使用GET方法',
                'detail': 'Get method not allowed',
            },
        })
    elif request.method == 'POST':
        contents = json.loads(request.body)
        try:
            Rid = contents['Rid']
            Rtitle = contents['Rtitle']
            Rmin = contents['Rmin']
            Rmax = contents['Rmax']
            # Rstart = contents['Rstart']
            # Rfinish = contents['Rfinish']
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
            room = rooms.objects.get(Rid=contents['Rid'])
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
        return JsonResponse({
            'status': 3,
            'statusInfo': {
                'message': '不允许使用GET方法',
                'detail': 'Get method not allowed',
            },
        })
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
                    'detail': e,
                }
            })
        # 再检查学号对不对
        students = []
        ideqstu = True
        noeq = ''
        try:
            for stu in contents['students']:
                print(stu)
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
        # 检查预约时间是否正确
        try:
            Astart = datetime.strptime(contents['Astart'], '%Y-%m-%d %H:%M:%S')
            Afinish = datetime.strptime(contents['Afinish'],
                                        '%Y-%m-%d %H:%M:%S')
            assert Astart >= Afinish, 'Appoint time error'
        except Exception as e:
            return JsonResponse({
                'status': 1,
                'statusInfo': {
                    'message': '预约时间错误',
                    'detail': e,
                }
            })
        # 学号对了，人对了，房间是真实存在的，那就开始预约了
        # 等待确认的和结束的肯定是当下时刻已经弄完的，所以不用管
        appoints = room.appoint_list.filter(Astatus__lte=2)
        for appoint in appoints:
            start = appoint.Astart
            finish = appoint.Afinish

            # 第一种可能，开始在开始之前，只要结束的比开始晚就不行
            # 第二种可能，开始在开始之后，只要在结束之前就都不行
            if ((start <= Astart and Astart <= finish)
                    or (Astart <= start and start < Afinish)):
                return JsonResponse({
                    'status': 1,
                    'statusInfo': {
                        'message': '预约时间与已有预约冲突',
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
            'data': 'success',
        })


def deleteAppoint(request):
    return JsonResponse({'delete all appoint'})


def updateAppoint(request):
    print(request)


def getAppoint(request):
    if request.method == 'GET':  # 获取所有预约信息
        appoints = Appoint.objects.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'status': 0, 'data': data})
    elif request.method == 'POST':  # 获取某条预约信息
        contents = json.loads(request.body)
        try:
            Aid = contents['Aid']
            assert Aid != '', 'Aid is empty'
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
