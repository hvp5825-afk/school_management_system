import os
import re

with open('authentication/templates/authentication/teacher_dashboard.html', 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# Extract everything up to <div class="container">
match = re.search(r'(.*?)<div class="container">', dashboard_html, re.DOTALL)
if not match:
    print("Failed to find container start")
    exit(1)

head_and_sidebar = match.group(1)
# Update the title
head_and_sidebar = head_and_sidebar.replace('<title>Teacher Dashboard</title>', '<title>About Teachers | Teacher Panel</title>')
# Update active class in sidebar (optional but good practice)
head_and_sidebar = head_and_sidebar.replace('class="sidebar-link active"', 'class="sidebar-link"')
head_and_sidebar = head_and_sidebar.replace('<span class="sidebar-icon">👤</span> About Teacher', '<span class="sidebar-icon">👤</span> About Teacher') # We will fix the href globally later

premium_content = """
<style>
    .teacher-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }

    .teacher-card {
        background: #ffffff;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        padding: 2rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #f3f4f6;
        position: relative;
        overflow: hidden;
    }

    .teacher-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    .teacher-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 80px;
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        z-index: 0;
    }

    .teacher-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: #fff;
        border: 4px solid #fff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        margin: 0 auto 1rem auto;
        position: relative;
        z-index: 1;
        margin-top: 10px;
    }

    .teacher-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }

    .teacher-qualification {
        display: inline-block;
        background: #e0e7ff;
        color: #4338ca;
        padding: 0.4rem 1rem;
        border-radius: 2rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .teacher-subject {
        color: #6b7280;
        font-size: 0.95rem;
    }
    
    .current-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #f59e0b;
        color: #fff;
        font-size: 0.7rem;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-weight: bold;
        z-index: 2;
    }
</style>

<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 800; color: #1f2937;">Our Faculty</h1>
    <p style="color: #6b7280; font-size: 1.1rem;">Meet the dedicated teachers guiding our students.</p>
</div>

<div class="teacher-grid">
    {% for t in teachers %}
    <div class="teacher-card">
        {% if t == current_teacher %}
            <div class="current-badge">YOU</div>
        {% endif %}
        <div class="teacher-avatar">👨‍🏫</div>
        <h3 class="teacher-name">{{ t.user.first_name }} {{ t.user.last_name }}</h3>
        
        {% if t.qualification %}
            <div class="teacher-qualification">🎓 {{ t.qualification }}</div>
        {% else %}
            <div class="teacher-qualification" style="background: #f3f4f6; color: #6b7280;">🎓 Qualification Pending</div>
        {% endif %}
        
        <div class="teacher-subject">
            {% if t.specialty_subject %}
                📚 Specializes in <strong>{{ t.specialty_subject.name }}</strong>
            {% else %}
                📚 General Faculty
            {% endif %}
        </div>
    </div>
    {% endfor %}
</div>
"""

final_html = head_and_sidebar + """
<div class="container">
    """ + premium_content + """
</div>
</main>
</body>
</html>
"""

with open('authentication/templates/authentication/about_teacher.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Created about_teacher.html")
