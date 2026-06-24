from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count

from school.models import (
    Teacher, Student, Classroom, Subject, Announcement,
    TeacherAttendance, LeaveRequest, Payroll, AcademicRecord, Attendance,
    StudentWarning, TeacherWarning
)
from .serializers import (
    TeacherSerializer, StudentSerializer, ClassroomSerializer, SubjectSerializer,
    AnnouncementSerializer, TeacherAttendanceSerializer, LeaveRequestSerializer,
    PayrollSerializer, AcademicRecordSerializer, StudentAttendanceSerializer,
    StudentWarningSerializer, TeacherWarningSerializer
)

class AdminDashboardStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_students = Student.objects.count()
        active_teachers = Teacher.objects.count()
        total_announcements = Announcement.objects.count()
        total_leave_requests = LeaveRequest.objects.filter(status='Pending').count()
        
        return Response({
            'total_students': total_students,
            'active_teachers': active_teachers,
            'total_announcements': total_announcements,
            'pending_leave_requests': total_leave_requests
        })

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdminUser]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminUser]

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser]

class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsAdminUser]

from rest_framework.permissions import IsAuthenticated

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return LeaveRequest.objects.all().order_by('-date_applied')
        return LeaveRequest.objects.filter(user=self.request.user).order_by('-date_applied')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='Pending')

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            serializer.save(status=serializer.instance.status) # Prevent teacher from modifying status
        else:
            serializer.save()

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAdminUser]

class AcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = AcademicRecord.objects.all()
    serializer_class = AcademicRecordSerializer
    permission_classes = [IsAdminUser]

class StudentAttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAdminUser]

class StudentWarningViewSet(viewsets.ModelViewSet):
    queryset = StudentWarning.objects.all()
    serializer_class = StudentWarningSerializer
    
    def perform_create(self, serializer):
        serializer.save(issued_by=self.request.user)

class TeacherWarningViewSet(viewsets.ModelViewSet):
    queryset = TeacherWarning.objects.all()
    serializer_class = TeacherWarningSerializer
    
    def perform_create(self, serializer):
        serializer.save(issued_by=self.request.user)
