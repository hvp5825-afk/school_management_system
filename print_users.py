import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from authentication.models import User
users = User.objects.all()
for u in users:
    print(f'User: {u.username}, Email: {u.email}, Role: {getattr(u, "role", None)}, is_superuser: {u.is_superuser}')
