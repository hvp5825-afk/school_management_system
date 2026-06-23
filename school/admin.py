from django.contrib import admin
from .models import Classroom, Subject, Student, Teacher, Timetable, Attendance, Mark, Exam, Announcement

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Timetable)
admin.site.register(Attendance)
admin.site.register(Mark)
admin.site.register(Exam)
admin.site.register(Announcement)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'specialty_subject', 'qualification', 'base_salary', 'net_salary')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'teacher_id')
    list_filter = ('specialty_subject',)

