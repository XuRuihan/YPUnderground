from Appointment.models import Student, Room, Appoint
from django.contrib import admin
from django.utils.html import format_html, format_html_join

# Register your models here.
admin.site.site_title = '元培地下室管理后台'
admin.site.site_header = '元培地下室 - 管理后台'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('Sid', 'Sname')
    list_display = ('Sid', 'Sname', 'Scredit')
    list_display_links = ('Sid', 'Sname')
    list_editable = ('Scredit', )
    list_filter = ('Scredit', )
    fieldsets = (['基本信息', {
        'fields': (
            'Sid',
            'Sname',
        ),
    }], [
        '显示全部', {
            'classes': ('collapse', ),
            'description': '默认信息，不建议修改！',
            'fields': ('Scredit', ),
        }
    ])


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'Rid',
        'Rtitle',
        'Rmin',
        'Rmax',
        'Rstart',
        'Rfinish',
        'Rstatus_display',
    )  # 'is_delete'
    list_display_links = ('Rid', )
    list_editable = ('Rtitle', 'Rmin', 'Rmax', 'Rstart', 'Rfinish')
    search_fields = ('Rid', 'Rtitle')
    list_filter = ('Rstatus', )  # 'is_delete'
    fieldsets = (
        [
            '基本信息', {
                'fields': (
                    'Rid',
                    'Rtitle',
                    'Rmin',
                    'Rmax',
                    'Rstart',
                    'Rfinish',
                    'Rstatus',
                ),
            }
        ],
        # [
        #     '删除房间信息', {
        #         'classes': ('wide', ),
        #         'description': '逻辑删除不会清空物理内存。只是在这里进行标记',
        #         'fields': ('is_delete', ),
        #     }
        # ],
    )

    def Rstatus_display(self, obj):
        if obj.Rstatus == Room.Status.PERMITTED:
            color_code = 'green'
        elif obj.Rstatus == Room.Status.SUSPENDED:
            color_code = 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            obj.get_Rstatus_display(),
        )

    Rstatus_display.short_description = '预约状态'


@admin.register(Appoint)
class AppointAdmin(admin.ModelAdmin):
    search_fields = (
        'Aid',
        'Room',
    )
    list_display = (
        'Aid',
        'Room',
        'Astart',
        'Afinish',
        'Atime',  # 'Ausage',
        'Students',
        'Astatus_display',
    )
    list_display_links = ('Aid', 'Room')
    list_editable = (
        'Astart',
        'Afinish',
    )  # 'Ausage'
    list_filter = ('Astart', 'Atime')
    date_hierarchy = 'Astart'

    def Students(self, obj):
        return format_html_join('\n', '<li>{}</li>',
                                ((stu.Sname, ) for stu in obj.students.all()))

    Students.short_description = '预约者'

    def Astatus_display(self, obj):
        status2color = {
            Appoint.Status.CANCELED: 'grey',
            Appoint.Status.APPOINTED: 'black',
            Appoint.Status.PROCESSING: 'purple',
            Appoint.Status.WAITING: 'blue',
            Appoint.Status.CONFIRMED: 'green',
            Appoint.Status.VIOLATED: 'red',
            Appoint.Status.JUDGED: 'yellowgreen',
        }
        color_code = status2color[obj.Astatus]
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            obj.get_Astatus_display(),
        )

    Astatus_display.short_description = '预约状态'

    actions = ['confirm', 'violate']

    def confirm(self, request, queryset):  # 确认通过
        for appoint in queryset:
            if appoint.Astatus == Appoint.Status.WAITING:
                appoint.Astatus = Appoint.Status.CONFIRMED
            elif appoint.Astatus == Appoint.Status.VIOLATED:
                appoint.Astatus = Appoint.Status.JUDGED
                for stu in appoint.students.all():
                    if stu.Scredit < 3:
                        stu.Scredit += 1
                        stu.save()
            appoint.save()

    confirm.short_description = '所选条目 通过'

    def violate(self, request, queryset):  # 确认违约
        for appoint in queryset:
            if appoint.Astatus == Appoint.Status.WAITING:
                appoint.Astatus = Appoint.Status.VIOLATED
                appoint.save()
                for stu in appoint.students.all():
                    stu.Scredit -= 1
                    stu.save()
            appoint.save()

    violate.short_description = '所选条目 违约'
