# Generated by Django 4.0.3 on 2020-03-01 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('Rid', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='房间编号')),
                ('Rtitle', models.CharField(max_length=32, verbose_name='房间名称')),
                ('Rmin', models.IntegerField(default=0, verbose_name='房间预约人数下限')),
                ('Rmax', models.IntegerField(default=20, verbose_name='房间使用人数上限')),
                ('Rstart', models.TimeField(verbose_name='最早预约时间')),
                ('Rfinish', models.TimeField(verbose_name='最迟预约时间')),
                ('Rstatus', models.SmallIntegerField(choices=[(0, 'Permitted'), (1, 'Forbidden')], default=0, verbose_name='房间状态')),
            ],
            options={
                'verbose_name': '房间',
                'verbose_name_plural': '房间',
                'ordering': ['Rid'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('Sid', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='学号')),
                ('Sname', models.CharField(max_length=64, verbose_name='姓名')),
                ('Scredit', models.IntegerField(default=3, verbose_name='信用分')),
            ],
            options={
                'verbose_name': '学生',
                'verbose_name_plural': '学生',
                'ordering': ['Sid'],
            },
        ),
        migrations.CreateModel(
            name='Appoint',
            fields=[
                ('Aid', models.AutoField(primary_key=True, serialize=False, verbose_name='预约编号')),
                ('Atime', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('Astart', models.DateTimeField(verbose_name='开始时间')),
                ('Afinish', models.DateTimeField(verbose_name='结束时间')),
                ('Ausage', models.CharField(max_length=64, verbose_name='用途')),
                ('Astatus', models.IntegerField(choices=[(0, 'Canceled'), (1, 'Appointed'), (2, 'Processing'), (3, 'Waiting'), (4, 'Confirmed'), (5, 'Violated'), (6, 'Judged')], default=0, verbose_name='预约状态')),
                ('Room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appoint_list', to='Appointment.Room', verbose_name='房间号')),
                ('students', models.ManyToManyField(related_name='appoint_list', to='Appointment.Student')),
            ],
            options={
                'verbose_name': '预约信息',
                'verbose_name_plural': '预约信息',
                'ordering': ['Aid'],
            },
        ),
    ]