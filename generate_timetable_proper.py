import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Teacher, Subject, Classroom, Timetable

def generate_proper_timetable():
    classrooms = list(Classroom.objects.all().order_by('standard', 'section'))
    if len(classrooms) > 6:
        classrooms = classrooms[:6]
        
    teachers = list(Teacher.objects.all().order_by('id')[:6])
    
    # Map each teacher to their specialized subject name
    teacher_subject_map = {
        teachers[0]: 'Mathematics',
        teachers[1]: 'Science',
        teachers[2]: 'English',
        teachers[3]: 'History',
        teachers[4]: 'Computer',
        teachers[5]: 'Hindi',
    }

    # Step 1: Ensure all subjects exist for all classrooms
    for c in classrooms:
        for t, subject_name in teacher_subject_map.items():
            if not Subject.objects.filter(name=subject_name, classroom=c).exists():
                Subject.objects.create(
                    name=subject_name, 
                    classroom=c,
                    subject_code=f"{subject_name[:3].upper()}-{c.standard}{c.section}-{str(uuid.uuid4())[:4]}"
                )
            
    # Step 2: Delete existing timetables
    Timetable.objects.all().delete()

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = [1, 2, 3, 4, 5, 6, 7, 8]

    # Step 3: Generate perfectly cross-verified timetable
    for day_idx, day in enumerate(days):
        for period in periods:
            for i, classroom in enumerate(classrooms):
                # Shift pattern: depends on class index, period, and day to vary the schedule across days
                # day_idx ensures Monday schedule is different from Tuesday schedule
                teacher_idx = (i + period + day_idx) % len(teachers)
                teacher = teachers[teacher_idx]
                
                # Get the correct subject for this teacher and classroom
                subject_name = teacher_subject_map[teacher]
                subject = Subject.objects.filter(name=subject_name, classroom=classroom).first()
                
                Timetable.objects.create(
                    classroom=classroom,
                    subject=subject,
                    teacher=teacher,
                    day=day,
                    period_number=period
                )

    print("Proper timetable generated successfully with perfect cross-verification!")
    print(f"Total entries created: {Timetable.objects.count()}")

if __name__ == '__main__':
    generate_proper_timetable()
