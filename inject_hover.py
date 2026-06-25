import os
import re

base_files = [
    r"c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html",
    r"c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html",
    r"c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html"
]

hover_css = """
        /* Enhanced Hover Effects for All Cards & Buttons */
        .card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .card:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
            border-color: rgba(2, 132, 199, 0.3) !important;
        }
        
        .btn {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
        }
        .btn:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
            filter: brightness(1.1) !important;
        }
        .btn:active {
            transform: translateY(1px) !important;
        }
"""

for filepath in base_files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already injected
        if "/* Enhanced Hover Effects" in content:
            print(f"Already injected in {filepath}")
            continue

        # Inject right before </style>
        if "</style>" in content:
            new_content = content.replace("</style>", f"{hover_css}\n    </style>")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully injected hover effects into {filepath}")
        else:
            print(f"Could not find </style> in {filepath}")
    else:
        print(f"File not found: {filepath}")
