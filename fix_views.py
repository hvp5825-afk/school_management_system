import os

filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r"\'announcements\'", "'announcements'")
content = content.replace(r"\'leave-requests\'", "'leave-requests'")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
