from django.contrib import admin
from Appointment.models import Student, Room, Appoint

# Register your models here.


class StudentInline(admin.TabularInline):
    model = Student


class RoomInline(admin.TabularInline):
    model = Room


class AppointInline(admin.TabularInline):
    model = Appoint


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('Sid', 'Sname')
    list_display = ('Sid', 'Sname', 'Scredit')  # list
    list_display_links = ('Sid', )
    list_editable = ('Sname', 'Scredit')
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


class RoomAdmin(admin.ModelAdmin):
    list_display = ('Rid', 'Rtitle', 'Rmin', 'Rmax', 'Rstart', 'Rfinish',
                    'Rstatus', 'is_delete')
    list_display_links = ('Rid', )
    list_editable = ('Rtitle', 'Rmin', 'Rmax', 'Rstart', 'Rfinish', 'Rstatus')
    search_fields = ('Rid', 'Rtitle')
    list_filter = ('Rstatus', 'is_delete')
    fieldsets = ([
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
    ], [
        '删除房间信息', {
            'classes': ('wide', ),
            'description': '逻辑删除不会清空物理内存。只是在这里进行标记',
            'fields': ('is_delete', ),
        }
    ])


class AppointAdmin(admin.ModelAdmin):
    search_fields = ('Aid', )
    list_display = ('Aid', 'Room', 'Astart', 'Afinish', 'Atime', 'Ausage')
    list_display_links = ('Aid', )
    list_editable = ('Astart', 'Afinish', 'Ausage')
    list_filter = ('Astart', 'Atime')


admin.site.register(Student, StudentAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Appoint, AppointAdmin)
