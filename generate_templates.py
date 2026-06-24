import os
import re

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates'

# 1. admin_timetable.html
admin_content = '''{% extends "admin/admin_base.html" %}

{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
    <h2><i class="fas fa-calendar-alt" style="color: var(--primary); margin-right: 10px;"></i> School Timetables</h2>
</div>

<div class="card">
    <table class="table">
        <thead>
            <tr>
                <th>Day</th>
                <th>Period</th>
                <th>Classroom</th>
                <th>Subject</th>
                <th>Teacher</th>
            </tr>
        </thead>
        <tbody>
            {% for t in timetables %}
            <tr>
                <td style="font-weight: 600;">{{ t.day }}</td>
                <td>Period {{ t.period_number }}</td>
                <td>{{ t.classroom }}</td>
                <td>{{ t.subject.name }}</td>
                <td>{{ t.teacher.user.first_name }} {{ t.teacher.user.last_name }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" style="text-align: center; color: #64748b; padding: 2rem;">No timetables found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
'''
with open(os.path.join(base_dir, 'admin', 'admin_timetable.html'), 'w', encoding='utf-8') as f:
    f.write(admin_content)

# 2. student_timetable.html
student_content = '''{% extends "authentication/student_base.html" %}

{% block title %}My Timetable{% endblock %}
{% block header %}My Class Timetable{% endblock %}

{% block content %}
<div class="card" style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1e293b;"><span class="icon">📅</span> Weekly Schedule</h3>
    <table class="table" style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
        <thead style="background: #f8fafc;">
            <tr>
                <th style="padding: 1rem; border-bottom: 1px solid #e2e8f0; text-align: left; color: #475569;">Day</th>
                <th style="padding: 1rem; border-bottom: 1px solid #e2e8f0; text-align: left; color: #475569;">Period</th>
                <th style="padding: 1rem; border-bottom: 1px solid #e2e8f0; text-align: left; color: #475569;">Subject</th>
                <th style="padding: 1rem; border-bottom: 1px solid #e2e8f0; text-align: left; color: #475569;">Teacher</th>
            </tr>
        </thead>
        <tbody>
            {% for t in timetables %}
            <tr>
                <td style="padding: 1rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #334155;">{{ t.day }}</td>
                <td style="padding: 1rem; border-bottom: 1px solid #e2e8f0; color: #475569;">Period {{ t.period_number }}</td>
                <td style="padding: 1rem; border-bottom: 1px solid #e2e8f0; color: #475569;">{{ t.subject.name }}</td>
                <td style="padding: 1rem; border-bottom: 1px solid #e2e8f0; color: #475569;">{{ t.teacher.user.first_name }} {{ t.teacher.user.last_name }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" style="padding: 2rem; text-align: center; color: #64748b;">No timetable assigned for your class.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
'''
with open(os.path.join(base_dir, 'authentication', 'student_timetable.html'), 'w', encoding='utf-8') as f:
    f.write(student_content)

# 3. teacher_timetable.html
with open(os.path.join(base_dir, 'authentication', 'teacher_dashboard.html'), 'r', encoding='utf-8') as f:
    teacher_template = f.read()

new_teacher_content = '''
        <div class="container">
            <div class="card">
                <h2>📅 My Timetable</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Day</th>
                            <th>Period</th>
                            <th>Classroom</th>
                            <th>Subject</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for t in timetables %}
                        <tr>
                            <td style="font-weight: 600;">{{ t.day }}</td>
                            <td>Period {{ t.period_number }}</td>
                            <td>{{ t.classroom }}</td>
                            <td>{{ t.subject.name }}</td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="4" style="text-align: center; color: #64748b; padding: 2rem;">No timetables assigned to you.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
'''
teacher_timetable = re.sub(r'<div class="container">.*</div>\s*</main>', new_teacher_content + '\n    </main>', teacher_template, flags=re.DOTALL)
# Make 'teacher_timetable' link active and others inactive
teacher_timetable = teacher_timetable.replace('class="sidebar-link active"', 'class="sidebar-link"')
teacher_timetable = teacher_timetable.replace('href="{% url \'teacher_timetable\' %}" class="sidebar-link"', 'href="{% url \'teacher_timetable\' %}" class="sidebar-link active"')

with open(os.path.join(base_dir, 'authentication', 'teacher_timetable.html'), 'w', encoding='utf-8') as f:
    f.write(teacher_timetable)

print('Templates created successfully')
