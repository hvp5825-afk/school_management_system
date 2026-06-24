import os
import re

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

def inject_badge(content, url_name, badge_var, text_keyword):
    # We want to find the link for the given url_name
    # Example: <a href="{% url 'teacher_announcements' %}" ...>
    # ...
    # </a>
    
    # regex to find the <a> tag and its contents up to </a>
    pattern = r'(<a\s+[^>]*href="{% url \'' + url_name + r'\' %}"[^>]*>)(.*?)(</a>)'
    
    def replacer(match):
        open_a = match.group(1)
        inner_html = match.group(2)
        close_a = match.group(3)
        
        # If the badge is already there, don't add it again
        if badge_var in inner_html:
            return match.group(0)
        
        badge_html = f" {{% if {badge_var} > 0 %}}<span style=\"background: #ef4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; margin-left: auto; font-weight: bold; min-width: 15px; height: 15px; display: inline-flex; align-items: center; justify-content: center;\">{{{{ {badge_var} }}}}</span>{{% endif %}}"
        
        return open_a + inner_html.rstrip() + badge_html + '\n            ' + close_a

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    return new_content

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        if 'student_' in filename or filename == 'student_base.html':
            content = inject_badge(content, 'student_announcements', 'unread_announcements_count', 'Announcement')
            
        elif 'teacher_' in filename or filename == 'about_teacher.html' or filename == 'manage_attendance.html':
            content = inject_badge(content, 'teacher_announcements', 'unread_announcements_count', 'Announcement')
            content = inject_badge(content, 'teacher_leave_requests', 'unread_leave_requests_count', 'Leave Requests')
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print('Injected badge into', filename)
