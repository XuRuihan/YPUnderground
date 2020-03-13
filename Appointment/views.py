# from django.shortcuts import render
from Appointment.models import Student, Room, Appoint  # 数据库模型
from django.views.decorators.http import require_POST
from django.http import JsonResponse  # Json响应
import json  # 读取Json请求

# csrf 检测和完善（待完成）
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

# 时间和定时任务
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)
scheduler.start()


def obj2json(obj):
    return list(obj.values())


def getToken(request):
    return JsonResponse({'token': get_token(request)})


# 返回数据的接口规范如下：
# return JsonResponse({
#     cookies: [],  # 暂时不用
#     data: {
#         XXXXXXXXXXXX  # 如果成功返回，显示数据
#         message: '',  #
#     },  # 返回的数据信息
#     errMsg: "request:ok"
#     header: {}  # 请求头
#     statusCode: 200,  # 200表示成功
# })
# statusCode 状态响应码规范：
# 200：成功
# 4XX：【客户端错误】使用了不合法的请求方式（GET、POST），缺少参数或参数不符合规范（条目不存在、插入重复、开始时间晚于结束时间等）
# 5XX：【服务器崩溃】看到5开头的错误就来找我……一定是我的锅（4开头的也可能是我的锅）
@require_POST
@csrf_exempt
def addStudent(request):
    contents = json.loads(request.body)
    # 判断参数是否符合规范
    try:
        Sid = contents['Sid']
        Sname = contents['Sname']
        assert Sid != '' and Sname != '', 'empty parameters'
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '缺少参数或参数不符合规范',
                'detail': str(e),
            }},
            status=400)
    # 插入数据库
    try:
        student = Student.objects.filter(Sid=Sid)
        assert not student.exists(), 'Sid already exists'
        Student.objects.create(Sid=Sid, Sname=Sname)
        return JsonResponse({'status': 0, 'data': 'success'})
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '学号已存在',
                'detailed': str(e)
            }},
            status=400)


@csrf_exempt
def getStudent(request):
    if request.method == 'GET':
        students = Student.objects.all()
        return JsonResponse({'data': obj2json(students)})
    elif request.method == 'POST':
        contents = json.loads(request.body)
        try:
            student = Student.objects.get(Sid=contents['Sid'])
        except Exception as e:
            return JsonResponse(
                {'statusInfo': {
                    'message': '学号不存在',
                    'detail': str(e)
                }},
                status=400)
        appoints = student.appoint_list.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'data': data})


@require_POST
@csrf_exempt
def addRoom(request):
    contents = json.loads(request.body)
    try:
        room = Room.objects.create(Rid=contents['Rid'],
                                   Rtitle=contents['Rtitle'],
                                   Rmin=contents['Rmin'],
                                   Rmax=contents['Rmax'],
                                   Rstatus=contents['Rstatus'])
        return JsonResponse({'data': obj2json(room)})
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '缺少参数或者房间号重复',
                'detail': str(e)
            }},
            status=400)


@csrf_exempt
def getRoom(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        return JsonResponse({'data': obj2json(rooms)})
    elif request.method == 'POST':
        contents = json.loads(request.body)
        # 修改，异常处理
        try:
            room = Room.objects.get(Rid=contents['Rid'])
        except Exception as e:
            return JsonResponse(
                {'statusInfo': {
                    'message': '房间不存在',
                    'detail': str(e)
                }},
                status=400)
        appoints = room.appoint_list.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'data': data})


# 定时任务函数
def startAppoint(Aid):
    # 变更预约状态
    appoint = Appoint.objects.get(Aid=Aid)
    if appoint.Astatus == Appoint.Status.APPOINTED:
        appoint.Astatus = Appoint.Status.PROCESSING  # processing
        appoint.save()


def finishAppoint(Aid):
    # 变更预约状态
    appoint = Appoint.objects.get(Aid=Aid)
    if appoint.Astatus == Appoint.Status.PROCESSING:
        appoint.Astatus = Appoint.Status.WAITING  # waiting
        appoint.save()
        # 管理员端发送通知


def confirmAppoint(Aid):
    # 变更预约状态
    appoint = Appoint.objects.get(Aid=Aid)
    if appoint.Astatus == Appoint.Status.WAITING:
        appoint.Astatus = Appoint.Status.CONFIRMED  # confirmed
        appoint.save()


