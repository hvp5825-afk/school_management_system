import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from authentication.models import User
from school.models import Teacher, Classroom, Subject

# 1. Check if we have a Geography subject or pick one
subject, created = Subject.objects.get_or_create(name='Geography', defaults={'description': 'Study of places and relationships'})

# 2. Create the User for the new teacher
username = 'neha_verma'
user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'first_name': 'Neha',
        'last_name': 'Verma',
        'email': 'neha.verma@example.com',
        'role': 'teacher'
    }
)

if created:
    user.set_password('teacher123')
    user.save()

# 3. Create the Teacher Profile
teacher, t_created = Teacher.objects.get_or_create(
    user=user,
    defaults={
        'specialty_subject': subject,
        'base_salary': 45000.00,
        'allowances': 5000.00
    }
)
# Make sure the teacher has an ID
if t_created or not teacher.teacher_id:
    teacher.save() # The custom save method in Teacher model will generate a teacher_id

# 4. Assign to Class 10-B
class_10_b = Classroom.objects.filter(standard='10', section='B').first()
if class_10_b:
    class_10_b.class_teacher = teacher
    class_10_b.save()
    print(f"Success! {user.first_name} {user.last_name} (ID: {teacher.teacher_id}) was added and assigned as the Class Teacher for 10-B.")
else:
    print("Class 10-B not found!")
