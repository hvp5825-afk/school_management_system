import os

dashboard_path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_dashboard.html'

with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_container = content.find('<div class="container">')
end_main = content.find('</main>')

if start_container != -1 and end_main != -1:
    head_and_nav = content[:start_container]
    footer = content[end_main:]

    notifications_html = '''<div class="container">
        <div class="card" style="margin-top: 2rem;">
            <h2 style="margin-top: 0; color: var(--primary);"><i class="fas fa-bell"></i> Notifications</h2>
            
            <div style="margin-top: 1.5rem;">
                {% for warn in warnings %}
                <div style="padding: 1rem; border-left: 4px solid var(--danger); background: #fff1f2; margin-bottom: 1rem; border-radius: 4px; display: flex; flex-direction: column;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: var(--danger);"><i class="fas fa-exclamation-triangle"></i> Official Notice</span>
                        <span style="font-size: 0.85rem; color: #64748b;">{{ warn.date_issued|date:"d M Y, h:i A" }}</span>
                    </div>
                    <p style="margin: 0; color: #334155;">{{ warn.message }}</p>
                    <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #64748b;">
                        Issued by: {{ warn.issued_by.get_full_name|default:warn.issued_by.username }}
                    </div>
                </div>
                {% empty %}
                <div style="text-align: center; padding: 2rem; color: #64748b;">
                    <i class="fas fa-check-circle" style="font-size: 2rem; color: var(--success); margin-bottom: 1rem;"></i>
                    <p>You have no notifications.</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
'''

    new_page = head_and_nav + notifications_html + footer

    with open(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_notifications.html', 'w', encoding='utf-8') as f:
        f.write(new_page)
    print('Fixed teacher_notifications.html')
else:
    print('Could not parse teacher_dashboard.html properly.')
