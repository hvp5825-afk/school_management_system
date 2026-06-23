import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import authenticate
from authentication.models import User

identifier = 'admin'
password = 'admin123'

user = authenticate(username=identifier, password=password)
print(f'User object returned by authenticate: {user}')
if user:
    print(f'User role: {getattr(user, "role", None)}')
