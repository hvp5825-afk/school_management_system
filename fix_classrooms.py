import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Classroom, Student, Subject, Timetable, Teacher

def fix_classrooms():
    # Target Classrooms
    c10a, _ = Classroom.objects.get_or_create(standard='10', section='A')
    c10b, _ = Classroom.objects.get_or_create(standard='10', section='B')
    
    # Old/Duplicate Classrooms
    old_c10a = Classroom.objects.filter(standard='10th', section='A').first()
    old_c10b = Classroom.objects.filter(standard='10th', section='B').first()
    
    if old_c10a and old_c10a.id != c10a.id:
        print(f"Moving records from {old_c10a.standard}-{old_c10a.section} to {c10a.standard}-{c10a.section}")
        Student.objects.filter(classroom=old_c10a).update(classroom=c10a)
        Subject.objects.filter(classroom=old_c10a).update(classroom=c10a)
        Timetable.objects.filter(classroom=old_c10a).update(classroom=c10a)
        old_c10a.delete()
        print("Deleted old 10th-A")

    if old_c10b and old_c10b.id != c10b.id:
        print(f"Moving records from {old_c10b.standard}-{old_c10b.section} to {c10b.standard}-{c10b.section}")
        Student.objects.filter(classroom=old_c10b).update(classroom=c10b)
        Subject.objects.filter(classroom=old_c10b).update(classroom=c10b)
        Timetable.objects.filter(classroom=old_c10b).update(classroom=c10b)
        old_c10b.delete()
        print("Deleted old 10th-B")
        
    print("Classroom mismatch fixed. Now standardizing Timetable.")

    # Regenerate timetable strictly for c10a and c10b
    subjects_info = ['Mathematics', 'Science', 'English', 'History', 'Computer']
    subjects_10a, subjects_10b = [], []
    
    for name in subjects_info:
        code_a = f"{name[:3].upper()}10A"
        code_b = f"{name[:3].upper()}10B"
        sa, _ = Subject.objects.get_or_create(subject_code=code_a, defaults={'name': name, 'classroom': c10a})
        sb, _ = Subject.objects.get_or_create(subject_code=code_b, defaults={'name': name, 'classroom': c10b})
        subjects_10a.append(sa)
        subjects_10b.append(sb)

    teachers = list(Teacher.objects.all()[:5])
    if len(teachers) < 5:
        print("Error: Need at least 5 teachers!")
        return

    for i, t in enumerate(teachers):
        t.specialty_subject = subjects_10a[i]
        t.save()

    Timetable.objects.filter(classroom__in=[c10a, c10b]).delete()

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [1, 2, 3, 4, 5, 6, 7, 8]

    for d_idx, day in enumerate(days):
        for p_idx, period in enumerate(periods):
            t_idx_a = (d_idx + p_idx) % 5
            Timetable.objects.create(
                classroom=c10a, subject=subjects_10a[t_idx_a], teacher=teachers[t_idx_a], 
                day=day, period_number=period
            )

            t_idx_b = (d_idx + p_idx + 1) % 5
            Timetable.objects.create(
                classroom=c10b, subject=subjects_10b[t_idx_b], teacher=teachers[t_idx_b], 
                day=day, period_number=period
            )

    print("Timetable generated successfully for 10-A and 10-B!")

if __name__ == '__main__':
    fix_classrooms()
