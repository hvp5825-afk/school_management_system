import os

filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'

views_code = """
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
"""

with open(filepath, 'a', encoding='utf-8') as f:
    f.write('\n' + views_code + '\n')

print("Success")
