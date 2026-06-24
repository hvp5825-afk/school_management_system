import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from school.models import Teacher, Subject, Classroom, Timetable

print('--- Teachers ---')
for t in Teacher.objects.all():
    print(f'ID: {t.id}, Name: {t.user.first_name} {t.user.last_name}')

print('\n--- Classrooms ---')
for c in Classroom.objects.filter(standard__in=[8, 9, 10]):
    print(f'ID: {c.id}, {c.standard}-{c.section}')

print('\n--- Subjects for 8, 9, 10 ---')
for s in Subject.objects.filter(classroom__standard__in=[8, 9, 10]):
    print(f'{s.name} ({s.classroom.standard}-{s.classroom.section}) - Teacher: {s.teacher.user.first_name if s.teacher else "None"}')

print('\n--- Timetable structure ---')
print([f.name for f in Timetable._meta.get_fields()])
