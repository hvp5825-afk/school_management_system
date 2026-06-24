import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add action_type dropdown
old_block = r'''                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <label style="font-weight: 500; font-size: 0.95rem;">Max Score</label>
                        <input type="number" name="max_score" class="form-input" value="{{ selected_exam.max_score|default:100 }}" required style="width: 100px;">
                    </div>
                    
                    <div>
                        <button type="submit" class="btn btn-primary">Load Students</button>
                    </div>'''

new_block = '''                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <label style="font-weight: 500; font-size: 0.95rem;">Max Score</label>
                        <input type="number" name="max_score" class="form-input" value="{{ selected_exam.max_score|default:100 }}" required style="width: 100px;">
                    </div>
                    
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <label style="font-weight: 500; font-size: 0.95rem;">Action</label>
                        <select name="action_type" class="form-input" required>
                            <option value="show" {% if action_type == 'show' %}selected{% endif %}>Show Marks</option>
                            <option value="edit" {% if action_type == 'edit' %}selected{% endif %}>Add / Edit Marks</option>
                        </select>
                    </div>
                    
                    <div>
                        <button type="submit" class="btn btn-primary">Load Students</button>
                    </div>'''

if re.search(old_block, content):
    content = re.sub(old_block, new_block, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added Action Type Dropdown successfully')
else:
    print('Failed to find block to replace')
