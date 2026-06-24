import re

path_views = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\views.py'
with open(path_views, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to completely rewrite teacher_exams to support this new flow.
# Let's extract the method and rewrite it.

match = re.search(r'def teacher_exams[\s\S]*?(?=def |$)', content)
if match:
    old_method = match.group(0)

new_method = '''def teacher_exams(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('login')

    # Only allow exams for the class they are Class Teacher of
    unique_classrooms = []
    if hasattr(teacher, 'assigned_classroom') and teacher.assigned_classroom:
        unique_classrooms = [teacher.assigned_classroom]
        
    unique_subjects = []
    if hasattr(teacher, 'assigned_classroom') and teacher.assigned_classroom:
        unique_subjects = list(Subject.objects.filter(classroom=teacher.assigned_classroom))

    selected_classroom_id = request.GET.get('classroom_id')
    selected_exam_name = request.GET.get('exam_name')
    
    # Second form params
    selected_subject_id = request.GET.get('subject_id')
    exam_date_str = request.GET.get('exam_date')
    max_score_val = request.GET.get('max_score', '100')
    export_csv = request.GET.get('export_csv')
    
    students = []
    selected_classroom = None
    selected_subject = None
    selected_exam = None
    selected_date = None

    # Step 1: Class and Exam Name selected
    if selected_classroom_id and selected_exam_name:
        try:
            selected_classroom = Classroom.objects.get(id=selected_classroom_id)
            students = list(selected_classroom.students.all())
            
            # Default to today's date
            from django.utils import timezone
            selected_date = timezone.now().date()
            
            # Step 2: If subject is also selected, create/fetch the actual Exam object
            if selected_subject_id:
                selected_subject = Subject.objects.get(id=selected_subject_id)
                
                if exam_date_str:
                    from datetime import datetime
                    try:
                        selected_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                
                max_sc = int(max_score_val) if max_score_val.isdigit() else 100
                from school.models import Exam, Mark
                selected_exam, _ = Exam.objects.get_or_create(
                    name=selected_exam_name,
                    classroom=selected_classroom,
                    subject=selected_subject,
                    defaults={'date': selected_date, 'max_score': max_sc, 'teacher': teacher}
                )
                
                # Fetch existing marks
                marks = Mark.objects.filter(student__in=students, exam=selected_exam)
                marks_dict = {m.student_id: m for m in marks}
                
                for student in students:
                    student.existing_mark = marks_dict.get(student.id)
                
                # CSV Export logic
                if export_csv == '1':
                    import csv
                    from django.http import HttpResponse
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="marks_{selected_classroom}_{selected_exam.name}_{selected_subject.name}.csv"'
                    
                    writer = csv.writer(response)
                    writer.writerow(['Student ID', 'Student Name', 'Score Obtained', 'Max Score', 'Percentage'])
                    
                    for student in students:
                        m = student.existing_mark
                        if m:
                            pct = round((m.score / m.max_score) * 100, 2) if m.max_score > 0 else 0
                            writer.writerow([student.student_id, f"{student.user.first_name} {student.user.last_name}", m.score, m.max_score, f"{pct}%"])
                        else:
                            writer.writerow([student.student_id, f"{student.user.first_name} {student.user.last_name}", 'N/A', selected_exam.max_score, 'N/A'])
                    
                    return response
                
        except (Classroom.DoesNotExist, Subject.DoesNotExist):
            pass

    if request.method == 'POST' and request.POST.get('save_marks') == '1':
        exam_id_post = request.GET.get('exam_id')
        from school.models import Exam, Mark
        try:
            selected_exam = Exam.objects.get(id=exam_id_post)
        except Exam.DoesNotExist:
            selected_exam = None
            
        if selected_exam and selected_classroom:
            has_error = False
            for student in students:
                score_val = request.POST.get(f'score_{student.id}')
                if score_val is not None and score_val != '':
                    try:
                        score = float(score_val)
                        if score > selected_exam.max_score:
                            has_error = True
                            continue
                            
                        # Update or Create
                        mark, created = Mark.objects.get_or_create(
                            student=student,
                            exam=selected_exam,
                            defaults={'score': score, 'max_score': selected_exam.max_score}
                        )
                        if not created:
                            mark.score = score
                            mark.max_score = selected_exam.max_score
                            mark.save()
                    except ValueError:
                        continue # Skip invalid numbers

            if not has_error:
                messages.success(request, f"Marks saved successfully for {selected_exam.subject.name} - {selected_exam.name}!")
            else:
                messages.warning(request, f"Some marks were saved, but some failed due to exceeding max score.")
            
            # Redirect to GET to show updated data
            return redirect(f"{request.path}?classroom_id={selected_classroom.id}&exam_name={selected_exam.name}&subject_id={selected_exam.subject.id}")

    context = {
        'unique_classrooms': unique_classrooms,
        'unique_subjects': unique_subjects,
        'selected_classroom': selected_classroom,
        'selected_exam_name': selected_exam_name,
        'selected_subject': selected_subject,
        'selected_exam': selected_exam,
        'selected_date': selected_date,
        'students': students,
    }
    return render(request, 'authentication/teacher_exams.html', context)
'''

# Avoid changing other functions, so replacing exactly the old_method with new_method
content = content.replace(old_method, new_method + '\n')

with open(path_views, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated views.py")
