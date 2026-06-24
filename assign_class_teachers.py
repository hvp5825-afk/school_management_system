import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Classroom, Teacher

# 1. Create 4 new classrooms
classrooms_data = [
    ('9', 'A'),
    ('9', 'B'),
    ('8', 'A'),
    ('8', 'B'),
]

new_classrooms = []
for std, sec in classrooms_data:
    c, created = Classroom.objects.get_or_create(standard=std, section=sec)
    new_classrooms.append(c)

# 2. Assign class teachers
teachers = Teacher.objects.select_related('user').all()

# Find Ramesh Sharma
ramesh = None
other_teachers = []
for t in teachers:
    if t.user.first_name.lower() == 'ramesh':
        ramesh = t
    else:
        other_teachers.append(t)

# Assign Ramesh to 10-A as Class Teacher (if possible)
class_10_a = Classroom.objects.filter(standard='10', section='A').first()
if class_10_a and ramesh:
    class_10_a.class_teacher = ramesh
    class_10_a.save()

# Assign the 4 other teachers to the 4 new classes
for i in range(min(len(other_teachers), len(new_classrooms))):
    new_classrooms[i].class_teacher = other_teachers[i]
    new_classrooms[i].save()
    print(f"Assigned {other_teachers[i].user.first_name} as main sir for {new_classrooms[i].standard}-{new_classrooms[i].section}")

print("\n--- Current Class Teachers ---")
for c in Classroom.objects.all().order_by('-standard', 'section'):
    teacher_name = c.class_teacher.user.first_name if c.class_teacher else "None"
    print(f"{c.standard}-{c.section}: Class Teacher = {teacher_name}")
