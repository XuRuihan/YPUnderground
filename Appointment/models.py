from django.db import models


# 确保你的MySQL数据库里已经包含underground数据库
# 如果没有的话，在命令行中执行mysql -uroot -p[密码]
# 执行create database underground charset=utf8rm4;（一定不能少了分号！！！）
# 定义完成后在命令行中执行python manage.py makemigrations，自动生成数据库迁移文件，
# 然后执行python manage.py migrate，Django根据迁移文件自动生成SQL语句并执行
# Django会给没有自增字段的表默认添加自增字段（id）
class Student(models.Model):
    Sid = models.CharField('学号', max_length=10, primary_key=True)
    Sname = models.CharField('姓名', max_length=64)
    # 性别对我们数据库没什么用，也许之后和其他组合并数据库会用到
    # GENDER_CHOICES = ((0, 'male'), (1, 'female'))
    # Sgender = models.SmallIntegerField(choices=GENDER_CHOICES,
    #                                    verbose_name='性别')
    # 年级同上
    # Sgrade = models.CharField(max_length=8, verbose_name='年级')
    Scredit = models.IntegerField('信用分', default=3)

    # 元数据，记录表的基本信息
    class Meta:
        db_table = 'tb_Student'  # 表名
        verbose_name = '学生'  # 指定具体名称
        verbose_name_plural = verbose_name  # 指定复数名称。中文里面没啥用，直接=verbose_name
        ordering = ['Sname']  # 指定输出结果的排序字段

        # 以下设置暂时用不到
        # abstract = True  # 把这个模型类设置成一个基类，让它不生成数据表只跟其他的子类来继承
        # permissions = (('定义好的权限', '权限的说明'), )  # 给数据表设置额外的权限
        # managed = False  # 默认是True 表示是否按照jango的既定的规则来管理模型类，比如说是否创建或者删除数据表
        # unique_together = ('address', 'note')
        # 对应mysql中联合唯一约束，可以是一元元组或者是二元元组，一元元组表示只使用一组字段作为约束条件
        # app_label = '应用名'  # 如果settings里面没有添加应用就需要定义好这个模型类属于哪个应用
        # db_tablespace  # 定义数据库表空间的名字


class RoomManager(models.Manager):
    def all(cls):
        return cls.filter(is_delete=False)


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
    # Deleted 标记已经被删除的房间，不能从表中删除的原因在下面Appoint中
    RSTATUS_CHOICES = ((0, 'Permitted'), (1, 'Forbidden'))
    Rstatus = models.SmallIntegerField('房间状态',
                                       choices=RSTATUS_CHOICES,
                                       default=0)

    # is_delete = models.BooleanField('逻辑删除', default=False)
    # last_edit = models.DateTimeField('最后一次编辑时间', auto_now=True)

    # objects = RoomManager()
    # def delete(self, using=None, keep_parents=False):
    #     """重写数据库删除方法实现逻辑删除"""
    #     self.is_delete = True
    #     self.save()

    class Meta:
        db_table = 'tb_Room'
        verbose_name = '房间'
        verbose_name_plural = verbose_name
        ordering = ['Rid']

    def __str__(self):
        return self.Rid + ' ' + self.Rtitle


class Appoint(models.Model):
    # 预约编号是自增的
    Aid = models.AutoField('预约编号', primary_key=True)
    # 这里Room使用外键的话只能设置DO_NOTHING，否则删除房间就会丢失预约信息
    # 所以房间信息不能删除，只能标记删除
    # 调用时使用appoint_obj.Room和room_obj.appoint_list
    Room = models.ForeignKey(Room,
                             related_name='appoint_list',
                             on_delete=models.SET_NULL,
                             verbose_name='房间号')
    # 申请时间为插入数据库的时间
    Atime = models.DateTimeField('申请时间', auto_now_add=True)
    # 因为预约信息不能删除，而时段和整数映射的方法不适合长时间保存
    # 所以不建议使用整数。如果想使用整数，可以采用下面映射。
    # **15分钟为1时段**
    # TIME_CHOICES = ((i, f'{i/4}h{(i%4)*15}m') for i in range(100))
    # Astart=models.SmallIntegerField(choice=TIME_CHOICES, verbose_name='开始时间')
    # Aend=models.SmallIntegerField(choice=TIME_CHOICES, verbose_name='结束时间')
    Astart = models.DateTimeField('开始时间')
    Afinish = models.DateTimeField('结束时间')
    Ausage = models.CharField('用途', max_length=64)

    # appointed:    预约中
    # processing:   进行中
    # waiting:      等待确认
    # confirmed:    已确认
    # cancelled:    已取消
    STATUS_CHOICES = ((0, 'appointed'), (1, 'processing'), (2, 'waiting'),
                      (3, 'confirmed'), (4, 'cancelled'), (5, 'violated'))
    Astatus = models.SmallIntegerField('预约状态',
                                       choices=STATUS_CHOICES,
                                       default=0)
    # 多对多关系
    # 调用时使用appoint_obj.students和student_obj.appoint_list
    # appoint是有序的，所以命名使用list；student是无序的，所以命名用复数
    # 在ER图中对应Appointer表
    students = models.ManyToManyField(Student, related_name='appoint_list')

    class Meta:
        db_table = 'tb_Appoint'
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
            self.Astatus,  # 预约状态
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
