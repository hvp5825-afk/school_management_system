import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the form POST action
old_post = r'''<form method="POST" action="{% url 'teacher_exams' %}\?classroom_id={{ selected_classroom.id }}&subject_id={{ selected_subject.id }}&exam_id={{ selected_exam.id }}">'''
new_post = '''<form method="POST" action="{% url 'teacher_exams' %}?classroom_id={{ selected_classroom.id }}&exam_name={{ selected_exam_name }}&subject_id={{ selected_subject.id }}&exam_id={{ selected_exam.id }}">'''
content = re.sub(old_post, new_post, content)

# Replace the Edit button link
old_edit = r'''<a href="\?classroom_id={{ selected_classroom.id }}&subject_id={{ selected_subject.id }}&exam_id={{ selected_exam.id }}&action_type=edit" class="btn btn-primary">Edit Marks</a>'''
new_edit = '''<a href="?classroom_id={{ selected_classroom.id }}&exam_name={{ selected_exam_name }}&subject_id={{ selected_subject.id }}&exam_id={{ selected_exam.id }}&action_type=edit" class="btn btn-primary">Edit Marks</a>'''
content = re.sub(old_edit, new_edit, content)

# Replace the Cancel button link
old_cancel = r'''<a href="\?classroom_id={{ selected_classroom.id }}&subject_id={{ selected_subject.id }}&exam_id={{ selected_exam.id }}&action_type=show" class="btn" style="background: #e5e7eb; color: var\(--text-dark\);">Cancel</a>'''
new_cancel = '''<a href="?classroom_id={{ selected_classroom.id }}&exam_name={{ selected_exam_name }}&subject_id={{ selected_subject.id }}&exam_id={{ selected_exam.id }}&action_type=show" class="btn" style="background: #e5e7eb; color: var(--text-dark);">Cancel</a>'''
content = re.sub(old_cancel, new_cancel, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated POST links in teacher_exams.html")
