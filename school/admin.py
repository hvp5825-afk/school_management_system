from django.contrib import admin
from .models import Classroom, Subject, Student, Teacher, Timetable, Attendance, Mark

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Timetable)
admin.site.register(Attendance)
admin.site.register(Mark)
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty_subject', 'base_salary', 'allowances', 'deductions', 'net_salary')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('specialty_subject',)

