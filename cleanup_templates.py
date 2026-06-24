import os

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        start_idx = content.find('<!-- Notifications -->')
        if start_idx != -1:
            end_idx = content.find('</div>', content.find('notification-dropdown', start_idx))
            if end_idx != -1:
                # We need to find the correct ending </div> of the outermost injected div
                # The outermost div was: <div style="position: absolute; right: 2rem; ... z-index: 100;">
                # Since it has nested divs, a simple find('</div>') is not enough.
                # Let's use a simple approach: find <!-- Notifications --> and just remove everything between it and the closing </div> before <div class="container">
                # Or simply replace the exact snippet string we injected!
                pass

        # Since we injected `ui_snippet` exactly, let's just find and replace it if possible.
        # However, the exact string might be hard. Let's use string operations:
        s1 = '<!-- Notifications -->'
        s2 = '\n        </div>\n        <div class="container">'
        
        if s1 in content:
            idx1 = content.find(s1)
            # Find the next container
            idx2 = content.find('<div class="container">', idx1)
            
            if idx2 != -1:
                # The stuff to remove is from idx1 to idx2
                # But wait, there is a </div> that closes the navbar right before container?
                # We previously injected: final_content = content_without_notif[:last_div_close] + ui_snippet + '\n        </div>\n' + content_without_notif[c_start:]
                
                # Let's carefully remove the notification block
                # The notification block ends with a specific </div>
                
                new_content = content[:idx1].rstrip() + '\n        </div>\n        <div class="container">' + content[idx2+len('<div class="container">'):]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print('Cleaned', filename)
