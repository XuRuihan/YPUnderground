from django.db import models


# mysql> create database yuanpei_underground charset=utf8mb4;
# > python manage.py makemigrations
# > python manage.py migrate
# Django会给没有自增字段的表默认添加自增字段（id）
class Student(models.Model):
    Sid = models.CharField('学号', max_length=10, primary_key=True)
    Sname = models.CharField('姓名', max_length=64)
    Scredit = models.IntegerField('信用分', default=3)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
        ordering = ['Sid']


class RoomManager(models.Manager):
    def permitted(self):
        return self.filter(Rstatus=Room.Status.PERMITTED)


class Room(models.Model):
    # 房间编号我不确定是否需要。如果地下室有门牌的话（例如B101）保留房间编号比较好
    # 如果删除Rid记得把Rtitle设置成主键
    Rid = models.CharField('房间编号', max_length=8, primary_key=True)
    Rtitle = models.CharField('房间名称', max_length=32)
    Rmin = models.IntegerField('房间预约人数下限', default=0)
    Rmax = models.IntegerField('房间使用人数上限', default=20)
    Rstart = models.TimeField('最早预约时间')
    Rfinish = models.TimeField('最迟预约时间')

    # Rstatus 标记当前房间是否允许预约，可由管理员修改
    class Status(models.IntegerChoices):
        PERMITTED = 0  # 允许预约
        SUSPENDED = 1  # 暂定使用
        # FORBIDDEN = 2  # 禁止使用

    Rstatus = models.SmallIntegerField('房间状态',
                                       choices=Status.choices,
                                       default=0)

    objects = RoomManager()

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = verbose_name
        ordering = ['Rid']

    def __str__(self):
        return self.Rid + ' ' + self.Rtitle


class AppointManager(models.Manager):
    def not_canceled(self):
        return self.exclude(Astatus=Appoint.Status.CANCELED)


class Appoint(models.Model):
    Aid = models.AutoField('预约编号', primary_key=True)
    # 申请时间为插入数据库的时间
    Atime = models.DateTimeField('申请时间', auto_now_add=True)
    Astart = models.DateTimeField('开始时间')
    Afinish = models.DateTimeField('结束时间')
    Ausage = models.CharField('用途', max_length=64)

    # 这里Room使用外键的话只能设置DO_NOTHING，否则删除房间就会丢失预约信息
    # 所以房间信息不能删除，只能逻辑删除
    # 调用时使用appoint_obj.Room和room_obj.appoint_list
    Room = models.ForeignKey(Room,
                             related_name='appoint_list',
                             null=True,
                             on_delete=models.SET_NULL,
                             verbose_name='房间号')
    students = models.ManyToManyField(Student, related_name='appoint_list')

    class Status(models.IntegerChoices):
        CANCELED = 0  # 已取消
        APPOINTED = 1  # 预约中
        PROCESSING = 2  # 进行中
        WAITING = 3  # 等待确认
        CONFIRMED = 4  # 已确认
        VIOLATED = 5  # 违约
        JUDGED = 6  # 违约申诉成功

    Astatus = models.IntegerField('预约状态',
                                  choices=Status.choices,
                                  default=1)

    objects = AppointManager()

    def cancel(self):
        self.Astatus = Appoint.Status.CANCELED
        self.save()

    class Meta:
        verbose_name = '预约信息'
        verbose_name_plural = verbose_name
        ordering = ['Aid']

    def toJson(self):
        data = {
            'Aid':
            self.Aid,  # 预约编号
            'Atime':
            self.Atime,  # 申请提交时间
            'Astart':
            self.Astart,  # 开始使用时间
            'Afinish':
            self.Afinish,  # 结束使用时间
            'Ausage':
            self.Ausage,  # 房间用途
            'Astatus':
            self.get_Astatus_display(),  # 预约状态
            'Rid':
            self.Room.Rid,  # 房间编号
            'Rtitle':
            self.Room.Rtitle,  # 房间名称
            'students': [  # 预约人
                {
                    'Sname': student.Sname,  # 预约人姓名
                } for student in self.students.all()
            ]
        }
        try:
            data['Rid'] = self.Room.Rid  # 房间编号
            data['Rtitle'] = self.Room.Rtitle  # 房间名称
        except Exception:
            data['Rid'] = 'deleted'  # 房间编号
            data['Rtitle'] = '房间已删除'  # 房间名称
        return data
