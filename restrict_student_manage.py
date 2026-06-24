import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# For teacher_add_student
old_add_view = r'''def teacher_add_student\(request\):[\s\S]*?classrooms = Classroom.objects.all\(\)'''
new_add_view = '''def teacher_add_student(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    # Restrict to assigned classroom
    classrooms = []
    if hasattr(request.user, 'teacher_profile') and getattr(request.user.teacher_profile, 'assigned_classroom', None):
        classrooms = [request.user.teacher_profile.assigned_classroom]'''

if re.search(old_add_view, content):
    content = re.sub(old_add_view, new_add_view, content)
    print('Updated teacher_add_student')

# For teacher_remove_student
old_remove_view = r'''def teacher_remove_student\(request\):[\s\S]*?classrooms = Classroom.objects.all\(\)'''
new_remove_view = '''def teacher_remove_student(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    classrooms = []
    if hasattr(request.user, 'teacher_profile') and getattr(request.user.teacher_profile, 'assigned_classroom', None):
        classrooms = [request.user.teacher_profile.assigned_classroom]'''

if re.search(old_remove_view, content):
    content = re.sub(old_remove_view, new_remove_view, content)
    print('Updated teacher_remove_student')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
