import os

nav_item_student = '''            <a href="{% url 'student_notifications' %}" class="sidebar-link {% if request.resolver_match.url_name == 'student_notifications' %}active{% endif %}">
                <span class="sidebar-icon"><i class="fas fa-bell"></i></span> Notifications
            </a>
'''

with open(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'student_notifications' not in content:
    content = content.replace('</nav>', nav_item_student + '        </nav>')
    with open(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated student_base.html")

nav_item_teacher = '''            <a href="{% url 'teacher_notifications' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_notifications' %}active{% endif %}">
                <span class="sidebar-icon"><i class="fas fa-bell"></i></span> Notifications
            </a>
'''

for root, dirs, files in os.walk(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'):
    for file in files:
        if file.startswith('teacher_') and file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                t_content = f.read()
            if '</nav>' in t_content and 'teacher_notifications' not in t_content:
                t_content = t_content.replace('</nav>', nav_item_teacher + '        </nav>')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(t_content)
                print(f"Updated {file}")
