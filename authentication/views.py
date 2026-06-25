from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from school.models import Teacher, Timetable, Classroom, Student, Attendance, Mark, Announcement, Subject, Exam
from django.utils import timezone
from django.db.models import Q

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        print(f"DEBUG LOGIN: Trying to login with username='{identifier}' and password='{password}'")

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
            
            # Auto-detect role from profiles if admin forgot to set the role field manually
            if not role or role not in ['admin', 'teacher', 'student']:
                if hasattr(user, 'student_profile'):
                    role = 'student'
                    user.role = 'student'
                    user.save()
                elif hasattr(user, 'teacher_profile'):
                    role = 'teacher'
                    user.role = 'teacher'
                    user.save()
                elif user.is_superuser:
                    role = 'admin'
                    user.role = 'admin'
                    user.save()
            
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            else:
                messages.error(request, "Account error: Role not assigned. Contact admin.")
                return redirect('login')
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

    # Only allow attendance for the class they are Class Teacher of
    classrooms = []
    if hasattr(teacher_profile, 'assigned_classroom'):
        classrooms = [teacher_profile.assigned_classroom]
    
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
        return HttpResponse(f"Student profile not found for this user. Username: {request.user.username}, Role: {getattr(request.user, 'role', 'None')}")

    # Schedule
    schedule = []
    if student_profile.classroom:
        schedule = Timetable.objects.filter(classroom=student_profile.classroom).order_by('day', 'period_number')

    # Attendance
    attendance_records = Attendance.objects.filter(student=student_profile)
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status=True).count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    # Get recent announcements
    recent_announcements = Announcement.objects.all().order_by('-date_posted')[:3]

    from school.models import StudentWarning
    warnings = StudentWarning.objects.filter(student=student_profile).order_by('-date_issued')

    context = {
        'student': student_profile,
        'schedule': schedule,
        'attendance_percentage': attendance_percentage,
        'total_days': total_days,
        'present_days': present_days,
        'recent_announcements': recent_announcements,
        'warnings': warnings,
    }
    
    return render(request, 'authentication/student_dashboard.html', context)

@login_required
def student_attendance(request):
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, 'Access denied.')
        return redirect('login')
        
    student = Student.objects.get(user=request.user)
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    
    total_days = attendances.count()
    present_days = attendances.filter(status=True).count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    context = {
        'student': student,
        'attendances': attendances,
        'total_days': total_days,
        'present_days': present_days,
        'attendance_percentage': round(attendance_percentage, 1),
    }
    return render(request, 'authentication/student_attendance.html', context)

@login_required
def student_exams(request):
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, 'Access denied.')
        return redirect('login')
        
    student = Student.objects.get(user=request.user)
    marks = Mark.objects.filter(student=student).select_related('exam', 'exam__subject')
    
    context = {
        'student': student,
        'marks': marks,
    }
    return render(request, 'authentication/student_exams.html', context)

