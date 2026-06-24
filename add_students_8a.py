import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from authentication.models import User
from school.models import Classroom, Student

def add_students():
    try:
        classroom = Classroom.objects.get(standard=8, section='A')
    except Classroom.DoesNotExist:
        print("Classroom 8-A not found.")
        return

    first_names = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Ayaan', 'Krishna', 'Ishaan', 'Shaurya']
    last_names = ['Sharma', 'Verma', 'Gupta', 'Kumar', 'Singh', 'Patel', 'Joshi', 'Mehta', 'Nair', 'Das']

    for i in range(10):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        username = f"stu_8a_{i}_{random.randint(1000, 9999)}"
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
            student_id=f"8A-{1000+i}",
            classroom=classroom
        )
        print(f"Added student: {student.user.first_name} {student.user.last_name} (ID: {student.student_id})")

if __name__ == '__main__':
    add_students()
