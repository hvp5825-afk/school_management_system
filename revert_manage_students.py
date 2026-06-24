import re

# 1. Revert views.py
path_views = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(path_views, 'r', encoding='utf-8') as f:
    views_content = f.read()

old_complex_view = r'@login_required\s*\n\s*def teacher_manage_students\(request\):[\s\S]*?return render\(request, \'authentication/teacher_manage_students\.html\', \{\s*\'students\': students,\s*\'classrooms\': classrooms,\s*\'search_query\': search_query,\s*\'selected_classroom\': classroom_id\s*\}\)'

new_simple_view = '''@login_required
def teacher_manage_students(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')
    return render(request, 'authentication/teacher_manage_students.html')'''

if re.search(old_complex_view, views_content):
    views_content = re.sub(old_complex_view, new_simple_view, views_content)
    with open(path_views, 'w', encoding='utf-8') as f:
        f.write(views_content)
    print('Reverted views.py')

# 2. Revert teacher_manage_students.html
path_html = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\teacher_manage_students.html'
with open(path_html, 'r', encoding='utf-8') as f:
    html_content = f.read()

new_html_content = '''
        <div class="container">
            <div style="text-align: center; margin-bottom: 3rem;">
                <h1 style="color: var(--text); font-size: 2.2rem; margin-bottom: 0.5rem;">What would you like to do?</h1>
                <p style="color: #6b7280; font-size: 1.1rem;">Select an action below to manage student records in the system.</p>
            </div>
            
            <div class="action-cards" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
                <a href="{% url 'teacher_add_student' %}" class="action-card" style="background: var(--surface); border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 3rem 2rem; text-align: center; text-decoration: none; color: var(--text); border: 2px solid transparent; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: transform 0.2s, box-shadow 0.2s;">
                    <i class="fas fa-user-plus" style="font-size: 3.5rem; margin-bottom: 1.5rem; color: var(--primary);"></i>
                    <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Add Student</div>
                    <div style="color: #6b7280; font-size: 1rem; line-height: 1.5;">Register a new student, assign them to a classroom, and generate their login credentials.</div>
                </a>
                
                <a href="{% url 'teacher_remove_student' %}" class="action-card" style="background: var(--surface); border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 3rem 2rem; text-align: center; text-decoration: none; color: var(--text); border: 2px solid transparent; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: transform 0.2s, box-shadow 0.2s;">
                    <i class="fas fa-user-minus" style="font-size: 3.5rem; margin-bottom: 1.5rem; color: #ef4444;"></i>
                    <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Remove Student</div>
                    <div style="color: #6b7280; font-size: 1rem; line-height: 1.5;">Search for an existing student and permanently cancel their admission.</div>
                </a>
            </div>
        </div>
'''

html_content = re.sub(r'<div class="container">.*</div>', new_html_content, html_content, flags=re.DOTALL)

with open(path_html, 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Reverted teacher_manage_students.html')
