import os

ui_snippet = """
            <!-- Notifications -->
            <div style="position: absolute; right: 2rem; display: flex; align-items: center;">
                <div class="notification-dropdown" style="position: relative;">
                    <button id="notificationBtn" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text); position: relative;">
                        <i class="fas fa-bell"></i>
                        {% if unread_notifications_count > 0 %}
                            <span id="notifBadge" style="position: absolute; top: -5px; right: -5px; background: #ef4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.7rem; font-weight: bold;">
                                {{ unread_notifications_count }}
                            </span>
                        {% endif %}
                    </button>
                    <div id="notificationMenu" style="display: none; position: absolute; right: 0; top: 40px; background: white; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-radius: 8px; width: 300px; z-index: 50; text-align: left;">
                        <div style="padding: 1rem; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: #1f2937; text-transform: none;">Notifications</div>
                        <div style="max-height: 300px; overflow-y: auto;">
                            {% for notif in latest_notifications %}
                                <a href="{{ notif.link|default:'#' }}" style="display: block; padding: 1rem; border-bottom: 1px solid #f3f4f6; text-decoration: none; color: {% if not notif.is_read %}#1f2937{% else %}#6b7280{% endif %}; background: {% if not notif.is_read %}#f9fafb{% else %}white{% endif %}; text-transform: none;">
                                    <div style="font-size: 0.9rem; line-height: 1.4;">{{ notif.message }}</div>
                                    <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">{{ notif.created_at|timesince }} ago</div>
                                </a>
                            {% empty %}
                                <div style="padding: 1rem; color: #6b7280; text-align: center; font-size: 0.9rem; text-transform: none;">No notifications</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
"""

js_snippet = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const notifBtn = document.getElementById('notificationBtn');
            const notifMenu = document.getElementById('notificationMenu');
            const notifBadge = document.getElementById('notifBadge');

            if(notifBtn) {
                notifBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    if(notifMenu.style.display === 'none') {
                        notifMenu.style.display = 'block';
                        // Mark as read
                        if(notifBadge) {
                            fetch('{% url "mark_notifications_read" %}', {
                                method: 'POST',
                                headers: {
                                    'X-CSRFToken': '{{ csrf_token }}',
                                    'Content-Type': 'application/json'
                                }
                            }).then(res => {
                                if(res.ok) notifBadge.style.display = 'none';
                            });
                        }
                    } else {
                        notifMenu.style.display = 'none';
                    }
                });

                document.addEventListener('click', function(e) {
                    if(!notifMenu.contains(e.target) && !notifBtn.contains(e.target)) {
                        notifMenu.style.display = 'none';
                    }
                });
            }
        });
    </script>
</body>
"""

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'class="navbar"' in content and 'notification-dropdown' not in content:
            if '<div class="container">' in content:
                content = content.replace('<div class="container">', ui_snippet + '\n        <div class="container">')
                
                if '</body>' in content:
                    content = content.replace('</body>', js_snippet)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filename}")
