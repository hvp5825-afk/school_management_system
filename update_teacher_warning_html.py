import os

filepath = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_teacher_detail.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

warning_html = '''
    <!-- Warning History -->
    <div class="card" style="margin-top: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h3 style="margin: 0; color: #0f172a;">Warning History</h3>
            <button onclick="document.getElementById('warning-modal').style.display='flex'" class="btn" style="background: var(--danger); color: white;"><i class="fas fa-exclamation-triangle"></i> Issue Warning</button>
        </div>
        
        <div style="overflow-x: auto;">
            <table class="table">
                <thead>
                    <tr>
                        <th>Date Issued</th>
                        <th>Warning Reason</th>
                        <th>Issued By</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for warn in warnings %}
                    <tr>
                        <td style="white-space: nowrap;">{{ warn.date_issued|date:"d M Y, h:i A" }}</td>
                        <td>{{ warn.message }}</td>
                        <td>{{ warn.issued_by.get_full_name|default:warn.issued_by.username }}</td>
                        <td>
                            {% if warn.is_read %}
                                <span style="color: var(--success);"><i class="fas fa-check-circle"></i> Read</span>
                            {% else %}
                                <span style="color: var(--warning);"><i class="fas fa-clock"></i> Unread</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" style="text-align: center; color: #64748b;">No warnings issued.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Warning Modal -->
    <div id="warning-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;">
        <div class="card" style="width: 100%; max-width: 500px; position: relative;">
            <span onclick="document.getElementById('warning-modal').style.display='none'" style="position: absolute; top: 1rem; right: 1.5rem; font-size: 1.5rem; cursor: pointer; color: #94a3b8;">&times;</span>
            <h2 style="margin-top: 0; color: var(--danger);"><i class="fas fa-exclamation-triangle"></i> Issue Warning</h2>
            <p style="color: #64748b; margin-bottom: 1rem;">This warning will be displayed prominently on the teacher's dashboard.</p>
            
            <form id="warning-form">
                <textarea id="warning-message" rows="4" required placeholder="Type the warning reason..." style="width: 100%; padding: 0.8rem; border-radius: 6px; border: 1px solid #cbd5e1; margin-bottom: 1rem; resize: vertical;"></textarea>
                
                <div style="display: flex; justify-content: flex-end;">
                    <button type="button" onclick="document.getElementById('warning-modal').style.display='none'" class="btn" style="background: #e2e8f0; color: #475569; margin-right: 0.5rem;">Cancel</button>
                    <button type="submit" class="btn" style="background: var(--danger); color: white;">Send Warning</button>
                </div>
            </form>
        </div>
    </div>
'''

js_html = '''
    // Warning Form Submit
    document.getElementById('warning-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const msg = document.getElementById('warning-message').value;
        
        fetch('/api/teacher-warnings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                teacher: '{{ teacher.id }}',
                message: msg
            })
        })
        .then(res => {
            if(res.ok) {
                window.location.reload(); // Reload to show new warning in the table
            } else {
                alert('Error sending warning');
            }
        })
        .catch(err => {
            console.error(err);
            alert('Error sending warning');
        });
    });
'''

# insert warning_html before {% endblock %} content
parts = content.split('{% endblock %}')
if len(parts) >= 2 and '<!-- Warning History -->' not in content:
    content = parts[0] + warning_html + '\n{% endblock %}' + parts[1] + '\n{% endblock %}'
    content = content.replace('</script>\n{% endblock %}', js_html + '\n</script>\n{% endblock %}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated admin_teacher_detail.html')
else:
    print('Already updated or endblock not found')
