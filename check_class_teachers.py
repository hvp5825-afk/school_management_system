import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Classroom, Teacher

for c in Classroom.objects.all():
    teacher_name = c.class_teacher.user.first_name if c.class_teacher else "None"
    print(f"{c.standard}-{c.section}: Class Teacher = {teacher_name}")
