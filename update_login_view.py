import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_login_block = r'''        if user is not None:
            login\(request, user\)
            role = getattr\(user, 'role', None\)
            
            if role == 'admin':
                return redirect\('admin_dashboard'\)
            elif role == 'teacher':
                return redirect\('teacher_dashboard'\)
            elif role == 'student':
                return redirect\('student_dashboard'\)
            else:
                return redirect\('login'\) # Fallback if no role is found
        else:'''

new_login_block = '''        if user is not None:
            login(request, user)
            role = getattr(user, 'role', None)
            
            # Auto-detect role from profiles if admin forgot to set the role field manually
            if not role or role not in ['admin', 'teacher', 'student']:
                if hasattr(user, 'student_profile'):
                    role = 'student'
                    user.role = 'student'
                    user.save()
                elif hasattr(user, 'teacher_profile'):
                    role = 'teacher'
                    user.role = 'teacher'
                    user.save()
                elif user.is_superuser:
                    role = 'admin'
                    user.role = 'admin'
                    user.save()
            
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            else:
                messages.error(request, "Account error: Role not assigned. Contact admin.")
                return redirect('login')
        else:'''

if re.search(old_login_block, content):
    content = re.sub(old_login_block, new_login_block, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated login view successfully!')
else:
    print('Failed to find login block')
