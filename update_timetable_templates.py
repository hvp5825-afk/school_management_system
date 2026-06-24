import os

def update_template(filepath, template_type):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_str = '<tbody>'
    end_str = '</tbody>'
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx == -1 or end_idx == -1:
        print(f"Could not find tbody in {filepath}")
        return
        
    if template_type == 'student':
        inner_content = '''
                {% for row in grid %}
                    {% if row.is_break %}
                        <tr>
                            <td colspan="7" style="padding: 1rem; border: 1px solid #e2e8f0; font-weight: 700; color: #ef4444; background: #fee2e2; text-align: center; letter-spacing: 2px;">
                                LUNCH BREAK ({{ row.time }})
                            </td>
                        </tr>
                    {% else %}
                        <tr>
                            <td style="padding: 1rem; border: 1px solid #e2e8f0; font-weight: 600; color: #334155; background: #f8fafc; white-space: nowrap;">
                                Lecture {{ row.period }}<br>
                                <span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">{{ row.time }}</span>
                            </td>
                            {% for t in row.days %}
                                <td style="padding: 0.75rem; border: 1px solid #e2e8f0;">
                                    {% if t %}
                                        <div style="font-weight: 600; color: #0f172a;">{{ t.subject.name }}</div>
                                        <div style="font-size: 0.85em; color: #64748b; margin-top: 5px;">{{ t.teacher.user.first_name }} {{ t.teacher.user.last_name }}</div>
                                    {% else %}
                                        <span style="color: #cbd5e1;">--</span>
                                    {% endif %}
                                </td>
                            {% endfor %}
                        </tr>
                    {% endif %}
                {% endfor %}
            '''
    elif template_type == 'teacher':
        inner_content = '''
                {% for row in grid %}
                    {% if row.is_break %}
                        <tr>
                            <td colspan="7" style="padding: 1rem; border: 1px solid #e2e8f0; font-weight: 700; color: #ef4444; background: #fee2e2; text-align: center; letter-spacing: 2px;">
                                LUNCH BREAK ({{ row.time }})
                            </td>
                        </tr>
                    {% else %}
                        <tr>
                            <td style="padding: 1rem; border: 1px solid #e2e8f0; font-weight: 600; color: #334155; background: #f8fafc; white-space: nowrap;">
                                Lecture {{ row.period }}<br>
                                <span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">{{ row.time }}</span>
                            </td>
                            {% for t in row.days %}
                                <td style="padding: 0.75rem; border: 1px solid #e2e8f0;">
                                    {% if t %}
                                        <div style="font-weight: 600; color: #0f172a;">Class {{ t.classroom.standard }}-{{ t.classroom.section }}</div>
                                        <div style="font-size: 0.85em; color: #64748b; margin-top: 5px;">{{ t.subject.name }}</div>
                                    {% else %}
                                        <span style="color: #cbd5e1;">--</span>
                                    {% endif %}
                                </td>
                            {% endfor %}
                        </tr>
                    {% endif %}
                {% endfor %}
            '''
    elif template_type == 'admin':
        inner_content = '''
                        {% for row in grid %}
                            {% if row.is_break %}
                                <tr>
                                    <td colspan="7" style="padding: 1rem; border: 1px solid #e2e8f0; font-weight: 700; color: #ef4444; background: #fee2e2; text-align: center; letter-spacing: 2px;">
                                        LUNCH BREAK ({{ row.time }})
                                    </td>
                                </tr>
                            {% else %}
                                <tr>
                                    <td style="padding: 1rem; border: 1px solid #e2e8f0; font-weight: 600; color: #334155; background: #f8fafc; white-space: nowrap;">
                                        Lecture {{ row.period }}<br>
                                        <span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">{{ row.time }}</span>
                                    </td>
                                    {% for t in row.days %}
                                        <td style="padding: 0.75rem; border: 1px solid #e2e8f0;">
                                            {% if t %}
                                                <div style="font-weight: 600; color: #0f172a;">{{ t.subject.name }}</div>
                                                <div style="font-size: 0.85em; color: #64748b; margin-top: 5px;">{{ t.teacher.user.first_name }} {{ t.teacher.user.last_name }}</div>
                                            {% else %}
                                                <span style="color: #cbd5e1;">--</span>
                                            {% endif %}
                                        </td>
                                    {% endfor %}
                                </tr>
                            {% endif %}
                        {% endfor %}
                    '''

    new_content = content[:start_idx + len(start_str)] + inner_content + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates'
update_template(os.path.join(base_dir, 'authentication', 'student_timetable.html'), 'student')
update_template(os.path.join(base_dir, 'authentication', 'teacher_timetable.html'), 'teacher')
update_template(os.path.join(base_dir, 'admin', 'admin_timetable.html'), 'admin')
