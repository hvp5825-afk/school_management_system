import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from school.models import Student, Classroom

User = get_user_model()

names = [
    "Aarav", "Vihaan", "Vivaan", "Ananya", "Diya", "Aditya", "Sai", "Arjun", "Ishaan", "Riya",
    "Aadhya", "Krishna", "Dhruv", "Aarohi", "Anvi", "Kabir", "Shaurya", "Atharv", "Prisha", "Avni",
    "Rudra", "Myra", "Kian", "Reyansh", "Anika", "Saanvi", "Ayaansh", "Navya", "Tara", "Zara"
]

classroom, _ = Classroom.objects.get_or_create(standard="10th", section="A")

markdown_content = "# Seeded Student Credentials\n\n"
markdown_content += "| Student Name | Student ID (Username) | Password |\n"
markdown_content += "|---|---|---|\n"

count = 0
for i, name in enumerate(names):
    username = f"{name.lower()}{random.randint(100,999)}"
    password = "student123"
    
    # Check if exists to avoid errors on rerun
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=f"{username}@school.com",
            password=password,
            first_name=name,
            last_name="Kumar",
            role="student"
        )
        
        student = Student.objects.create(user=user, classroom=classroom)
        
        markdown_content += f"| {name} Kumar | **{student.student_id}** | {password} |\n"
        count += 1

# Save to an artifact file
artifact_path = r"C:\Users\Harsh\.gemini\antigravity-ide\brain\2fed6cc9-763f-4702-b90f-4ca919d5ab87\student_credentials.md"
with open(artifact_path, "w") as f:
    f.write(markdown_content)

print(f"Successfully seeded {count} students!")
