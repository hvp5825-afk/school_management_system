import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def reset_passwords():
    users = User.objects.all()
    count = 0
    for user in users:
        # We don't want to reset the admin password if they made one
        if not user.is_superuser:
            user.set_password("teacher123")
            user.save()
            count += 1
            
    print(f"Successfully reset passwords to 'teacher123' for {count} users!")

if __name__ == '__main__':
    reset_passwords()
