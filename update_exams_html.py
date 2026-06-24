import re

path_html = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html'
with open(path_html, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the first form and second form entirely.
# Let's find the start of the Selection Card up to the table start.
pattern = r'<h3 class="card-header">Select Class and Subject</h3>[\s\S]*?(?=<form method="POST")'

new_forms = '''<h3 class="card-header">Select Class and Exam</h3>
            <form method="GET" action="{% url 'teacher_exams' %}" style="display: flex; gap: 1rem; align-items: flex-end;">
                <div style="flex: 1;">
                    <label class="form-label">Class</label>
                    <select name="classroom_id" class="form-select" required>
                        <option value="">-- Select Class --</option>
                        {% for c in unique_classrooms %}
                            <option value="{{ c.id }}" {% if selected_classroom.id == c.id %}selected{% endif %}>
                                {{ c }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div style="flex: 1;">
                    <label class="form-label">Exam Name</label>
                    <select name="exam_name" class="form-select" required>
                        <option value="">-- Select Exam --</option>
                        <option value="Unit Test" {% if selected_exam_name == 'Unit Test' %}selected{% endif %}>Unit Test</option>
                        <option value="Mid Term" {% if selected_exam_name == 'Mid Term' %}selected{% endif %}>Mid Term</option>
                        <option value="Final Exam" {% if selected_exam_name == 'Final Exam' %}selected{% endif %}>Final Exam</option>
                    </select>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary">Select</button>
                </div>
            </form>
            
            {% if selected_classroom and selected_exam_name %}
            <hr style="margin: 2rem 0; border: none; border-top: 1px solid #e5e7eb;">
            
            <h3 class="card-header" style="border:none; margin-bottom: 1rem;">Select Subject for Marks Entry</h3>
            
            <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                <form method="GET" action="{% url 'teacher_exams' %}" style="display: flex; gap: 1rem; align-items: flex-end; background: #f9fafb; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; width: 100%;">
                    <input type="hidden" name="classroom_id" value="{{ selected_classroom.id }}">
                    <input type="hidden" name="exam_name" value="{{ selected_exam_name }}">
                    
                    <div style="display: flex; flex-direction: column; gap: 0.5rem; flex: 1;">
                        <label style="font-weight: 500; font-size: 0.95rem;">Subject</label>
                        <select name="subject_id" class="form-input" required>
                            <option value="">-- Select Subject --</option>
                            {% for s in unique_subjects %}
                                <option value="{{ s.id }}" {% if selected_subject.id == s.id %}selected{% endif %}>{{ s.name }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 0.5rem; flex: 1;">
                        <label style="font-weight: 500; font-size: 0.95rem;">Exam Date</label>
                        <input type="date" name="exam_date" class="form-input" value="{{ selected_date|date:'Y-m-d' }}" required>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <label style="font-weight: 500; font-size: 0.95rem;">Max Score</label>
                        <input type="number" name="max_score" class="form-input" value="{{ selected_exam.max_score|default:100 }}" required style="width: 100px;">
                    </div>
                    
                    <div>
                        <button type="submit" class="btn btn-primary">Load Students</button>
                    </div>
                </form>
            </div>
            {% endif %}
            
            {% if selected_classroom and selected_subject and selected_exam %}
            <div style="margin-top: 2rem; display: flex; justify-content: space-between; align-items: center;">
                <h3 class="card-header" style="margin: 0; border: none;">Enter Marks: {{ selected_subject.name }} ({{ selected_exam_name }})</h3>
                <a href="?classroom_id={{ selected_classroom.id }}&exam_name={{ selected_exam_name }}&subject_id={{ selected_subject.id }}&export_csv=1" class="btn" style="background: #10b981; color: white;">Download CSV</a>
            </div>
            
            '''

if re.search(pattern, content):
    content = re.sub(pattern, new_forms, content)
    with open(path_html, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated teacher_exams.html successfully")
else:
    print("Could not match pattern in teacher_exams.html")
