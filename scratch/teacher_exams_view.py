
@login_required
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
        key = (t.classroom.id, t.subject.id)
        if key not in seen:
            seen.add(key)
            assignments.append({
                'classroom': t.classroom,
                'subject': t.subject
            })

    selected_classroom_id = request.GET.get('classroom_id')
    selected_subject_id = request.GET.get('subject_id')
    
    students = []
    selected_classroom = None
    selected_subject = None

    if selected_classroom_id and selected_subject_id:
        try:
            selected_classroom = Classroom.objects.get(id=selected_classroom_id)
            selected_subject = Subject.objects.get(id=selected_subject_id)
            students = list(selected_classroom.students.all())
            
            # Fetch existing marks
            marks = Mark.objects.filter(student__in=students, subject=selected_subject)
            marks_dict = {m.student_id: m for m in marks}
            
            for student in students:
                student.existing_mark = marks_dict.get(student.id)
                
        except (Classroom.DoesNotExist, Subject.DoesNotExist):
            pass

    if request.method == 'POST' and selected_classroom and selected_subject:
        for student in students:
            score_val = request.POST.get(f'score_{student.id}')
            max_score_val = request.POST.get(f'max_score_{student.id}')
            
            if score_val is not None and max_score_val is not None and score_val != '':
                try:
                    score = float(score_val)
                    max_score = int(max_score_val)
                    
                    # Update or Create
                    mark, created = Mark.objects.get_or_create(
                        student=student,
                        subject=selected_subject,
                        defaults={'score': score, 'max_score': max_score}
                    )
                    if not created:
                        mark.score = score
                        mark.max_score = max_score
                        mark.save()
                except ValueError:
                    continue # Skip invalid numbers

        messages.success(request, f"Marks saved successfully for {selected_classroom} - {selected_subject.name}!")
        return redirect(f"{request.path}?classroom_id={selected_classroom.id}&subject_id={selected_subject.id}")

    context = {
        'assignments': assignments,
        'selected_classroom': selected_classroom,
        'selected_subject': selected_subject,
        'students': students,
    }
    return render(request, 'authentication/teacher_exams.html', context)
