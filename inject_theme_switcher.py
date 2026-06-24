import os
import re

switcher_html = '''
    <!-- Theme Switcher -->
    <div style="position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;">
        <button onclick="cycleTheme()" class="btn btn-primary" style="border-radius: 50px; padding: 0.75rem 1.5rem; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
            <i class="fas fa-palette"></i> <span id="theme-name">Emerald Green</span>
        </button>
    </div>

    <script>
        const themes = [
            {
                name: 'Ocean Cerulean',
                primary: '#0284c7',
                primaryHover: '#0369a1',
                secondary: '#0ea5e9',
                sidebarBg: 'linear-gradient(135deg, #082f49 0%, #0369a1 100%)',
                avatarBg: 'linear-gradient(135deg, #0284c7, #38bdf8)',
                shadow: 'rgba(2, 132, 199, 0.3)'
            },
            {
                name: 'Sunset Orange',
                primary: '#ea580c',
                primaryHover: '#c2410c',
                secondary: '#f97316',
                sidebarBg: 'linear-gradient(135deg, #431407 0%, #9a3412 100%)',
                avatarBg: 'linear-gradient(135deg, #ea580c, #fb923c)',
                shadow: 'rgba(234, 88, 12, 0.3)'
            },
            {
                name: 'Royal Amethyst',
                primary: '#7c3aed',
                primaryHover: '#6d28d9',
                secondary: '#a78bfa',
                sidebarBg: 'linear-gradient(135deg, #2e1065 0%, #5b21b6 100%)',
                avatarBg: 'linear-gradient(135deg, #7c3aed, #c084fc)',
                shadow: 'rgba(124, 58, 237, 0.3)'
            },
            {
                name: 'Midnight Gold',
                primary: '#1e3a8a',
                primaryHover: '#1e40af',
                secondary: '#fbbf24',
                sidebarBg: 'linear-gradient(135deg, #020617 0%, #0f172a 100%)',
                avatarBg: 'linear-gradient(135deg, #1e3a8a, #fbbf24)',
                shadow: 'rgba(30, 58, 138, 0.3)'
            },
            {
                name: 'Emerald Green',
                primary: '#059669',
                primaryHover: '#047857',
                secondary: '#10b981',
                sidebarBg: 'linear-gradient(135deg, #064e3b 0%, #0f766e 100%)',
                avatarBg: 'linear-gradient(135deg, #059669, #34d399)',
                shadow: 'rgba(5, 150, 105, 0.3)'
            }
        ];

        let currentTheme = 4; // Start at Emerald Green

        function cycleTheme() {
            currentTheme = (currentTheme + 1) % themes.length;
            const theme = themes[currentTheme];
            
            // Set CSS Variables
            document.documentElement.style.setProperty('--primary', theme.primary);
            document.documentElement.style.setProperty('--primary-hover', theme.primaryHover);
            document.documentElement.style.setProperty('--secondary', theme.secondary);
            
            // Set Sidebar
            const sidebar = document.querySelector('.sidebar');
            if(sidebar) sidebar.style.background = theme.sidebarBg;
            
            // Set Avatars
            document.querySelectorAll('.user-avatar').forEach(el => el.style.background = theme.avatarBg);
            
            // Update Button Text
            document.getElementById('theme-name').innerText = theme.name;
            
            // Optionally, we can save it to localStorage so it persists
            localStorage.setItem('selectedTheme', currentTheme);
        }

        // Load saved theme on startup
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('selectedTheme');
            if (savedTheme !== null) {
                currentTheme = parseInt(savedTheme) - 1;
                cycleTheme();
            }
        });
    </script>
'''

base_files = [
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\admin\admin_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\student_base.html',
    r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_base.html'
]

for filepath in base_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- Theme Switcher -->' not in content:
        # insert right before </body>
        new_content = content.replace('</body>', switcher_html + '\n</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Added theme switcher to {os.path.basename(filepath)}')
