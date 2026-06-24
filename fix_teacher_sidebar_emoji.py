import os

nav_item_teacher = '''            <a href="{% url 'teacher_notifications' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_notifications' %}active{% endif %}">
                <span class="sidebar-icon">🔔</span> Notifications
            </a>
'''

files_to_update = []
for root, dirs, files in os.walk(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'):
    for file in files:
        if file == 'about_teacher.html' or (file.startswith('teacher_') and file.endswith('.html')):
            files_to_update.append(os.path.join(root, file))

for filepath in files_to_update:
    with open(filepath, 'r', encoding='utf-8') as f:
        t_content = f.read()
        
    updated = False
    
    if 'teacher_notifications' in t_content:
        # replace the old <i class="fas fa-bell"></i> Notifications with 🔔 Notifications
        new_content = t_content.replace('<i class="fas fa-bell"></i></span> Notifications', '🔔</span> Notifications')
        if new_content != t_content:
            t_content = new_content
            updated = True
    else:
        # insert the nav item
        if '</nav>' in t_content:
            t_content = t_content.replace('</nav>', nav_item_teacher + '        </nav>')
            updated = True
            
    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(t_content)
        print(f'Updated {os.path.basename(filepath)}')
