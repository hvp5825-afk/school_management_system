import os
base_dir = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication'
for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        navbar_start = content.find('<div class="navbar"')
        container_start = content.find('<div class="container">', navbar_start)
        print(f'{filename}: navbar={navbar_start}, container={container_start}')
