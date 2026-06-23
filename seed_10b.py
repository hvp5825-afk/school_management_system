import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from school.models import Classroom, Student, Teacher, Subject, Timetable
from django.contrib.auth.hashers import make_password

User = get_user_model()

def seed_10b():
    classroom_b, _ = Classroom.objects.get_or_create(standard='10', section='B')
    teacher = Teacher.objects.filter(teacher_id='TCH-AMIT396').first()
    subject = Subject.objects.first()
    
    if not teacher:
        print("Teacher AMIT not found.")
        return

    print(f'Assigning {teacher.user.first_name} to {classroom_b} for {subject.name}')
    Timetable.objects.get_or_create(
        teacher=teacher, 
        classroom=classroom_b, 
        subject=subject,
        day='Tuesday',
        period_number=2
    )
    
    print('Generating 30 students for 10-B...')
    start_id = Student.objects.count() + 1
    
    for i in range(1, 31):
        uid = str(start_id + i).zfill(3)
        username = f'student_10b_{uid}'
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'password': make_password('student123'),
                'role': 'student',
                'first_name': 'Student',
                'last_name': f'10B_{i}'
            }
        )
        Student.objects.get_or_create(
            user=user,
            defaults={
                'student_id': f'STU-10B-{uid}',
                'classroom': classroom_b
            }
        )
    print('Successfully created 30 students for 10-B and assigned Amit to 10-B!')

if __name__ == '__main__':
    seed_10b()
