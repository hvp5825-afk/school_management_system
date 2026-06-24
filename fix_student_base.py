import os
filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<div class="container">', '{% block content %}{% endblock %}')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
