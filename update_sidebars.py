import os

student_base = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html'
with open(student_base, 'r', encoding='utf-8') as f:
    content = f.read()

nav_item = '''
            <a href="{% url 'student_notifications' %}" class="sidebar-link {% if request.resolver_match.url_name == 'student_notifications' %}active{% endif %}">
                <span class="sidebar-icon"><i class="fas fa-bell"></i></span> Notifications
            </a>
'''
content = content.replace('            <a href="{% url \'logout\' %}" class="sidebar-link">', nav_item + '            <a href="{% url \'logout\' %}" class="sidebar-link">')

with open(student_base, 'w', encoding='utf-8') as f:
    f.write(content)

teacher_base = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_dashboard.html'
with open(teacher_base, 'r', encoding='utf-8') as f:
    t_content = f.read()

t_nav_item = '''
            <a href="{% url 'teacher_notifications' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_notifications' %}active{% endif %}">
                <span class="sidebar-icon"><i class="fas fa-bell"></i></span> Notifications
            </a>
'''
t_content = t_content.replace('            <a href="{% url \'logout\' %}" class="sidebar-link">', t_nav_item + '            <a href="{% url \'logout\' %}" class="sidebar-link">')

with open(teacher_base, 'w', encoding='utf-8') as f:
    f.write(t_content)

# wait, we need to do it for all teacher templates because they don't use teacher_base.html
for root, dirs, files in os.walk(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'):
    for file in files:
        if file.startswith('teacher_') and file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                fc = f.read()
            if '<a href="{% url \'logout\' %}" class="sidebar-link">' in fc and 'teacher_notifications' not in fc:
                fc = fc.replace('            <a href="{% url \'logout\' %}" class="sidebar-link">', t_nav_item + '            <a href="{% url \'logout\' %}" class="sidebar-link">')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fc)
