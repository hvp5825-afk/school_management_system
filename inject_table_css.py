import os

table_css = '''
        /* Table Styles */
        .table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            text-align: left;
            margin-top: 1rem;
        }

        .table th {
            padding: 1rem 1.5rem;
            background: #f8fafc;
            color: #475569;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e2e8f0;
            border-top: 1px solid #e2e8f0;
        }

        .table th:first-child {
            border-top-left-radius: 8px;
            border-left: 1px solid #e2e8f0;
        }

        .table th:last-child {
            border-top-right-radius: 8px;
            border-right: 1px solid #e2e8f0;
        }

        .table td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #e2e8f0;
            color: #334155;
            vertical-align: middle;
        }
        
        .table td:first-child {
            border-left: 1px solid #e2e8f0;
        }
        
        .table td:last-child {
            border-right: 1px solid #e2e8f0;
        }

        .table tbody tr {
            transition: all 0.2s ease;
            background: white;
        }

        .table tbody tr:hover {
            background: #f1f5f9;
        }

        .table tbody tr:last-child td:first-child {
            border-bottom-left-radius: 8px;
        }

        .table tbody tr:last-child td:last-child {
            border-bottom-right-radius: 8px;
        }

        /* Forms inside table */
        .form-control {
            border: 1px solid #cbd5e1;
            padding: 0.5rem;
            border-radius: 6px;
            width: 100%;
            font-family: 'Inter', sans-serif;
            color: #334155;
            transition: border-color 0.2s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
'''

base_files = [
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html'
]

for filepath in base_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Insert table_css before {% block extra_css %}
    if '/* Table Styles */' not in content:
        content = content.replace('{% block extra_css %}', table_css + '\n        {% block extra_css %}')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Added table styles to {os.path.basename(filepath)}')
