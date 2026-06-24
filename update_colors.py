import os

base_files = [
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html'
]

replacements = {
    '--primary: #4f46e5;': '--primary: #059669;',
    '--primary-hover: #4338ca;': '--primary-hover: #047857;',
    '--secondary: #10b981;': '--secondary: #0f766e;',
    'background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);': 'background: linear-gradient(135deg, #064e3b 0%, #0f766e 100%);',
    'background: linear-gradient(135deg, var(--primary), #818cf8);': 'background: linear-gradient(135deg, var(--primary), #34d399);',
    'box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);': 'box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);',
    'box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);': 'box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);',
    'box-shadow: 0 6px 15px rgba(79, 70, 229, 0.4);': 'box-shadow: 0 6px 15px rgba(5, 150, 105, 0.4);',
    'rgba(79, 70, 229, 0.1)': 'rgba(5, 150, 105, 0.1)'
}

for filepath in base_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated colors in {os.path.basename(filepath)}')
