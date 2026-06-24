import os
import re

dashboard_path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_dashboard.html'
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'<a href="[^"]*" class="sidebar-link[^"]*"', content)
for l in links:
    print(l)
