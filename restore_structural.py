import os
import re

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

teacher_navbar = '''    </aside>

    <!-- Main Content -->
    <main class="main-wrapper">
        <div class="navbar">
            <div style="font-weight: 800; color: var(--primary); font-size: 2.2rem; text-align: center; width: 100%; text-transform: capitalize;">
                Welcome {{ teacher.user.first_name }} {{ teacher.user.last_name }} Panel
            </div>
        </div>
        <div class="container">'''

student_navbar = '''    </aside>

    <!-- Main Content -->
    <main class="main-wrapper">
        <div class="navbar">
            <div style="font-weight: 800; color: var(--primary); font-size: 2.2rem; text-align: center; width: 100%; text-transform: capitalize;">
                Welcome {{ student.user.first_name }} {{ student.user.last_name }} Panel
            </div>
        </div>
        <div class="container">'''

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'admin_' in filename or filename == 'login.html' or filename == 'register.html':
            continue

        # Look for the broken transition from sidebar to container
        # Pattern: Logout block ending, followed by <div class="container"> without aside/main/navbar
        pattern = r'(Logout\s*</a>\s*</div>)\s*<div class="container">'
        
        replacement = r'\1\n' + (student_navbar if 'student_' in filename else teacher_navbar)
        
        new_content, count = re.subn(pattern, replacement, content)
        
        # Also check for alternate logout icon logic in student panel
        if count == 0 and 'student_' in filename:
            pattern2 = r'(Logout\s*</a>\s*</div>)\s*<div class="container">'
            new_content, count = re.subn(pattern2, replacement, content)

        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('Fully restored structural layout in', filename)
