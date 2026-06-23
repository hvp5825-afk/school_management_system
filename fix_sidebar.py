import os

files = [
    'authentication/templates/authentication/teacher_exams.html',
    'authentication/templates/authentication/teacher_attendance.html',
    'authentication/templates/authentication/teacher_add_student.html',
    'authentication/templates/authentication/manage_attendance.html'
]

old_str = '<a href="#" class="sidebar-link" onclick="alert(\'Announcement feature coming soon!\')">'
new_str = '<a href="{% url \'teacher_announcements\' %}" class="sidebar-link {% if request.resolver_match.url_name == \'teacher_announcements\' %}active{% endif %}">'

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace(old_str, new_str)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
    else:
        print(f"File not found: {f}")
