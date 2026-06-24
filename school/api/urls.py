from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminDashboardStatsAPIView,
    TeacherViewSet, StudentViewSet, ClassroomViewSet, SubjectViewSet,
    AnnouncementViewSet, TeacherAttendanceViewSet, LeaveRequestViewSet,
    PayrollViewSet, AcademicRecordViewSet, StudentAttendanceViewSet,
    StudentWarningViewSet, TeacherWarningViewSet
)

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'teacher-attendance', TeacherAttendanceViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'payroll', PayrollViewSet)
router.register(r'academic-records', AcademicRecordViewSet)
router.register(r'student-attendance', StudentAttendanceViewSet)
router.register(r'student-warnings', StudentWarningViewSet)
router.register(r'teacher-warnings', TeacherWarningViewSet)

urlpatterns = [
    path('dashboard/stats/', AdminDashboardStatsAPIView.as_view(), name='api_admin_dashboard_stats'),
    path('', include(router.urls)),
]
