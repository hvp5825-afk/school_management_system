import re

with open(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html', 'r', encoding='utf-8') as f:
    html = f.read()

links = re.findall(r'<a href="[^"]*" class="sidebar-link[^"]*"', html)
for l in links:
    print(l)
