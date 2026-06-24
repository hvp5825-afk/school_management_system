import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Classroom, Subject, Timetable, Exam, Teacher

print("Starting Subject Cleanup...")

for c in Classroom.objects.all():
    subjects = Subject.objects.filter(classroom=c)
    
    # Group subjects by name
    subject_map = {}
    for s in subjects:
        name = s.name.strip().lower()
        if name not in subject_map:
            subject_map[name] = []
        subject_map[name].append(s)
        
    for name, s_list in subject_map.items():
        if len(s_list) > 1:
            print(f"Found duplicates for {name} in {c.standard}-{c.section}: {[s.id for s in s_list]}")
            
            primary_subject = s_list[0]
            duplicates = s_list[1:]
            
            for dup in duplicates:
                # Reassign Timetables
                Timetable.objects.filter(subject=dup).update(subject=primary_subject)
                # Reassign Exams
                Exam.objects.filter(subject=dup).update(subject=primary_subject)
                # Reassign Teacher specialty
                Teacher.objects.filter(specialty_subject=dup).update(specialty_subject=primary_subject)
                
                print(f"Deleted duplicate subject ID {dup.id} ({dup.name})")
                dup.delete()

print("Cleanup complete!")
