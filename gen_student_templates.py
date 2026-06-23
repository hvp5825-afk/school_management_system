import os

base_dir = 'authentication/templates/authentication/'

attendance_html = """{% extends 'authentication/student_base.html' %}

{% block student_content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <h2 style="margin: 0;">Attendance Record</h2>
</div>

<div class="card" style="display: flex; gap: 2rem; align-items: center; background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); color: white;">
    <div style="font-size: 3rem; font-weight: 800;">{{ attendance_percentage }}%</div>
    <div>
        <h3 style="margin: 0 0 0.5rem 0; color: white;">Overall Attendance</h3>
        <p style="margin: 0; opacity: 0.9;">You have been present for {{ present_days }} days out of a total of {{ total_days }} days.</p>
    </div>
</div>

<div class="card">
    <h3 style="margin-top: 0;">Detailed History</h3>
    {% if attendances %}
    <table class="table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for record in attendances %}
            <tr>
                <td><strong>{{ record.date|date:"F d, Y" }}</strong></td>
                <td>
                    {% if record.status %}
                        <span style="background: #d1fae5; color: #065f46; padding: 0.3rem 0.8rem; border-radius: 2rem; font-weight: 600; font-size: 0.85rem;">Present</span>
                    {% else %}
                        <span style="background: #fee2e2; color: #991b1b; padding: 0.3rem 0.8rem; border-radius: 2rem; font-weight: 600; font-size: 0.85rem;">Absent</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="color: #6b7280;">No attendance records found.</p>
    {% endif %}
</div>
{% endblock %}
"""

exams_html = """{% extends 'authentication/student_base.html' %}

{% block student_content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <h2 style="margin: 0;">Exams & Marks</h2>
</div>

<div class="card">
    <h3 style="margin-top: 0;">Academic Performance</h3>
    {% if marks %}
    <table class="table">
        <thead>
            <tr>
                <th>Subject</th>
                <th>Exam Name</th>
                <th>Score</th>
                <th>Maximum Score</th>
                <th>Percentage</th>
            </tr>
        </thead>
        <tbody>
            {% for mark in marks %}
            <tr>
                <td><strong>{{ mark.exam.subject.name }}</strong></td>
                <td>{{ mark.exam.name }}</td>
                <td style="font-weight: 700; color: #4f46e5;">{{ mark.score }}</td>
                <td>{{ mark.max_score }}</td>
                <td>
                    <span style="background: #e0e7ff; color: #4338ca; padding: 0.3rem 0.8rem; border-radius: 2rem; font-weight: 600; font-size: 0.85rem;">
                        {% widthratio mark.score mark.max_score 100 %}%
                    </span>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="color: #6b7280;">No marks have been uploaded for you yet.</p>
    {% endif %}
</div>
{% endblock %}
"""

announcements_html = """{% extends 'authentication/student_base.html' %}

{% block extra_css %}
<style>
    .feed-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 2rem;
    }

    .announcement-item {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 1.25rem;
        overflow: hidden;
        transition: all 0.4s ease;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .announcement-item:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }

    .announcement-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-bottom: 1px solid #e5e7eb;
        transition: transform 0.5s ease;
    }
    .announcement-item:hover .announcement-img {
        transform: scale(1.05);
    }

    .announcement-img-wrapper {
        overflow: hidden;
    }

    .announcement-body {
        padding: 1.8rem;
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .badge.exam { background: linear-gradient(45deg, #f87171, #ef4444); color: white; }
    .badge.event { background: linear-gradient(45deg, #c084fc, #a855f7); color: white; }
    .badge.holiday { background: linear-gradient(45deg, #34d399, #10b981); color: white; }
    .badge.general { background: linear-gradient(45deg, #60a5fa, #3b82f6); color: white; }

    .announcement-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.8rem 0;
        color: #1f2937;
        line-height: 1.3;
    }

    .announcement-date {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .announcement-text {
        font-size: 1.05rem;
        color: #4b5563;
        line-height: 1.6;
        flex: 1;
        white-space: pre-wrap;
    }

    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
        background: #f9fafb;
        border: 2px dashed #cbd5e1;
        border-radius: 1.25rem;
        color: #64748b;
        grid-column: 1 / -1;
    }
    .empty-state h3 {
        font-size: 1.8rem;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
</style>
{% endblock %}

{% block student_content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
    <h2 style="margin: 0;">Announcements & Events</h2>
</div>

<div class="feed-grid">
    {% for ann in announcements %}
    <div class="announcement-item">
        {% if ann.image %}
            <div class="announcement-img-wrapper">
                <img src="{{ ann.image.url }}" alt="{{ ann.title }}" class="announcement-img">
            </div>
        {% endif %}
        <div class="announcement-body">
            <div>
                <span class="badge {{ ann.category|lower }}">{{ ann.category }}</span>
            </div>
            <h3 class="announcement-title">{{ ann.title }}</h3>
            <div class="announcement-date">
                🕒 {{ ann.date_posted|date:"F d, Y h:i A" }}
            </div>
            <p class="announcement-text">{{ ann.content }}</p>
        </div>
    </div>
    {% empty %}
    <div class="empty-state">
        <h3>No Announcements</h3>
        <p>There are no current announcements for your class.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""

with open(os.path.join(base_dir, 'student_attendance.html'), 'w', encoding='utf-8') as f:
    f.write(attendance_html)

with open(os.path.join(base_dir, 'student_exams.html'), 'w', encoding='utf-8') as f:
    f.write(exams_html)

with open(os.path.join(base_dir, 'student_announcements.html'), 'w', encoding='utf-8') as f:
    f.write(announcements_html)

print("Generated student templates.")
