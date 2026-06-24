import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_timetable.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = '''
        <div class="container">
            <div class="card" style="padding: 2rem;">
                <h2 style="border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; color: #1e293b;">📅 My Master Timetable</h2>
                <div style="overflow-x: auto; margin-top: 1rem;">
                    <table class="table" style="width: 100%; min-width: 800px; text-align: center; border-collapse: collapse;">
                        <thead>
                            <tr>
                                <th style="width: 100px; background: var(--primary); color: white; text-align: center; padding: 1rem;">Period \ Day</th>
                                {% for day in days %}
                                    <th style="background: var(--primary); color: white; text-align: center; padding: 1rem;">{{ day }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for period, day_dict in grid.items %}
                            <tr>
                                <td style="font-weight: 600; background: #f8fafc; border: 1px solid var(--border); padding: 1rem; color: #334155;">
                                    Lecture {{ period }}
                                </td>
                                {% for day, t in day_dict.items %}
                                    <td style="border: 1px solid var(--border); padding: 0.75rem;">
                                        {% if t %}
                                            <div style="font-weight: 600; color: #0f172a;">{{ t.subject.name }}</div>
                                            <div style="font-size: 0.85em; color: var(--primary); margin-top: 5px; font-weight: 500;">Class {{ t.classroom.standard }}-{{ t.classroom.section }}</div>
                                        {% else %}
                                            <span style="color: #cbd5e1;">Free Period</span>
                                        {% endif %}
                                    </td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
'''

content = re.sub(r'<div class="container">.*</div>', new_content, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
