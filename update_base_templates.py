import os
import re

teacher_base_path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html'
admin_base_path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html'
student_base_path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html'

with open(teacher_base_path, 'r', encoding='utf-8') as f:
    teacher_base = f.read()

def update_base_template(path, title, role, icon_class, logo_text):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract nav
    start_nav = content.find('<nav class="sidebar-nav">')
    end_nav = content.find('</nav>', start_nav) + 6
    if start_nav == -1 or end_nav < 6:
        print(f"Could not find nav in {path}")
        return
        
    nav_content = content[start_nav:end_nav]
    
    # Generate new content
    new_content = teacher_base
    
    # Replace nav
    start_t_nav = new_content.find('<nav class="sidebar-nav">')
    end_t_nav = new_content.find('</nav>', start_t_nav) + 6
    new_content = new_content[:start_t_nav] + nav_content + new_content[end_t_nav:]
    
    # Replace title
    new_content = new_content.replace('Teacher Panel</title>', f'{title}</title>')
    new_content = new_content.replace('<i class="fas fa-chalkboard-teacher"></i> Teacher Portal', f'<i class="{icon_class}"></i> {title}')
    
    # Replace role
    new_content = new_content.replace('<span class="user-role">Teacher</span>', f'<span class="user-role">{role}</span>')
    
    # Replace logo
    new_content = new_content.replace('<h2>EduPanel</h2>', f'<h2>{logo_text}</h2>')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {os.path.basename(path)}")

update_base_template(admin_base_path, "Admin Portal", "Administrator", "fas fa-user-shield", "AdminPanel")
update_base_template(student_base_path, "Student Portal", "Student", "fas fa-user-graduate", "StudentPanel")
