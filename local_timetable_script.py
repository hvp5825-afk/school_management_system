import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Teacher, Classroom, Subject, Timetable

def generate_timetable():
    # Classes
    c10a, _ = Classroom.objects.get_or_create(standard='10th', section='A')
    c10b, _ = Classroom.objects.get_or_create(standard='10th', section='B')
    
    # Subjects
    subjects_info = ['Mathematics', 'Science', 'English', 'History', 'Computer']
    subjects_10a, subjects_10b = [], []
    
    for name in subjects_info:
        code_a = f"{name[:3].upper()}10A"
        code_b = f"{name[:3].upper()}10B"
        sa, _ = Subject.objects.get_or_create(subject_code=code_a, defaults={'name': name, 'classroom': c10a})
        sb, _ = Subject.objects.get_or_create(subject_code=code_b, defaults={'name': name, 'classroom': c10b})
        subjects_10a.append(sa)
        subjects_10b.append(sb)

    # Get 5 Teachers
    teachers = list(Teacher.objects.all()[:5])
    if len(teachers) < 5:
        print("Error: Need at least 5 teachers locally!")
        return

    # Update their specialities
    for i, t in enumerate(teachers):
        t.specialty_subject = subjects_10a[i]
        t.save()

    # Clear old timetables
    Timetable.objects.filter(classroom__in=[c10a, c10b]).delete()

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [1, 2, 3, 4, 5, 6, 7, 8]

    print("Generating perfect non-conflicting Monday to Saturday (8 periods) timetable locally...")

    for d_idx, day in enumerate(days):
        for p_idx, period in enumerate(periods):
            # 10-A ke liye
            t_idx_a = (d_idx + p_idx) % 5
            Timetable.objects.create(
                classroom=c10a, subject=subjects_10a[t_idx_a], teacher=teachers[t_idx_a], 
                day=day, period_number=period
            )

            # 10-B ke liye (1 index shift kar diya taki same time pe 2 class me na jaye)
            t_idx_b = (d_idx + p_idx + 1) % 5
            Timetable.objects.create(
                classroom=c10b, subject=subjects_10b[t_idx_b], teacher=teachers[t_idx_b], 
                day=day, period_number=period
            )

    print("Timetable successfully generated for 8 Lectures across Monday to Saturday without any overlaps!")

if __name__ == '__main__':
    generate_timetable()