@require_POST
@csrf_exempt
def addAppoint(request):
    contents = json.loads(request.body)
    # 首先检查房间是否存在
    try:
        room = Room.objects.get(Rid=contents['Rid'])
        assert room.Rstatus == Room.Status.PERMITTED, 'room service suspended!'
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '房间不存在或当前房间暂停预约服务',
                'detail': str(e)
            }},
            status=400)
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
        return JsonResponse(
            {'statusInfo': {
                'message': '学号不存在',
                'detail': str(e)
            }}, status=400)
    # 再检查学号和人对不对
    if ideqstu is False:
        return JsonResponse(
            {'statusInfo': {
                'message': '学号姓名不匹配',
                'detail': noeq
            }}, status=400)
    try:
        assert len(students) >= room.Rmin, f'at least {room.Rmin} students'
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '预约人数太少',
                'detail': str(e)
            }},
            status=400)
    # 检查预约时间是否正确
    try:
        Astart = datetime.strptime(contents['Astart'], '%Y-%m-%d %H:%M:%S')
        Afinish = datetime.strptime(contents['Afinish'], '%Y-%m-%d %H:%M:%S')
        assert Astart <= Afinish, 'Appoint time error'
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '时间错误',
                'detail': str(e)
            }}, status=400)
    # 学号对了，人对了，房间是真实存在的，那就开始预约了
    # 等待确认的和结束的肯定是当下时刻已经弄完的，所以不用管
    appoints = room.appoint_list.not_canceled()
    for appoint in appoints:
        start = appoint.Astart
        finish = appoint.Afinish

        # 第一种可能，开始在开始之前，只要结束的比开始晚就不行
        # 第二种可能，开始在开始之后，只要在结束之前就都不行
        if (start <= Astart <= finish) or (Astart <= start <= Afinish):
            return JsonResponse(
                {
                    'statusInfo': {
                        'message': '预约时间与已有预约冲突',
                        'detail': appoint.toJson()
                    }
                },
                status=400)

    # 合法，可以返回了
    appoint = Appoint(Room=room,
                      Astart=Astart,
                      Afinish=Afinish,
                      Ausage=contents['Ausage'])
    appoint.save()
    for student in students:
        appoint.students.add(student)
    appoint.save()

    # 开始使用，变更预约状态，学生端发送订阅消息，（可能兼顾开门工作）
    scheduler.add_job(startAppoint,
                      args=(appoint.Aid, ),
                      id=f'{appoint.Aid}_start',
                      next_run_time=Astart)
    # 结束使用，变更预约状态，管理员端发送通知（web页面能不能发通知？）
    scheduler.add_job(finishAppoint,
                      args=(appoint.Aid, ),
                      id=f'{appoint.Aid}_finish',
                      next_run_time=Afinish)
    # 如果管理员30分钟内没有确认，则自动确认，学生端发送订阅消息，管理员端发送通知
    scheduler.add_job(confirmAppoint,
                      args=(appoint.Aid, ),
                      id=f'{appoint.Aid}_confirm',
                      next_run_time=Afinish + timedelta(seconds=1800))
    return JsonResponse({'data': appoint.toJson()})


@require_POST
@csrf_exempt
def cancelAppoint(request):
    contents = json.loads(request.body)
    try:
        appoints = Appoint.objects.filter(Astatus=Appoint.Status.APPOINTED)
        appoint = appoints.get(Aid=contents['Aid'])
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '预约不存在、已经开始或者已取消',
                'detail': str(e)
            }},
            status=400)
    appoint.cancel()
    scheduler.remove_job(f'{appoint.Aid}_start')
    scheduler.remove_job(f'{appoint.Aid}_finish')
    scheduler.remove_job(f'{appoint.Aid}_confirm')
    return JsonResponse({'data': appoint.toJson()})


@csrf_exempt
def getAppoint(request):
    if request.method == 'GET':  # 获取所有预约信息
        appoints = Appoint.objects.all()
        data = [appoint.toJson() for appoint in appoints]
        return JsonResponse({'data': data})
    elif request.method == 'POST':  # 获取某条预约信息
        contents = json.loads(request.body)
        try:
            appoint = Appoint.objects.get(Aid=contents['Aid'])
        except Exception as e:
            return JsonResponse(
                {'statusInfo': {
                    'message': '预约不存在，检查Aid参数',
                    'detail': str(e)
                }},
                status=400)
        return JsonResponse({'data': appoint.toJson()})


@require_POST
@csrf_exempt
def getViolated(request):
    contents = json.loads(request.body)
    try:
        student = Student.objects.get(Sid=contents['Sid'])
    except Exception as e:
        return JsonResponse(
            {'statusInfo': {
                'message': '学号不存在',
                'detail': str(e)
            }}, status=400)
    appoints = student.appoint_list.filter(Astatus=Appoint.Status.VIOLATED)
    data = [appoint.toJson() for appoint in appoints]
    return JsonResponse({'data': data})
