import os
import re

filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

helper_function = '''
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
'''

# Admin Timetable replacement
admin_new = '''def admin_timetable(request):
    if getattr(request.user, 'role', None) != 'admin' and not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)
        
    classrooms = Classroom.objects.all().order_by('standard', 'section')
    
    timetable_grids = {}
    days = []
    for c in classrooms:
        tt_entries = Timetable.objects.filter(classroom=c)
        grid, days = get_timetable_grid(tt_entries)
        timetable_grids[c] = grid
        
    return render(request, 'admin/admin_timetable.html', {'timetable_grids': timetable_grids, 'days': days})'''

# Teacher Timetable replacement
teacher_new = '''def teacher_timetable(request):
    if getattr(request.user, 'role', None) != 'teacher':
        return HttpResponse('Unauthorized', status=401)
    
    try:
        teacher = request.user.teacher_profile
        tt_entries = Timetable.objects.filter(teacher=teacher)
        grid, days = get_timetable_grid(tt_entries)
    except Exception:
        grid, days = get_timetable_grid([])
        
    return render(request, 'authentication/teacher_timetable.html', {'grid': grid, 'days': days})'''

# Student Timetable replacement
student_new = '''def student_timetable(request):
    if getattr(request.user, 'role', None) != 'student':
        return HttpResponse('Unauthorized', status=401)
    
    try:
        student = request.user.student_profile
        tt_entries = Timetable.objects.filter(classroom=student.classroom)
        grid, days = get_timetable_grid(tt_entries)
    except Exception:
        grid, days = get_timetable_grid([])
        
    return render(request, 'authentication/student_timetable.html', {'grid': grid, 'days': days})'''

# Perform replacements using regex
content = re.sub(r'def admin_timetable\(request\):[\s\S]*?return render\(request, \'admin/admin_timetable.html\', [^\n]*\)', admin_new, content)
content = re.sub(r'def teacher_timetable\(request\):[\s\S]*?return render\(request, \'authentication/teacher_timetable\.html\', [^\n]*\)', teacher_new, content)
content = re.sub(r'def student_timetable\(request\):[\s\S]*?return render\(request, \'authentication/student_timetable\.html\', [^\n]*\)', student_new, content)

# Inject the helper function before admin_timetable
if 'def get_timetable_grid' not in content:
    content = content.replace('def admin_timetable(request):', helper_function + '\n' + 'def admin_timetable(request):')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
