import os

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

ui_snippet = """
            <!-- Notifications -->
            <div style="position: absolute; right: 2rem; top: 50%; transform: translateY(-50%); display: flex; align-items: center; z-index: 100;">
                <div class="notification-dropdown" style="position: relative;">
                    <button id="notificationBtn" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text); position: relative; padding: 0.5rem; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-bell"></i>
                        {% if unread_notifications_count > 0 %}
                            <span id="notifBadge" style="position: absolute; top: 0px; right: 0px; background: #ef4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; font-weight: bold; border: 2px solid white; display: flex; align-items: center; justify-content: center; min-width: 15px; height: 15px;">
                                {{ unread_notifications_count }}
                            </span>
                        {% endif %}
                    </button>
                    <div id="notificationMenu" style="display: none; position: absolute; right: 0; top: 50px; background: white; border: 1px solid #e5e7eb; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1); border-radius: 12px; width: 320px; z-index: 1000; text-align: left; overflow: hidden;">
                        <div style="padding: 1rem 1.25rem; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: #111827; background: #f9fafb; font-size: 1rem; text-transform: none;">Notifications</div>
                        <div style="max-height: 350px; overflow-y: auto;">
                            {% for notif in latest_notifications %}
                                <a href="{{ notif.link|default:'#' }}" style="display: block; padding: 1rem 1.25rem; border-bottom: 1px solid #f3f4f6; text-decoration: none; color: {% if not notif.is_read %}#111827{% else %}#6b7280{% endif %}; background: {% if not notif.is_read %}#f0fdf4{% else %}white{% endif %}; text-transform: none; transition: background 0.2s;">
                                    <div style="font-size: 0.9rem; line-height: 1.4; font-weight: {% if not notif.is_read %}500{% else %}400{% endif %};">{{ notif.message }}</div>
                                    <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.35rem; display: flex; align-items: center; gap: 0.25rem;"><i class="far fa-clock"></i> {{ notif.created_at|timesince }} ago</div>
                                </a>
                            {% empty %}
                                <div style="padding: 2rem 1rem; color: #6b7280; text-align: center; font-size: 0.95rem; text-transform: none; display: flex; flex-direction: column; align-items: center; gap: 0.5rem;">
                                    <i class="far fa-bell-slash" style="font-size: 2rem; color: #d1d5db;"></i>
                                    You have no notifications
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
"""

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Strip old notification block if it exists
        start_idx = content.find('<!-- Notifications -->')
        if start_idx != -1:
            end_idx = content.find('</div>', content.find('notification-dropdown', start_idx))
            # Actually, to remove the whole block properly we can use regex or just replace the known old block.
            # But the old block is dynamically formatted.
            # Let's just find the exact text from <!-- Notifications --> up to its enclosing div closure.
            pass # Easier to just replace the broken part

        # A cleaner way is to reconstruct the navbar for all templates:
        import re
        # Find the navbar opening tag
        navbar_match = re.search(r'<div class="navbar"[^>]*>', content)
        if navbar_match:
            # We want to make sure navbar has position:relative
            navbar_tag = navbar_match.group(0)
            new_navbar_tag = navbar_tag
            
            # Remove any injected style="position: relative;" to clean up duplicates
            new_navbar_tag = new_navbar_tag.replace(' style="position: relative;"', '')
            
            # Combine styles if there's already a style attribute
            if 'style="' in new_navbar_tag:
                new_navbar_tag = new_navbar_tag.replace('style="', 'style="position: relative; ')
            else:
                new_navbar_tag = new_navbar_tag[:-1] + ' style="position: relative;">'

            content = content.replace(navbar_tag, new_navbar_tag, 1)

        # Remove the old buggy <!-- Notifications --> block
        # We know it starts with <!-- Notifications --> and ends just before <div class="container">
        # Or before </div>\n        <div class="container">
        # Let's find <!-- Notifications -->
        notif_start = content.find('<!-- Notifications -->')
        if notif_start != -1:
            # Look for the closing div of the old notification block
            # Since it's a mess, we'll extract the clean part of the file.
            # Before notif_start, there might be a missing </div>
            pre_notif = content[:notif_start]
            
            # Find where container starts
            container_start = content.find('<div class="container">', notif_start)
            
            if container_start != -1:
                # Reconstruct properly: pre_notif + </div> (if needed) + ui_snippet + container
                # Let's check if pre_notif is missing a </div> for the title
                if pre_notif.endswith('Panel'):
                    pre_notif += '\n            </div>\n'
                
                # We want ui_snippet to be INSIDE the navbar, right before its closing </div>
                # The navbar structure usually is:
                # <div class="navbar">
                #    <div title>Welcome</div>
                # </div>
                # <div class="container">
                
                # So the navbar's closing </div> should be right before container.
                # Let's find the closing </div> of the navbar. It's usually the </div> before <div class="container">
                content_without_notif = pre_notif + content[container_start:]
                
                # Now inject ui_snippet into content_without_notif, right before container_start, but INSIDE navbar.
                # Actually, the easiest way to guarantee it's inside the navbar and looks good is to append it inside the navbar div.
                # We can do this by finding the </div> that precedes <div class="container">
                
                c_start = content_without_notif.find('<div class="container">')
                last_div_close = content_without_notif.rfind('</div>', 0, c_start)
                
                final_content = content_without_notif[:last_div_close] + ui_snippet + '\n        </div>\n' + content_without_notif[c_start:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                print('Fixed', filename)
