import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from authentication.models import User
from school.models import Student, Teacher, Classroom, Subject

first_names = ["Amit", "Rahul", "Priya", "Sneha", "Rohan", "Neha", "Vikas", "Pooja", "Karan", "Anjali", "Suresh", "Ramesh", "Deepa", "Divya", "Kavita", "Mohit", "Nitin", "Nisha", "Sachin", "Swati", "Tarun", "Varun", "Yash", "Aarti", "Bhavna", "Chirag", "Dinesh", "Gaurav", "Harsh", "Isha"]
last_names = ["Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Joshi", "Mehta", "Chawla", "Yadav", "Rajput", "Chauhan", "Agarwal", "Bansal", "Das"]

def seed_data():
    classroom, _ = Classroom.objects.get_or_create(standard='10th', section='A')
    subject, _ = Subject.objects.get_or_create(
        subject_code='MATH101', 
        defaults={'name': 'Mathematics', 'classroom': classroom}
    )

    print("Creating 5 Teachers...")
    for i in range(5):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        username = f"tch_{fn.lower()}{random.randint(100, 999)}"
        
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password='teacher123',
            first_name=fn,
            last_name=ln,
            role='teacher'
        )
        Teacher.objects.create(
            user=user,
            specialty_subject=subject,
            base_salary=50000,
            qualification="B.Ed, M.Sc"
        )
        print(f"Created Teacher: {username} (Password: teacher123)")

    print("\nCreating 30 Students...")
    for i in range(30):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        username = f"stu_{fn.lower()}{random.randint(1000, 9999)}"
        
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password='student123',
            first_name=fn,
            last_name=ln,
            role='student'
        )
        Student.objects.create(user=user, classroom=classroom)
        
    print("\nSuccessfully seeded 5 Teachers and 30 Students! (All Student Passwords: student123)")

if __name__ == '__main__':
    seed_data()
