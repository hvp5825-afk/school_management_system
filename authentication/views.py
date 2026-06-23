from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from school.models import Teacher, Timetable, Classroom, Student, Attendance, Mark
from django.utils import timezone

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = None
        
        # 1. First, try if the user entered their direct 'username' (like teacher_amit45 or admin)
        user = authenticate(request, username=identifier, password=password)
        
        # 2. If not found, check if they entered a Teacher ID (like TCH-AMIT456)
        if user is None:
            teacher = Teacher.objects.filter(teacher_id__iexact=identifier).first()
            if teacher:
                user = authenticate(request, username=teacher.user.username, password=password)
                
        # 3. If still not found, check if they entered a Student ID (like STU-XYZ)
        if user is None:
            student = Student.objects.filter(student_id__iexact=identifier).first()
            if student:
                user = authenticate(request, username=student.user.username, password=password)
        
        if user is not None:
            login(request, user)
            role = getattr(user, 'role', None)
            
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('login') # Fallback if no role is found
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            
    return render(request, 'authentication/login.html')

@login_required
def admin_dashboard(request):
    if getattr(request.user, 'role', None) != 'admin':
        messages.error(request, "Access denied. You are not an admin.")
        return redirect('login')
        
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classrooms = Classroom.objects.count()
    
    total_payroll = sum(t.net_salary for t in Teacher.objects.all())
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classrooms': total_classrooms,
        'total_payroll': total_payroll,
    }
    return render(request, 'authentication/admin_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied. You are not a teacher.")
        return redirect('login')

    try:
        teacher_profile = request.user.teacher_profile
    except Exception:
        return HttpResponse("Teacher profile not found for this user.")

    # Get teacher's assigned classrooms and subjects based on the timetable
    timetables = Timetable.objects.filter(teacher=teacher_profile).select_related('classroom', 'subject')
    
    unique_classrooms = set()
    unique_subjects = set()
    
    for t in timetables:
        unique_classrooms.add(t.classroom)
        unique_subjects.add(t.subject)
        
    assigned_classrooms = sorted(list(unique_classrooms), key=lambda x: str(x))
    assigned_subjects = sorted(list(unique_subjects), key=lambda x: x.name)
    
    context = {
        'teacher': teacher_profile,
        'assigned_classrooms': assigned_classrooms,
        'assigned_subjects': assigned_subjects,
    }
    return render(request, 'authentication/teacher_dashboard.html', context)

@login_required
def teacher_attendance(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied. You are not a teacher.")
        return redirect('login')

    try:
        teacher_profile = request.user.teacher_profile
    except Exception:
        return HttpResponse("Teacher profile not found for this user.")

    classrooms = Classroom.objects.filter(timetable__teacher=teacher_profile).distinct()
    
    selected_classroom = None
    students = []

    if request.method == 'GET':
        classroom_id = request.GET.get('classroom_id')
        if classroom_id:
            try:
                selected_classroom = Classroom.objects.get(id=classroom_id)
                students = selected_classroom.students.all()
            except Classroom.DoesNotExist:
                pass

    context = {
        'teacher': teacher_profile,
        'classrooms': classrooms,
        'selected_classroom': selected_classroom,
        'students': students,
        'today_date': timezone.now().date(),
    }
    return render(request, 'authentication/teacher_attendance.html', context)

@login_required
def student_dashboard(request):
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, "Access denied. You are not a student.")
        return redirect('login')

    try:
        student_profile = request.user.student_profile
    except Exception:
        return HttpResponse("Student profile not found for this user.")

    # Schedule
    schedule = []
    if student_profile.classroom:
        schedule = Timetable.objects.filter(classroom=student_profile.classroom).order_by('day', 'period_number')

    # Attendance
    attendance_records = Attendance.objects.filter(student=student_profile)
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status=True).count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    # Marks
    marks = Mark.objects.filter(student=student_profile)

    context = {
        'student': student_profile,
        'schedule': schedule,
        'attendance_percentage': round(attendance_percentage, 2),
        'present_days': present_days,
        'total_days': total_days,
        'marks': marks,
    }
    return render(request, 'authentication/student_dashboard.html', context)

@login_required
def manage_attendance(request, classroom_id):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')
        
    date_str = request.GET.get('date')
    action_type = request.GET.get('action_type', 'show')
    
    if date_str:
        from datetime import datetime
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.now().date()
    else:
        target_date = timezone.now().date()
        
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        students = classroom.students.all()
    except Classroom.DoesNotExist:
        messages.error(request, "Classroom not found.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        for student in students:
            att_val = request.POST.get(f'attendance_{student.id}')
            if att_val in ['present', 'absent']:
                status = (att_val == 'present')
                att_record, created = Attendance.objects.get_or_create(
                    student=student, 
                    date=target_date,
                    defaults={'status': status}
                )
                if not created:
                    att_record.status = status
                    att_record.save()
        messages.success(request, f"Attendance saved successfully for {target_date}!")
        return redirect('teacher_attendance')

    # Fetch existing attendance
    existing_attendance = Attendance.objects.filter(student__in=students, date=target_date)
    attendance_map = {att.student_id: ('present' if att.status else 'absent') for att in existing_attendance}

    for student in students:
        student.existing_status = attendance_map.get(student.id, 'none')

    if action_type == 'take':
        # Only show students who haven't been marked yet
        students = [s for s in students if s.existing_status == 'none']
        
        if not students:
            messages.error(request, f"Attendance for {target_date} has already been completely taken. Please use 'Edit Attendance' if you wish to change it.")
            return redirect('teacher_attendance')

    context = {
        'classroom': classroom,
        'students': students,
        'target_date': target_date,
        'action_type': action_type,
    }
    return render(request, 'authentication/manage_attendance.html', context)


@login_required
def teacher_add_student(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    classrooms = Classroom.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        classroom_id = request.POST.get('classroom_id')

        # Auto-generate username and password
        import random
        base_username = f"{first_name.lower()}.{last_name.lower()}"
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{random.randint(10, 9999)}"
        
        password = "Student@123" # Default password
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student'
            )
            
            # Create student profile
            classroom = Classroom.objects.get(id=classroom_id) if classroom_id else None
            student = Student.objects.create(user=user, classroom=classroom)
            
            messages.success(request, f"Student {first_name} {last_name} added successfully! ID: {student.student_id} | Username: {username} | Password: {password}")
            return redirect('teacher_add_student')
            
        except Exception as e:
            messages.error(request, f"Error adding student: {str(e)}")
            return redirect('teacher_add_student')

    return render(request, 'authentication/teacher_add_student.html', {'classrooms': classrooms})

