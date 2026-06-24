import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_exams.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = r'''            {% if selected_classroom and selected_subject and selected_exam %}
            <div style="margin-top: 2rem; display: flex; justify-content: space-between; align-items: center;">'''

new_block = '''            {% if selected_classroom and selected_subject %}
                {% if action_type == 'show' and not selected_exam %}
                    <div class="empty-state" style="margin-top: 2rem; background: #fef2f2; color: #b91c1c; border-color: #fca5a5;">
                        <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">📅</span>
                        <p>No exam was conducted on this date.</p>
                        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">Select 'Add / Edit Marks' from the Action dropdown to create it.</p>
                    </div>
                {% elif selected_exam %}
            <div style="margin-top: 2rem; display: flex; justify-content: space-between; align-items: center;">'''

content = re.sub(old_block, new_block, content)

# I also need to close the outer `{% if selected_classroom and selected_subject %}` at the end.
old_end = r'''            </form>
            {% else %}
            <div class="empty-state">
                <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">s</span>
                <p>No students found in this class.</p>
            </div>
            {% endif %}
        </div>'''

new_end = '''            </form>
            {% else %}
            <div class="empty-state">
                <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">🎓</span>
                <p>No students found in this class.</p>
            </div>
            {% endif %}
            
            {% endif %}  <!-- End of elif selected_exam -->
        {% endif %}      <!-- End of outer selected_classroom and selected_subject -->
        </div>'''

content = re.sub(old_end, new_end, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed HTML display logic')
