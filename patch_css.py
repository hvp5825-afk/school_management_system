import os

base_files = [
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html'
]

compat_css = """
        /* COMPATIBILITY & GLOBAL FIXES FOR ALL PAGES */
        :root {
            --text: var(--text-main);
            --text-color: var(--text-main);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .glass-card, .premium-card, .action-card {
            background: var(--surface);
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            padding: 1.5rem;
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: all 0.3s ease;
        }

        .glass-input, .premium-input {
            border: 1px solid #cbd5e1;
            padding: 0.8rem;
            border-radius: 8px;
            width: 100%;
            font-family: 'Inter', sans-serif;
            color: #334155;
            background: white;
            transition: border-color 0.2s ease;
        }

        .glass-input:focus, .premium-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.1);
        }

        .glass-btn, .premium-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
            text-decoration: none;
        }

        .glass-btn:hover, .premium-btn:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(2, 132, 199, 0.4);
        }

        .messages {
            margin-bottom: 1.5rem;
        }

        .message, .alert {
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-weight: 500;
            background: #d1fae5; 
            color: #065f46; 
            border: 1px solid #10b981;
        }
        
        .message.error, .alert.error {
            background: #fee2e2;
            color: #991b1b;
            border-color: #ef4444;
        }

        .card-header {
            margin-top: 0;
            margin-bottom: 1.5rem;
            color: #1e293b;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 0.75rem;
            font-size: 1.25rem;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #1e293b;
        }
        
        .action-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }
"""

for filepath in base_files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Avoid appending multiple times
        if "COMPATIBILITY & GLOBAL FIXES" not in content:
            # Inject right before {% block extra_css %}
            target = "{% block extra_css %}{% endblock %}"
            if target in content:
                new_content = content.replace(target, compat_css + "\n        " + target)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Patched {os.path.basename(filepath)}")
            else:
                print(f"Could not find target in {os.path.basename(filepath)}")
        else:
            print(f"Already patched {os.path.basename(filepath)}")
    else:
        print(f"File not found: {filepath}")

