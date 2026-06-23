from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import random

class Classroom(models.Model):
    standard = models.CharField(max_length=50)
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.standard} - {self.section}"

class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.subject_code})"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    student_id = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Extract up to 4 characters from the user's first name, else use username
            base_name = self.user.first_name if self.user.first_name else self.user.username
            name_part = base_name[:4].lower().ljust(4, 'x')
            
            # Generate a unique ID combining the name part and a 3-digit random number
            while True:
                num_part = str(random.randint(100, 999))
                new_id = f"{name_part}{num_part}"
                if not Student.objects.filter(student_id=new_id).exists():
                    self.student_id = new_id
                    break
                    
        super().save(*args, **kwargs)

    def __str__(self):
        name = f"{self.user.first_name} {self.user.last_name}".strip()
        if not name:
            name = self.user.username
        return f"{name} ({self.student_id})"

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    specialty_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    teacher_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Payroll fields
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Professional fields
    qualification = models.CharField(max_length=200, blank=True, null=True, help_text="e.g. M.Sc. Mathematics, B.Ed.")

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            base_name = self.user.first_name if self.user.first_name else self.user.username
            name_part = base_name[:4].lower().ljust(4, 'x')
            
            while True:
                num_part = str(random.randint(100, 999))
                new_id = f"tch-{name_part}{num_part}"
                if not Teacher.objects.filter(teacher_id=new_id).exists():
                    self.teacher_id = new_id
                    break
                    
        super().save(*args, **kwargs)

    @property
    def net_salary(self):
        return self.base_salary + self.allowances - self.deductions

    def __str__(self):
        name = f"{self.user.first_name} {self.user.last_name}".strip()
        if not name:
            name = self.user.username
        return f"Teacher: {name} ({self.teacher_id})"

class Timetable(models.Model):
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    
    PERIOD_CHOICES = [(i, str(i)) for i in range(1, 7)]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetable')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetable')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
    period_number = models.IntegerField(choices=PERIOD_CHOICES)

    class Meta:
        unique_together = ('classroom', 'day', 'period_number')

    def clean(self):
        super().clean()

        # 1. A teacher cannot be assigned to two different classrooms during the same day and period.
        teacher_conflict = Timetable.objects.filter(
            teacher=self.teacher,
            day=self.day,
            period_number=self.period_number
        ).exclude(pk=self.pk)

        if teacher_conflict.exists():
            raise ValidationError({
                'teacher': f"Teacher {self.teacher} is already scheduled for another class on {self.day} during Period {self.period_number}."
            })

        # 2. A classroom cannot have two different lectures scheduled at the same day and period.
        classroom_conflict = Timetable.objects.filter(
            classroom=self.classroom,
            day=self.day,
            period_number=self.period_number
        ).exclude(pk=self.pk)

        if classroom_conflict.exists():
            raise ValidationError({
                'classroom': f"Classroom {self.classroom} already has a lecture scheduled on {self.day} during Period {self.period_number}."
            })

    def __str__(self):
        return f"{self.classroom} - {self.day} P{self.period_number} ({self.subject})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=True) # True = Present, False = Absent

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.status else 'Absent'}"

class Exam(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='exams_created')
    date = models.DateField(default=timezone.now)
    max_score = models.IntegerField(default=100)

    class Meta:
        unique_together = ('name', 'classroom', 'subject')

    def __str__(self):
        return f"{self.name} - {self.classroom} ({self.subject})"

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    max_score = models.IntegerField(default=100)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student} - {self.exam.name} ({self.score}/{self.max_score})"

class Announcement(models.Model):
    CATEGORY_CHOICES = (
        ('Exam', 'Exam'),
        ('Event', 'Event'),
        ('Holiday', 'Holiday'),
        ('General', 'General'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    image = models.ImageField(upload_to='announcements/', null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='announcements')
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=True) # True = Present, False = Absent

    class Meta:
        unique_together = ('teacher', 'date')

    def __str__(self):
        return f"{self.teacher} - {self.date} - {'Present' if self.status else 'Absent'}"

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date} ({self.status})"

class Payroll(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='payrolls')
    month = models.DateField() # Store the first day of the month
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_date = models.DateField(null=True, blank=True)

    @property
    def net_salary(self):
        return self.base_salary + self.allowances - self.deductions

    def __str__(self):
        return f"{self.teacher} - {self.month.strftime('%B %Y')} - {self.status}"

class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    term = models.CharField(max_length=50) # e.g. "Mid Term 2026"
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.term}"

class StudentWarning(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='warnings')
    message = models.TextField()
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_issued = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_issued']

    def __str__(self):
        return f"Warning for {self.student.user.username} on {self.date_issued.date()}"
