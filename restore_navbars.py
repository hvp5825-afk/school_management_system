import os
import re

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

teacher_navbar = '''<div class="navbar">
            <div style="font-weight: 800; color: var(--primary); font-size: 2.2rem; text-align: center; width: 100%; text-transform: capitalize;">
                Welcome {{ teacher.user.first_name }} {{ teacher.user.last_name }} Panel
            </div>
        </div>

        <div class="container">'''

student_navbar = '''<div class="navbar">
            <div style="font-weight: 800; color: var(--primary); font-size: 2.2rem; text-align: center; width: 100%; text-transform: capitalize;">
                Welcome {{ student.user.first_name }} {{ student.user.last_name }} Panel
            </div>
        </div>

        <div class="container">'''

admin_navbar = '''<div class="navbar">
        <h2 style="margin: 0;">School Management</h2>
        <div style="font-weight: 500;">
            Welcome, Administrator | 
            <a href="{% url 'login' %}" style="color:white; margin-left: 10px; text-decoration: underline;">Logout</a>
        </div>
    </div>

    <div class="container">'''

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the start of the navbar
        navbar_start = content.find('<div class="navbar"')
        if navbar_start == -1:
            continue
            
        # Find the container start
        container_start = content.find('<div class="container">', navbar_start)
        if container_start == -1:
            continue
            
        end_idx = container_start + len('<div class="container">')

        # Determine which navbar to use based on filename
        if filename == 'admin_dashboard.html':
            replacement = admin_navbar
        elif 'student_' in filename:
            replacement = student_navbar
        else:
            replacement = teacher_navbar

        new_content = content[:navbar_start] + replacement + content[end_idx:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Fixed navbar in', filename)
