import sys

with open('authentication/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where `teacher_exams` starts
start_idx = -1
for i, line in enumerate(lines):
    if line.startswith('def teacher_exams(request):'):
        start_idx = i - 1 # Include @login_required
        break

if start_idx == -1:
    print("Could not find teacher_exams")
    sys.exit(1)

# Truncate file from start_idx
lines = lines[:start_idx]

# Now append our new code
new_code = """@login_required
def teacher_exams(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('login')

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('login')

    # Get unique classes and subjects the teacher teaches
    timetables = Timetable.objects.filter(teacher=teacher).select_related('classroom', 'subject')
    assignments = []
    seen = set()
    for t in timetables:
        key = t.classroom.id
        if key not in seen:
            seen.add(key)
            assignments.append(t)

    selected_classroom_id = request.GET.get('classroom_id')
    selected_subject_id = request.GET.get('subject_id')
    exam_id = request.GET.get('exam_id')
    exam_date_str = request.GET.get('exam_date')
    exam_name = request.GET.get('exam_name')
    max_score_val = request.GET.get('max_score', '100')
    action_type = request.GET.get('action_type', 'show')
    export_csv = request.GET.get('export_csv')
    
    students = []
    selected_classroom = None
    selected_subject = None
    selected_exam = None
    selected_date = None
    available_exams = []

    if selected_classroom_id and selected_subject_id:
        try:
            selected_classroom = Classroom.objects.get(id=selected_classroom_id)
            selected_subject = Subject.objects.get(id=selected_subject_id)
            students = list(selected_classroom.students.all())
            
            # Get existing exams for this class & subject
            from school.models import Exam, Mark
            available_exams = Exam.objects.filter(classroom=selected_classroom, subject=selected_subject).order_by('-date')
            
            # Determine the current exam
            if exam_name and exam_date_str:
                from datetime import datetime
                from django.utils import timezone
                try:
                    selected_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                except ValueError:
                    selected_date = timezone.now().date()
                
                max_sc = int(max_score_val) if max_score_val.isdigit() else 100
                selected_exam, _ = Exam.objects.get_or_create(
                    name=exam_name,
                    classroom=selected_classroom,
                    subject=selected_subject,
                    defaults={'date': selected_date, 'max_score': max_sc, 'teacher': teacher}
                )
            elif exam_id:
                selected_exam = Exam.objects.filter(id=exam_id).first()
                if selected_exam:
                    selected_date = selected_exam.date

            # Fetch existing marks if an exam is selected
            if selected_exam:
                marks = Mark.objects.filter(student__in=students, exam=selected_exam)
                marks_dict = {m.student_id: m for m in marks}
                
                for student in students:
                    student.existing_mark = marks_dict.get(student.id)
                
                # CSV Export logic
                if export_csv == '1':
                    import csv
                    from django.http import HttpResponse
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="marks_{selected_classroom}_{selected_exam.name}.csv"'
                    
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
            
        if selected_exam and selected_classroom and selected_subject:
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
                messages.success(request, f"Marks saved successfully for {selected_classroom} - {selected_exam.name}!")
            else:
                messages.warning(request, f"Some marks were saved, but some failed due to exceeding max score.")
            return redirect(f"{request.path}?classroom_id={selected_classroom.id}&subject_id={selected_subject.id}&exam_id={selected_exam.id}&action_type=show")

    context = {
        'assignments': assignments,
        'selected_classroom': selected_classroom,
        'selected_subject': selected_subject,
        'selected_exam': selected_exam,
        'selected_date': selected_date,
        'available_exams': available_exams,
        'students': students,
        'action_type': action_type,
    }
    return render(request, 'authentication/teacher_exams.html', context)

@login_required
def teacher_announcements(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('login')

    from school.models import Announcement

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if title and content:
            Announcement.objects.create(
                teacher=teacher,
                title=title,
                content=content,
                category=category,
                image=image
            )
            messages.success(request, 'Announcement posted successfully!')
            return redirect('teacher_announcements')

    announcements = Announcement.objects.filter(teacher=teacher).order_by('-date_posted')
    return render(request, 'authentication/teacher_announcements.html', {'announcements': announcements})
"""

with open('authentication/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
    f.write(new_code)
print("Done!")
