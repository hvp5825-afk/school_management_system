from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('manage-attendance/<int:classroom_id>/', views.manage_attendance, name='manage_attendance'),
    path('dashboard/teacher/add-student/', views.teacher_add_student, name='teacher_add_student'),
    path('dashboard/teacher/exams/', views.teacher_exams, name='teacher_exams'),
]
