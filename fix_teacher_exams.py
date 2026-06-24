import os
filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('<!-- Main Content -->')
if start != -1:
    messages_start = content.find('{% if messages %}')
    end = content.rfind('</main>')

    if messages_start != -1 and end != -1:
        inner = content[messages_start:end].strip()
        new_content = f"{{% extends 'authentication/teacher_base.html' %}}\n\n{{% block content %}}\n{inner}\n{{% endblock %}}\n"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Updated teacher_exams.html')
    else:
        print('Could not parse inner bounds')
else:
    print('Could not find <!-- Main Content -->')
