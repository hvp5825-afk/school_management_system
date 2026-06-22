import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from school.models import Teacher, Subject, Classroom

User = get_user_model()

names = ["Ramesh", "Suresh", "Geeta", "Sunita", "Amit"]
subjects = [("MAT10", "Mathematics"), ("SCI10", "Science"), ("ENG10", "English"), ("HIN10", "Hindi"), ("SST10", "Social Studies")]

classroom, _ = Classroom.objects.get_or_create(standard="10th", section="A")

markdown_content = "# Seeded Teacher Credentials\n\n"
markdown_content += "| Teacher Name | Specialty Subject | Teacher ID (Username) | Password |\n"
markdown_content += "|---|---|---|---|\n"

count = 0
for i, name in enumerate(names):
    username = f"teacher_{name.lower()}{random.randint(10,99)}"
    password = "teacher123"
    
    # Ensure subject exists
    subj_code, subj_name = subjects[i]
    subject, _ = Subject.objects.get_or_create(subject_code=subj_code, defaults={'name': subj_name, 'classroom': classroom})
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=f"{username}@school.com",
            password=password,
            first_name=name,
            last_name="Sharma",
            role="teacher"
        )
        
        teacher = Teacher.objects.create(
            user=user, 
            specialty_subject=subject,
            base_salary=50000.00,
            allowances=5000.00,
            deductions=2000.00
        )
        
        markdown_content += f"| {name} Sharma | {subj_name} | **{teacher.teacher_id}** | {password} |\n"
        count += 1

artifact_path = r"C:\Users\Harsh\.gemini\antigravity-ide\brain\2fed6cc9-763f-4702-b90f-4ca919d5ab87\teacher_credentials.md"
with open(artifact_path, "w") as f:
    f.write(markdown_content)

print(f"Successfully seeded {count} teachers!")
