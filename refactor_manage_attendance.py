import os
import re

filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\manage_attendance.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the body parts we need
container_start = content.find('<div class="container">')
container_end = content.find('<!-- Exit Safeguard Modal -->')

container_content = content[container_start:container_end]

modal_start = content.find('<!-- Exit Safeguard Modal -->')
modal_end = content.find('<script>')

modal_content = content[modal_start:modal_end]

script_start = content.find('<script>')
script_end = content.find('</script>') + 9

script_content = content[script_start:script_end]

new_html = '''{% extends 'authentication/teacher_base.html' %}

{% block page_title %}<i class="fas fa-calendar-check"></i> Manage Attendance - {{ classroom }}{% endblock %}

{% block extra_css %}
<style>
    .student-item {
        padding: 1rem;
        border-bottom: 1px solid var(--border);
        cursor: pointer;
        transition: background 0.2s;
        border-radius: 0.5rem;
    }
    .student-item:hover {
        background: #f9fafb;
    }
    .student-item.active {
        background: #e0e7ff;
        border-left: 4px solid var(--primary);
    }
    
    .att-btn {
        padding: 0.4rem 0.8rem;
        border: 1px solid var(--border);
        background: white;
        color: var(--text-main);
        border-radius: 0.3rem;
        cursor: pointer;
        font-weight: 600;
        margin-right: 0.5rem;
        transition: all 0.2s;
    }
    .att-btn.present.active {
        background: #10b981; /* Success Green */
        color: white;
        border-color: #10b981;
    }
    .att-btn.absent.active {
        background: #ef4444; /* Danger Red */
        color: white;
        border-color: #ef4444;
    }
</style>
{% endblock %}

{% block content %}
''' + container_content + '\n' + modal_content + '''
{% endblock %}

{% block extra_js %}
''' + script_content + '''
{% endblock %}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Refactored manage_attendance.html to use teacher_base.html")
