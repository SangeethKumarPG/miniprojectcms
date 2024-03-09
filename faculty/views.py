from django.shortcuts import render
from .models import Faculty, Semester, Subject
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest
import pandas as pd
from student.models import StudentSemester, Course, Registration
from django.contrib import messages
import io

# Create your views here.

def get_faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request,template_name="faculty_list.html", context={"faculties":faculties})



def export_csv_template(request):
    if request.method == 'POST':
        
        course_id = request.POST.get('course')
        semester_id = request.POST.get('semester')
        faculty_id = request.POST.get('faculty')
        subject_id = request.POST.get('subject')

        
        queryset = StudentSemester.objects.all()
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if semester_id:
            queryset = queryset.filter(semester_id=semester_id)
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        
        data = {
            'Registration Id':[item.id for item in queryset],
            'Roll Number': [item.registration.roll_number for item in queryset],
            'Name': [f"{item.registration.first_name} {item.registration.last_name}" for item in queryset],
            'Internal Exam 1 Mark': [item.internal_exam1_mark for item in queryset],
            'Internal Exam 2 Mark': [item.internal_exam2_marks for item in queryset],
            'Assignment Mark': [item.assignment_mark for item in queryset],
            'Seminar Mark': [item.seminar_mark for item in queryset],
            'Total Mark': [item.total_mark for item in queryset],
        }
        df = pd.DataFrame(data)

        
        output = io.BytesIO()
        # writer = pd.ExcelWriter(output, engine='xlsxwriter')
        # df.to_excel(writer, index=False, sheet_name='Student Marks')
        # writer.save()
        # output.seek(0)
        df.to_csv(output, index=False)
        output.seek(0)


        
        # response = HttpResponse(output.read(),
        #                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename=student_marks.xlsx'
        response = HttpResponse(output, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=internal_marks.csv'
        return response

    else:
        courses = Course.objects.all()
        semesters = Semester.objects.all()
        faculties = Faculty.objects.all()
        subjects = Subject.objects.all()

        context = {
            'courses': courses,
            'semesters': semesters,
            'faculties': faculties,
            'subjects': subjects,
        }
        return render(request, 'generate_template.html', context)
    

def populate_student_semester(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        semester_id = request.POST.get('semester_id')
        faculty_id = request.POST.get('faculty_id')
        subject_id = request.POST.get('subject_id')
        uploaded_file = request.FILES.get('csv_file')
        
        if not uploaded_file:
            return HttpResponseBadRequest('No file uploaded!')
        if not uploaded_file.name.endswith('.csv'):
            return HttpResponseBadRequest('Uploaded file must be in CSV format!')
        
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            return HttpResponseBadRequest('Error reading CSV file: {}'.format(str(e)))
        
        df = df.fillna(0)
        
        for index, row in df.iterrows():
            registration_id = row['Registration Id']
            internal_exam1_mark = row.get('Internal Exam 1 Mark', 0)
            internal_exam2_marks = row.get('Internal Exam 2 Mark', 0)
            assignment_mark = row.get('Assignment Mark', 0)
            seminar_mark = row.get('Seminar Mark', 0)
            total_mark = internal_exam1_mark + internal_exam2_marks + assignment_mark + seminar_mark

            try:
                student_semester = StudentSemester.objects.get(
                    id=registration_id,
                    # semester_id=semester_id,
                    # subject_id=subject_id
                )

                # student_semester.faculty_id = faculty_id
                student_semester.internal_exam1_mark = internal_exam1_mark
                student_semester.internal_exam2_marks = internal_exam2_marks
                student_semester.assignment_mark = assignment_mark
                student_semester.seminar_mark = seminar_mark
                student_semester.total_mark = total_mark
                student_semester.save()
            except StudentSemester.DoesNotExist:
                # Handle the case when the student semester does not exist
                print("Student Does not exist")

        # return HttpResponse('Data populated successfully!')
        messages.success(request, 'Marks uploaded successfully!')
            
    
    courses = Course.objects.all()
    semesters = Semester.objects.all()
    faculties = Faculty.objects.all()
    subjects = Subject.objects.all()
    
    return render(request, 'internal_mark_bulk_upload.html', {
        'courses': courses,
        'semesters': semesters,
        'faculties': faculties,
        'subjects': subjects
    })

    # return HttpResponseBadRequest('Method not allowed')

def student_marks_detailed(request): 
    roll_number = request.GET.get('roll_number')
    if not roll_number:
        messages.error(request, "Roll number cannot be empty")
        return render(request, 'student_internal_marks_details.html')
    else:
        try:
            registration = Registration.objects.get(roll_number=roll_number)
        except Registration.DoesNotExist:
            messages.error(request, "Roll number does not exist")
            return render(request, 'student_internal_marks_details.html')
        student_marks = StudentSemester.objects.filter(registration=registration)
        return render(request, 'student_internal_marks_details.html', {'student_marks': student_marks})