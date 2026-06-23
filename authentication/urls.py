from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/teacher/<int:pk>/', views.admin_teacher_detail, name='admin_teacher_detail'),
    path('dashboard/admin/student/<int:pk>/', views.admin_student_detail, name='admin_student_detail'),
    path('dashboard/admin/teachers/', views.admin_teachers, name='admin_teachers'),
    path('dashboard/admin/students/', views.admin_students, name='admin_students'),
    path('dashboard/admin/announcements/', views.admin_announcements, name='admin_announcements'),
    path('dashboard/admin/leave-requests/', views.admin_leave_requests, name='admin_leave_requests'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/student/attendance/', views.student_attendance, name='student_attendance'),
    path('dashboard/student/exams/', views.student_exams, name='student_exams'),
    path('dashboard/student/announcements/', views.student_announcements, name='student_announcements'),
    path('manage-attendance/<int:classroom_id>/', views.manage_attendance, name='manage_attendance'),
    path('dashboard/teacher/manage-attendance/', views.manage_attendance, name='teacher_manage_attendance'),
    path('dashboard/teacher/manage-students/', views.teacher_manage_students, name='teacher_manage_students'),
    path('dashboard/teacher/add-student/', views.teacher_add_student, name='teacher_add_student'),
    path('dashboard/teacher/remove-student/', views.teacher_remove_student, name='teacher_remove_student'),
    path('dashboard/teacher/exams/', views.teacher_exams, name='teacher_exams'),
    path('dashboard/teacher/announcements/', views.teacher_announcements, name='teacher_announcements'),
    path('dashboard/teacher/leave-requests/', views.teacher_leave_requests, name='teacher_leave_requests'),
    path('dashboard/teacher/about/', views.about_teacher, name='about_teacher'),
]
