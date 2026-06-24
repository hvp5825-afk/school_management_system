import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_manage_students.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = '''
        <div class="container">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: var(--text); font-size: 2.2rem; margin-bottom: 0.5rem;">Manage Students</h1>
                <p style="color: #6b7280; font-size: 1.1rem;">Add new students or cancel admission for existing ones.</p>
            </div>
            
            <div style="margin-bottom: 2rem; display: flex; justify-content: flex-end;">
                <a href="{% url 'teacher_add_student' %}" class="btn" style="background: var(--primary); color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 0.5rem; display: inline-flex; align-items: center; font-weight: 600;">
                    <i class="fas fa-user-plus" style="margin-right: 0.5rem;"></i> Add New Student
                </a>
            </div>

            <div class="card" style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                {% if messages %}
                    {% for message in messages %}
                        <div style="padding: 1rem; border-radius: 0.5rem; margin-bottom: 1.5rem; font-weight: 500; {% if message.tags == 'error' %}background-color: #fee2e2; color: #991b1b; border: 1px solid #f87171;{% else %}background-color: #d1fae5; color: #065f46; border: 1px solid #34d399;{% endif %}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}

                <form method="GET" action="{% url 'teacher_manage_students' %}" style="display: flex; gap: 1rem; align-items: flex-end; margin-bottom: 2rem; background: #f8fafc; padding: 1.5rem; border-radius: 0.75rem; border: 1px solid var(--border);">
                    <div style="flex: 2;">
                        <label for="search_query" style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151;">Search by Name or ID</label>
                        <input type="text" id="search_query" name="search_query" style="width: 100%; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: 0.5rem; box-sizing: border-box;" value="{{ search_query }}" placeholder="Enter name or ID...">
                    </div>
                    <div style="flex: 1;">
                        <label for="classroom_id" style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151;">Filter by Class</label>
                        <select id="classroom_id" name="classroom_id" style="width: 100%; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: 0.5rem; box-sizing: border-box;">
                            <option value="">All Classes</option>
                            {% for c in classrooms %}
                            <option value="{{ c.id }}" {% if selected_classroom == c.id|stringformat:"s" %}selected{% endif %}>{{ c.standard }} - {{ c.section }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div>
                        <button type="submit" style="padding: 0.75rem 2rem; background: var(--primary); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer;"><i class="fas fa-search"></i> Search</button>
                    </div>
                </form>

                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="background: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                                <th style="padding: 1rem; font-weight: 600; color: #475569;">Student ID</th>
                                <th style="padding: 1rem; font-weight: 600; color: #475569;">Name</th>
                                <th style="padding: 1rem; font-weight: 600; color: #475569;">Classroom</th>
                                <th style="padding: 1rem; font-weight: 600; color: #475569; text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for student in students %}
                            <tr style="border-bottom: 1px solid #e2e8f0;">
                                <td style="padding: 1rem;">{{ student.student_id }}</td>
                                <td style="padding: 1rem; font-weight: 500;">{{ student.user.get_full_name|default:student.user.username }}</td>
                                <td style="padding: 1rem;">{{ student.classroom|default:"Not Assigned" }}</td>
                                <td style="padding: 1rem; text-align: right;">
                                    <form method="POST" action="{% url 'teacher_manage_students' %}" style="display: inline;" onsubmit="return confirm('Are you sure you want to cancel admission for {{ student.user.get_full_name|escapejs }}? This will remove them permanently.');">
                                        {% csrf_token %}
                                        <input type="hidden" name="action" value="remove">
                                        <input type="hidden" name="student_id" value="{{ student.id }}">
                                        <button type="submit" style="background: #ef4444; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.375rem; cursor: pointer; font-weight: 500; transition: background-color 0.2s;" onmouseover="this.style.background='#dc2626'" onmouseout="this.style.background='#ef4444'">
                                            <i class="fas fa-user-times" style="margin-right: 0.25rem;"></i> Cancel Admission
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="4" style="padding: 2rem; text-align: center; color: #64748b;">No students found matching your criteria.</td>
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
