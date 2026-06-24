import re

with open(r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<input type="number" name="max_score_.*?" class="(.*?)"', content)
if match:
    print('Max score classes:', match.group(1))
else:
    print('No match found')
