import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def reset_passwords():
    users = User.objects.all()
    teacher_count = 0
    student_count = 0
    for user in users:
        # We don't want to reset the admin password if they made one
        if not user.is_superuser:
            role = getattr(user, 'role', None)
            if role == 'teacher':
                user.set_password("teacher123")
                user.save()
                teacher_count += 1
            elif role == 'student':
                user.set_password("student123")
                user.save()
                student_count += 1
            
    print(f"Successfully reset passwords for {teacher_count} teachers and {student_count} students!")

if __name__ == '__main__':
    reset_passwords()
