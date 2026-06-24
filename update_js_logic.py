import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_script = r'''    <script>
        // Navigate through score inputs using the Enter key
        document.addEventListener\('keydown', function\(e\) \{
            if \(e.key === 'Enter'\) \{
                // If the active element is a score input field
                if \(document.activeElement && document.activeElement.classList.contains\('score-obtained-input'\)\) \{
                    e.preventDefault\(\); // Prevent form submission
                    
                    // Get all score inputs as an array
                    var inputs = Array.from\(document.querySelectorAll\('.score-obtained-input'\)\);
                    var index = inputs.indexOf\(document.activeElement\);
                    
                    // Focus the next input if it exists
                    if \(index > -1 && index < inputs.length - 1\) \{
                        inputs\[index \+ 1\].focus\(\);
                        inputs\[index \+ 1\].select\(\);
                    \}
                \}
            \}
        \}\);
    </script>'''

new_script = '''    <script>
        // Navigate through score inputs using the Enter key (Excel-like logic)
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                if (document.activeElement && document.activeElement.classList.contains('score-input')) {
                    e.preventDefault(); // Prevent form submission
                    
                    // Determine which column we are in
                    var isObtainedScore = document.activeElement.classList.contains('score-obtained-input');
                    var selector = isObtainedScore ? '.score-obtained-input' : '.score-input:not(.score-obtained-input)';
                    
                    var inputs = Array.from(document.querySelectorAll(selector));
                    var index = inputs.indexOf(document.activeElement);
                    
                    if (index > -1 && index < inputs.length - 1) {
                        inputs[index + 1].focus();
                        inputs[index + 1].select();
                    }
                }
            }
        });
    </script>'''

content = re.sub(old_script, new_script, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated JS logic')
