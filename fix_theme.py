import os
import re

base_files = [
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html'
]

replacements = {
    '--primary: #059669;': '--primary: #0284c7;',
    '--primary-hover: #047857;': '--primary-hover: #0369a1;',
    '--secondary: #10b981;': '--secondary: #0ea5e9;',
    'background: linear-gradient(135deg, #064e3b 0%, #0f766e 100%);': 'background: linear-gradient(135deg, #082f49 0%, #0369a1 100%);',
    'background: linear-gradient(135deg, var(--primary), #34d399);': 'background: linear-gradient(135deg, var(--primary), #38bdf8);',
    'box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);': 'box-shadow: 0 4px 10px rgba(2, 132, 199, 0.3);',
    'box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);': 'box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);',
    'box-shadow: 0 6px 15px rgba(5, 150, 105, 0.4);': 'box-shadow: 0 6px 15px rgba(2, 132, 199, 0.4);',
    'rgba(5, 150, 105, 0.1)': 'rgba(2, 132, 199, 0.1)'
}

for filepath in base_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update colors
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # 2. Remove Theme Switcher
    # Find <!-- Theme Switcher --> and the subsequent <script>...</script> block
    pattern = r'<!-- Theme Switcher -->.*?</script>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Set Ocean Cerulean and removed switcher in {os.path.basename(filepath)}')
