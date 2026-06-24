import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_view = r'@login_required\s*\n\s*def teacher_manage_students\(request\):[\s\S]*?return render\(request, \'authentication/teacher_manage_students.html\'\)'

new_view = '''@login_required
def teacher_manage_students(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove':
            student_id = request.POST.get('student_id')
            try:
                student = Student.objects.get(id=student_id)
                user_to_delete = student.user
                student.delete()
                user_to_delete.delete()
                messages.success(request, "Student admission cancelled and removed successfully!")
            except Exception as e:
                messages.error(request, f"Error removing student: {str(e)}")
            return redirect('teacher_manage_students')

    search_query = request.GET.get('search_query', '').strip()
    classroom_id = request.GET.get('classroom_id', '')

    students = Student.objects.select_related('user', 'classroom').all()
    
    if search_query:
        from django.db.models import Q
        students = students.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(student_id__icontains=search_query)
        )
    if classroom_id:
        students = students.filter(classroom_id=classroom_id)
        
    classrooms = Classroom.objects.all()

    return render(request, 'authentication/teacher_manage_students.html', {
        'students': students,
        'classrooms': classrooms,
        'search_query': search_query,
        'selected_classroom': classroom_id
    })'''

if re.search(old_view, content):
    content = re.sub(old_view, new_view, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated views.py successfully')
else:
    print('Not found')
