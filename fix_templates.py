import os

base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'

for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<!-- Notifications -->' in content and '<div class="navbar' in content:
            start_idx = content.find('<!-- Notifications -->')
            if start_idx != -1:
                part1 = content[:start_idx]
                part2 = content[start_idx:]
                
                container_idx = part2.find('<div class="container">')
                if container_idx != -1:
                    notif_block = part2[:container_idx]
                    rest = part2[container_idx:]
                    
                    last_div_close = part1.rfind('</div>')
                    if last_div_close != -1:
                        # Before we move it, we should ensure the navbar has position: relative if it doesn't
                        part1 = part1.replace('<div class="navbar"', '<div class="navbar" style="position: relative;"')
                        
                        new_content = part1[:last_div_close] + notif_block + '</div>\n' + rest
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print('Fixed', filename)
