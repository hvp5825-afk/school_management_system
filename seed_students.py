import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from authentication.models import User
from school.models import Classroom, Student

def seed_students_for_classes():
    targets = [
        {'standard': 8, 'section': 'B'},
        {'standard': 9, 'section': 'A'},
        {'standard': 9, 'section': 'B'}
    ]

    first_names = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Ayaan', 'Krishna', 'Ishaan', 'Shaurya', 'Ananya', 'Diya', 'Aadhya', 'Pari', 'Saanvi']
    last_names = ['Sharma', 'Verma', 'Gupta', 'Kumar', 'Singh', 'Patel', 'Joshi', 'Mehta', 'Nair', 'Das', 'Reddy', 'Chauhan', 'Yadav']

    for target in targets:
        std = target['standard']
        sec = target['section']
        class_name = f"{std}{sec}"
        
        try:
            classroom = Classroom.objects.get(standard=std, section=sec)
            print(f"\\nSeeding students for {std}-{sec}...")
        except Classroom.DoesNotExist:
            print(f"\\nClassroom {std}-{sec} not found. Skipping.")
            continue

        for i in range(10):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            username = f"stu_{class_name.lower()}_{i}_{random.randint(1000, 9999)}"
            email = f"{username}@example.com"

            user = User.objects.create_user(
                username=username,
                password='password123',
                first_name=fname,
                last_name=lname,
                email=email
            )
            user.role = 'student'
            user.save()

            student = Student.objects.create(
                user=user,
                student_id=f"{class_name}-{1000+i}",
                classroom=classroom
            )
            print(f"  Added: {student.user.first_name} {student.user.last_name} (ID: {student.student_id})")

if __name__ == '__main__':
    seed_students_for_classes()
