import os
import re

standard_css = '''
        /* Sidebar */
        .sidebar {
            width: 280px;
            background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
            color: white;
            display: flex;
            flex-direction: column;
            box-shadow: 4px 0 10px rgba(0,0,0,0.1);
        }

        .sidebar-header {
            padding: 2rem 1.5rem;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            background: rgba(0,0,0,0.2);
        }

        .sidebar-header h2 {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #a5b4fc;
            margin: 0;
        }

        .sidebar-nav {
            padding: 1.5rem 0;
            flex-grow: 1;
            overflow-y: auto;
        }

        .sidebar-link {
            display: flex;
            align-items: center;
            padding: 1rem 1.5rem;
            color: #e0e7ff;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
            border-left: 4px solid transparent;
        }

        .sidebar-link:hover {
            background: rgba(255,255,255,0.1);
            color: white;
            border-left-color: #818cf8;
        }

        .sidebar-link.active {
            background: rgba(255,255,255,0.15);
            color: white;
            border-left-color: var(--primary);
            font-weight: 600;
        }

        .sidebar-icon {
            margin-right: 1rem;
            font-size: 1.2rem;
            width: 20px;
            text-align: center;
        }

        .logout-btn {
            display: block;
            padding: 0.75rem;
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            text-align: center;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .logout-btn:hover {
            background: var(--danger);
            color: white;
            text-decoration: none;
        }
'''

standard_html = '''
    <!-- Sidebar -->
    <aside class="sidebar">
        <div class="sidebar-header">
            <h2>Teacher Panel</h2>
        </div>
        <nav class="sidebar-nav">
            <a href="{% url 'teacher_dashboard' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_dashboard' %}active{% endif %}">
                <span class="sidebar-icon">🏠</span> Dashboard
            </a>
            <a href="{% url 'teacher_attendance' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_attendance' %}active{% endif %}">
                <span class="sidebar-icon">📅</span> Attendance
            </a>
            <a href="{% url 'teacher_manage_students' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_manage_students' %}active{% endif %}">
                <span class="sidebar-icon">👥</span> Manage Students
            </a>
            <a href="{% url 'teacher_exams' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_exams' %}active{% endif %}">
                <span class="sidebar-icon">📝</span> Exams & Marks
            </a>
            <a href="{% url 'teacher_timetable' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_timetable' %}active{% endif %}">
                <span class="sidebar-icon">📅</span> Timetable
            </a>
            <a href="{% url 'teacher_announcements' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_announcements' %}active{% endif %}">
                <span class="sidebar-icon">📢</span> Announcement {% if unread_announcements_count > 0 %}<span style="background: #ef4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; margin-left: auto; font-weight: bold; min-width: 15px; height: 15px; display: inline-flex; align-items: center; justify-content: center;">{{ unread_announcements_count }}</span>{% endif %}
            </a>
            <a href="{% url 'teacher_leave_requests' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_leave_requests' %}active{% endif %}">
                <span class="sidebar-icon">📄</span> Leave Requests {% if unread_leave_requests_count > 0 %}<span style="background: #ef4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; margin-left: auto; font-weight: bold; min-width: 15px; height: 15px; display: inline-flex; align-items: center; justify-content: center;">{{ unread_leave_requests_count }}</span>{% endif %}
            </a>
            <a href="{% url 'about_teacher' %}" class="sidebar-link {% if request.resolver_match.url_name == 'about_teacher' %}active{% endif %}">
                <span class="sidebar-icon">👤</span> About Teacher
            </a>
            <a href="{% url 'teacher_notifications' %}" class="sidebar-link {% if request.resolver_match.url_name == 'teacher_notifications' %}active{% endif %}">
                <span class="sidebar-icon">🔔</span> Notifications
            </a>
        </nav>
        <div style="padding: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <a href="{% url 'login' %}" class="logout-btn">
                <i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i> Logout
            </a>
        </div>
    </aside>
'''

files_to_update = []
for root, dirs, files in os.walk(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'):
    for file in files:
        if file == 'about_teacher.html' or (file.startswith('teacher_') and file.endswith('.html')):
            files_to_update.append(os.path.join(root, file))

for filepath in files_to_update:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the CSS block
    # We find .sidebar { and we replace everything up to but not including /* Main Content Styles */ or .main-wrapper {
    
    # Try finding the start of sidebar CSS
    css_start = content.find('.sidebar {')
    if css_start == -1:
        # Some might have '/* Sidebar */'
        css_start = content.find('/* Sidebar */')
        if css_start != -1:
            css_start = content.find('.sidebar {', css_start)
    
    # Try finding the end of sidebar CSS (start of main content CSS)
    css_end = content.find('/* Main Content Styles */', css_start)
    if css_end == -1:
        css_end = content.find('/* Main Content */', css_start)
    if css_end == -1:
        css_end = content.find('.main-wrapper {', css_start)
    if css_end == -1:
        css_end = content.find('.main-content {', css_start)

    # Note: .logout-btn might be below .sidebar-icon or it might not exist in old files. 
    # If the old file doesn't have .logout-btn CSS, the standard CSS block will just supply it.

    if css_start != -1 and css_end != -1:
        # Go backwards from css_start to capture any preceding comments like /* Sidebar */
        # But let's just insert standard_css
        content = content[:css_start] + standard_css.strip() + '\n\n        ' + content[css_end:]
    
    # 2. Replace the HTML block
    # Find <aside class="sidebar">
    html_start = content.find('<aside class="sidebar">')
    if html_start == -1:
        html_start = content.find('<!-- Sidebar -->\n    <aside class="sidebar">')

    # Find </aside>
    html_end = content.find('</aside>', html_start)
    if html_end != -1:
        html_end += len('</aside>')
        
    if html_start != -1 and html_end != -1:
        content = content[:html_start] + standard_html.strip() + content[html_end:]
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {os.path.basename(filepath)}')