@login_required
def student_announcements(request):
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, 'Access denied.')
        return redirect('login')
        
    student = Student.objects.get(user=request.user)
    
    # All announcements are common for all students
    from school.models import Notification
    Notification.objects.filter(user=request.user, is_read=False, link__icontains='announcements').update(is_read=True)
    announcements = Announcement.objects.all().order_by('-date_posted')
    
    context = {
        'student': student,
        'announcements': announcements,
    }
    return render(request, 'authentication/student_announcements.html', context)

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
def teacher_manage_students(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')
    return render(request, 'authentication/teacher_manage_students.html')

@login_required
def teacher_add_student(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    # Restrict to assigned classroom
    classrooms = []
    if hasattr(request.user, 'teacher_profile') and getattr(request.user.teacher_profile, 'assigned_classroom', None):
        classrooms = [request.user.teacher_profile.assigned_classroom]

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove':
            student_id = request.POST.get('student_id')
            try:
                student = Student.objects.get(id=student_id)
                user_to_delete = student.user
                student.delete()
                user_to_delete.delete()
                messages.success(request, "Student removed successfully!")
            except Exception as e:
                messages.error(request, f"Error removing student: {str(e)}")
            return redirect('teacher_add_student')

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

    students = Student.objects.select_related('user', 'classroom').order_by('-user__date_joined')
    return render(request, 'authentication/teacher_add_student.html', {'classrooms': classrooms, 'students': students})


@login_required
def teacher_remove_student(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    classrooms = []
    if hasattr(request.user, 'teacher_profile') and getattr(request.user.teacher_profile, 'assigned_classroom', None):
        classrooms = [request.user.teacher_profile.assigned_classroom]
    students = []
    search_query = request.GET.get('search_query', '').strip()
    classroom_id = request.GET.get('classroom_id', '')

    if search_query or classroom_id:
        from django.db.models import Q
        students = Student.objects.select_related('user', 'classroom')
        if search_query:
            students = students.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(student_id__icontains=search_query)
            )
        if classroom_id:
            students = students.filter(classroom_id=classroom_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove':
            student_id = request.POST.get('student_id')
            try:
                student = Student.objects.get(id=student_id)
                user_to_delete = student.user
                student.delete()
                user_to_delete.delete()
                messages.success(request, "Student removed successfully!")
            except Exception as e:
                messages.error(request, f"Error removing student: {str(e)}")
            return redirect('teacher_remove_student')

    return render(request, 'authentication/teacher_remove_student.html', {
        'classrooms': classrooms, 
        'students': students, 
        'search_query': search_query,
        'selected_classroom': classroom_id
    })

@login_required
def teacher_exams(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('login')

    # Only allow exams for the class they are Class Teacher of
    unique_classrooms = []
    if hasattr(teacher, 'assigned_classroom') and teacher.assigned_classroom:
        unique_classrooms = [teacher.assigned_classroom]
        
    unique_subjects = []
    if hasattr(teacher, 'assigned_classroom') and teacher.assigned_classroom:
        unique_subjects = list(Subject.objects.filter(classroom=teacher.assigned_classroom))

    selected_classroom_id = request.GET.get('classroom_id')
    selected_exam_name = request.GET.get('exam_name')
    
    # Second form params
    selected_subject_id = request.GET.get('subject_id')
    exam_date_str = request.GET.get('exam_date')
    max_score_val = request.GET.get('max_score', '100')
    export_csv = request.GET.get('export_csv')
    
    students = []
    selected_classroom = None
    selected_subject = None
    selected_exam = None
    selected_date = None
    action_type = request.GET.get('action_type', 'show')

    # Step 1: Class and Exam Name selected
    if selected_classroom_id and selected_exam_name:
        try:
            selected_classroom = Classroom.objects.get(id=selected_classroom_id)
            students = list(selected_classroom.students.all())
            
            # Default to today's date
            from django.utils import timezone
            selected_date = timezone.now().date()
            
            # Step 2: If subject is also selected, create/fetch the actual Exam object
            if selected_subject_id:
                selected_subject = Subject.objects.get(id=selected_subject_id)
                
                if exam_date_str:
                    from datetime import datetime
                    try:
                        selected_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                max_sc = int(max_score_val) if max_score_val.isdigit() else 100
                from school.models import Exam, Mark
                
                action_type = request.GET.get('action_type', 'show')
                
                if action_type == 'edit':
                    selected_exam, created = Exam.objects.get_or_create(
                        name=selected_exam_name,
                        classroom=selected_classroom,
                        subject=selected_subject,
                        date=selected_date,
                        defaults={'max_score': max_sc, 'teacher': teacher}
                    )
                    if not created:
                        selected_exam.max_score = max_sc
                        selected_exam.save()
                else:
                    try:
                        selected_exam = Exam.objects.get(
                            name=selected_exam_name,
                            classroom=selected_classroom,
                            subject=selected_subject,
                            date=selected_date
                        )
                    except Exam.DoesNotExist:
                        selected_exam = None
                
                # Fetch existing marks
                marks = []
                if selected_exam:
                    marks = Mark.objects.filter(student__in=students, exam=selected_exam)
                marks_dict = {m.student_id: m for m in marks}
                
                for student in students:
                    student.existing_mark = marks_dict.get(student.id)
                
                # CSV Export logic
                if export_csv == '1':
                    import csv
                    from django.http import HttpResponse
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="marks_{selected_classroom}_{selected_exam.name}_{selected_subject.name}.csv"'
                    
                    writer = csv.writer(response)
                    writer.writerow(['Student ID', 'Student Name', 'Score Obtained', 'Max Score', 'Percentage'])
                    
                    for student in students:
                        m = student.existing_mark
                        if m:
                            pct = round((m.score / m.max_score) * 100, 2) if m.max_score > 0 else 0
                            writer.writerow([student.student_id, f"{student.user.first_name} {student.user.last_name}", m.score, m.max_score, f"{pct}%"])
                        else:
                            writer.writerow([student.student_id, f"{student.user.first_name} {student.user.last_name}", 'N/A', selected_exam.max_score, 'N/A'])
                    
                    return response
                
        except (Classroom.DoesNotExist, Subject.DoesNotExist):
            pass

    if request.method == 'POST' and request.POST.get('save_marks') == '1':
        exam_id_post = request.GET.get('exam_id')
        from school.models import Exam, Mark
        try:
            selected_exam = Exam.objects.get(id=exam_id_post)
        except Exam.DoesNotExist:
            selected_exam = None
            
        if selected_exam and selected_classroom:
            has_error = False
            for student in students:
                score_val = request.POST.get(f'score_{student.id}')
                if score_val is not None and score_val != '':
                    try:
                        score = float(score_val)
                        if score > selected_exam.max_score:
                            has_error = True
                            continue
                            
                        # Update or Create
                        mark, created = Mark.objects.get_or_create(
                            student=student,
                            exam=selected_exam,
                            defaults={'score': score, 'max_score': selected_exam.max_score}
                        )
                        if not created:
                            mark.score = score
                            mark.max_score = selected_exam.max_score
                            mark.save()
                    except ValueError:
                        continue # Skip invalid numbers

            if not has_error:
                messages.success(request, f"Marks saved successfully for {selected_exam.subject.name} - {selected_exam.name}!")
            else:
                messages.warning(request, f"Some marks were saved, but some failed due to exceeding max score.")
            
            # Redirect to GET to show updated data
            return redirect(f"{request.path}?classroom_id={selected_classroom.id}&exam_name={selected_exam.name}&subject_id={selected_exam.subject.id}&exam_date={selected_exam.date}&action_type=show")

    context = {
        'unique_classrooms': unique_classrooms,
        'unique_subjects': unique_subjects,
        'selected_classroom': selected_classroom,
        'selected_exam_name': selected_exam_name,
        'selected_subject': selected_subject,
        'selected_exam': selected_exam,
        'selected_date': selected_date,
        'students': students,
        'action_type': action_type,
    }
    return render(request, 'authentication/teacher_exams.html', context)

def teacher_announcements(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('login')

    from school.models import Announcement

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if title and content:
            Announcement.objects.create(
                teacher=teacher,
                title=title,
                content=content,
                category=category,
                image=image
            )
            messages.success(request, 'Announcement posted successfully!')
            return redirect('teacher_announcements')

    from school.models import Notification
    Notification.objects.filter(user=request.user, is_read=False, link__icontains='announcements').update(is_read=True)
    announcements = Announcement.objects.filter(teacher=teacher).order_by('-date_posted')
    return render(request, 'authentication/teacher_announcements.html', {'announcements': announcements})

@login_required
def about_teacher(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')
        
    try:
        teacher = Teacher.objects.select_related('user', 'specialty_subject').get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('login')
        
    return render(request, 'authentication/about_teacher.html', {'teacher': teacher})

@login_required
def teacher_leave_requests(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')
        
    from school.models import LeaveRequest, Notification
    
    # Mark all unread leave-request related notifications as read
    Notification.objects.filter(user=request.user, is_read=False, link__icontains='leave-requests').update(is_read=True)
    
    leave_requests = LeaveRequest.objects.filter(user=request.user).order_by('-date_applied')
    return render(request, 'authentication/teacher_leave_requests.html', {'leave_requests': leave_requests})

# Admin Panel Views
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('login')
    return render(request, 'admin/admin_dashboard.html')

@login_required
@login_required
def admin_teacher_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    from school.models import Teacher, TeacherWarning
    from django.shortcuts import get_object_or_404
    teacher = get_object_or_404(Teacher, pk=pk)
    warnings = teacher.warnings.all()
    return render(request, 'admin/admin_teacher_detail.html', {'teacher_id': pk, 'teacher': teacher, 'warnings': warnings})

@login_required
def admin_student_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    
    from school.models import Student, Attendance, Mark, StudentWarning
    from django.shortcuts import get_object_or_404
    
    from django.db.models import Sum
    
    student = get_object_or_404(Student, pk=pk)
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    marks = Mark.objects.filter(student=student).select_related('exam', 'exam__subject').order_by('-exam__date')
    warnings = StudentWarning.objects.filter(student=student).order_by('-date_issued')
    
    # --- Performance Calculation Logic ---
    # 1. Attendance Percentage
    total_days = attendances.count()
    present_days = attendances.filter(status=True).count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    # 2. Marks Average
    marks_aggr = marks.aggregate(total_score=Sum('score'), total_max=Sum('max_score'))
    total_score = marks_aggr['total_score'] or 0
    total_max = marks_aggr['total_max'] or 0
    marks_percentage = (float(total_score) / float(total_max) * 100) if total_max > 0 else 0

    # 3. Overall Performance
    # We average both percentages. If data is missing for one, we rely on the other.
    if total_days > 0 and total_max > 0:
        overall_percentage = (attendance_percentage + marks_percentage) / 2
    elif total_days > 0:
        overall_percentage = attendance_percentage
    elif total_max > 0:
        overall_percentage = marks_percentage
    else:
        overall_percentage = 0
        
    performance_label = "Very Bad"
    performance_color = "var(--danger)"
    
    if total_days == 0 and total_max == 0:
        performance_label = "No Data"
        performance_color = "#64748b"
    elif overall_percentage > 90:
        performance_label = "Excellent"
        performance_color = "#8b5cf6" # Purple
    elif overall_percentage > 80:
        performance_label = "Good"
        performance_color = "var(--success)"
    elif overall_percentage >= 50:
        performance_label = "Average"
        performance_color = "var(--warning)"
    elif overall_percentage >= 30:
        performance_label = "Poor"
        performance_color = "#f97316" # Orange
    else:
        performance_label = "Very Bad"
        performance_color = "var(--danger)"
    
    context = {
        'student_id': pk,
        'attendances': attendances,
        'marks': marks,
        'warnings': warnings,
        'performance_label': performance_label,
        'performance_color': performance_color,
    }
    return render(request, 'admin/admin_student_detail.html', context)

@login_required
def admin_teachers(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'admin/admin_teachers.html')

@login_required

@login_required
def admin_classrooms(request):
    if getattr(request.user, 'role', None) != 'admin' and not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_classroom':
            standard = request.POST.get('standard')
            section = request.POST.get('section')
            if standard and section:
                try:
                    Classroom.objects.create(standard=standard, section=section)
                    messages.success(request, f'Classroom {standard}-{section} added successfully.')
                except Exception as e:
                    messages.error(request, f'Error creating classroom: {str(e)}')
            else:
                messages.error(request, 'Standard and section are required.')
        else:
            classroom_id = request.POST.get('classroom_id')
            teacher_id = request.POST.get('teacher_id')
            
            try:
                classroom = Classroom.objects.get(id=classroom_id)
                if teacher_id:
                    teacher = Teacher.objects.get(id=teacher_id)
                    classroom.class_teacher = teacher
                else:
                    classroom.class_teacher = None
                classroom.save()
                messages.success(request, f'Class teacher updated successfully for {classroom.standard}-{classroom.section}.')
            except Exception as e:
                messages.error(request, f'Error updating class teacher: {str(e)}')
            
        return redirect('admin_classrooms')

    classrooms = Classroom.objects.all().order_by('standard', 'section')
    teachers = Teacher.objects.all()
    return render(request, 'admin/admin_classrooms.html', {'classrooms': classrooms, 'teachers': teachers})

def admin_students(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'admin/admin_students.html')

@login_required
def admin_announcements(request):
    if not request.user.is_superuser:
        return redirect('login')

    from school.models import Announcement
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if title and content:
            Announcement.objects.create(
                teacher=None, # Admin posting
                title=title,
                content=content,
                category=category,
                image=image
            )
            messages.success(request, 'Announcement posted successfully!')
            return redirect('admin_announcements')
            
    announcements = Announcement.objects.all().order_by('-date_posted')
    return render(request, 'admin/admin_announcements.html', {'announcements': announcements})

@login_required
def admin_leave_requests(request):
    if not request.user.is_superuser:
        return redirect('login')
    
    from school.models import LeaveRequest, Notification
    
    # Mark leave request notifications as read
    Notification.objects.filter(user=request.user, is_read=False, link__icontains='leave-requests').update(is_read=True)
    
    leave_requests = LeaveRequest.objects.all().select_related('user').order_by('-date_applied')
    return render(request, 'admin/admin_leave_requests.html', {'leave_requests': leave_requests})


def get_timetable_grid(tt_entries):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    time_slots = [
        (1, "07:00 AM - 07:35 AM"),
        (2, "07:35 AM - 08:10 AM"),
        (3, "08:10 AM - 08:45 AM"),
        (4, "08:45 AM - 09:20 AM"),
        ("BREAK", "09:20 AM - 09:50 AM"),
        (5, "09:50 AM - 10:25 AM"),
        (6, "10:25 AM - 11:00 AM"),
        (7, "11:00 AM - 11:30 AM"),
        (8, "11:30 AM - 12:00 PM")
    ]
    
    tt_dict = {}
    if tt_entries:
        for t in tt_entries:
            tt_dict[(t.period_number, t.day)] = t
            
    grid = []
    for slot in time_slots:
        period_num = slot[0]
        time_str = slot[1]
        
        if period_num == "BREAK":
            grid.append({
                'is_break': True,
                'time': time_str
            })
        else:
            day_data = []
            for d in days:
                day_data.append(tt_dict.get((period_num, d), None))
                
            grid.append({
                'is_break': False,
                'period': period_num,
                'time': time_str,
                'days': day_data
            })
    return grid, days

@login_required
def admin_timetable(request):
    if getattr(request.user, 'role', None) != 'admin' and not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
        
    classrooms = Classroom.objects.all().order_by('standard', 'section')
    
    timetable_grids = {}
    days = []
    for c in classrooms:
        tt_entries = Timetable.objects.filter(classroom=c)
        grid, days = get_timetable_grid(tt_entries)
        timetable_grids[c] = grid
        
    return render(request, 'admin/admin_timetable.html', {'timetable_grids': timetable_grids, 'days': days})

@login_required
def teacher_timetable(request):
    if getattr(request.user, 'role', None) != 'teacher':
        return HttpResponse('Unauthorized', status=401)
    
    try:
        teacher = request.user.teacher_profile
        tt_entries = Timetable.objects.filter(teacher=teacher)
        grid, days = get_timetable_grid(tt_entries)
    except Exception:
        grid, days = get_timetable_grid([])
        
    return render(request, 'authentication/teacher_timetable.html', {'grid': grid, 'days': days})

@login_required
def student_timetable(request):
    if getattr(request.user, 'role', None) != 'student':
        return HttpResponse('Unauthorized', status=401)
    
    try:
        student = request.user.student_profile
        tt_entries = Timetable.objects.filter(classroom=student.classroom)
        grid, days = get_timetable_grid(tt_entries)
    except Exception:
        grid, days = get_timetable_grid([])
        
    return render(request, 'authentication/student_timetable.html', {'grid': grid, 'days': days})


from django.http import JsonResponse
from school.models import Notification

def mark_notifications_read(request):
    if request.user.is_authenticated and request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def student_notifications(request):
    if getattr(request.user, 'role', None) != 'student':
        return redirect('login')
    from school.models import StudentWarning, Student
    from django.shortcuts import get_object_or_404
    student = get_object_or_404(Student, user=request.user)
    warnings = StudentWarning.objects.filter(student=student).order_by('-date_issued')
    return render(request, 'authentication/student_notifications.html', {'warnings': warnings})

@login_required
def teacher_notifications(request):
    if getattr(request.user, 'role', None) != 'teacher':
        return redirect('login')
    from school.models import TeacherWarning, Teacher
    from django.shortcuts import get_object_or_404
    teacher = get_object_or_404(Teacher, user=request.user)
    warnings = TeacherWarning.objects.filter(teacher=teacher).order_by('-date_issued')
    return render(request, 'authentication/teacher_notifications.html', {'warnings': warnings})


@login_required
def admin_add_student(request):
    if getattr(request.user, 'role', None) != 'admin':
        messages.error(request, "Access denied.")
        return redirect('login')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        classroom_id = request.POST.get('classroom_id')

        import random
        base_username = f"{first_name.lower()}.{last_name.lower()}"
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{random.randint(10, 9999)}"
        
        password = "Student@123"
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student'
            )
            
            classroom = Classroom.objects.get(id=classroom_id) if classroom_id else None
            student = Student.objects.create(user=user, classroom=classroom)
            
            messages.success(request, f"Student {first_name} {last_name} added successfully! ID: {student.student_id} | Username: {username} | Password: {password}")
            return redirect('admin_students')
            
        except Exception as e:
            messages.error(request, f"Error adding student: {str(e)}")
            return redirect('admin_add_student')

    classrooms = Classroom.objects.all().order_by('standard', 'section')
    return render(request, 'admin/admin_add_student.html', {'classrooms': classrooms})

@login_required
def admin_add_teacher(request):
    if getattr(request.user, 'role', None) != 'admin':
        messages.error(request, "Access denied.")
        return redirect('login')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        subject_id = request.POST.get('subject_id')
        qualification = request.POST.get('qualification', '').strip()
        base_salary = request.POST.get('base_salary', '0.00')

        import random
        base_username = f"{first_name.lower()}.{last_name.lower()}"
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{random.randint(10, 9999)}"
        
        password = "Teacher@123"
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='teacher'
            )
            
            subject = Subject.objects.get(id=subject_id) if subject_id else None
            teacher = Teacher.objects.create(
                user=user, 
                specialty_subject=subject,
                qualification=qualification,
                base_salary=base_salary
            )
            
            messages.success(request, f"Teacher {first_name} {last_name} added successfully! ID: {teacher.teacher_id} | Username: {username} | Password: {password}")
            return redirect('admin_teachers')
            
        except Exception as e:
            messages.error(request, f"Error adding teacher: {str(e)}")
            return redirect('admin_add_teacher')

    subjects = Subject.objects.all().order_by('name')
    return render(request, 'admin/admin_add_teacher.html', {'subjects': subjects})

