from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from school.models import (
    Teacher, Student, Classroom, Subject, Announcement,
    TeacherAttendance, LeaveRequest, Payroll, AcademicRecord, Attendance,
    StudentWarning
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specialty_subject = SubjectSerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'specialty_subject', 'teacher_id', 'base_salary', 'allowances', 'deductions', 'qualification', 'net_salary']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)
    performance_label = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'classroom', 'student_id', 'performance_label']

    def get_performance_label(self, obj):
        from school.models import Attendance, Mark
        from django.db.models import Sum

        total_days = Attendance.objects.filter(student=obj).count()
        present_days = Attendance.objects.filter(student=obj, status=True).count()
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

        marks_aggr = Mark.objects.filter(student=obj).aggregate(total_score=Sum('score'), total_max=Sum('max_score'))
        total_score = marks_aggr['total_score'] or 0
        total_max = marks_aggr['total_max'] or 0
        marks_percentage = (float(total_score) / float(total_max) * 100) if total_max > 0 else 0

        if total_days > 0 and total_max > 0:
            overall_percentage = (attendance_percentage + marks_percentage) / 2
        elif total_days > 0:
            overall_percentage = attendance_percentage
        elif total_max > 0:
            overall_percentage = marks_percentage
        else:
            overall_percentage = 0

        if total_days == 0 and total_max == 0:
            return "No Data"
        elif overall_percentage > 90:
            return "Excellent"
        elif overall_percentage > 80:
            return "Good"
        elif overall_percentage >= 50:
            return "Average"
        elif overall_percentage >= 30:
            return "Poor"
        else:
            return "Very Bad"

class AnnouncementSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = TeacherAttendance
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['user']

class PayrollSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = Payroll
        fields = '__all__'

class AcademicRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = AcademicRecord
        fields = '__all__'

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class StudentWarningSerializer(serializers.ModelSerializer):
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)

    class Meta:
        model = StudentWarning
        fields = '__all__'
