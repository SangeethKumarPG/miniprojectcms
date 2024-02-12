
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from .models import Registration
from .forms import StudentRegistrationForm
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from django.urls import reverse_lazy
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from django.http import JsonResponse
from .models import Course, FeeStructure
from instamojo_wrapper import Instamojo
from cms.settings import INSTA_MOJO_API_KEY,INSTA_MOJO_AUTH_TOKEN,INSTA_MOJO_SALT
from django.utils import timezone
from django.contrib import messages
# Create your views here.

class RegistrationCreateView(CreateView):
    model = Registration
    form_class = StudentRegistrationForm
    template_name = 'student_registration.html'
    success_url = reverse_lazy("registration_form")
    def form_valid(self, form):
        response = super().form_valid(form)
        pdf_filename =  f'registration_{self.object.pk}.pdf'
        pdf_content = self.generate_pdf()
        messages.success(self.request, "Form Submitted Successfully!")
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response
    
    
    def generate_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = {
            'Normal': ParagraphStyle(
                'Normal',
                fontSize=12,
                leading=14,
            ),
            'Heading1': ParagraphStyle(
                'Heading1',
                fontSize=14,
                leading=16,
                textColor=colors.blue,
            ),
        }
        try:
            photo_path = self.object.photo.path
            photo = Image(photo_path, width=1.5*inch, height=1.5*inch)
            elements.append(photo)
            elements.append(Spacer(1, 0.5*inch))

        except Exception as e:
            elements.append(Paragraph(f"Error: {e}", styles['Normal']))

        data = [
            ['Field', 'Value'],
            ['First Name', self.object.first_name],
            ['Last Name', self.object.last_name],
            ['Course Option 1', self.object.course_option1.name],
            ['Course Option 2', self.object.course_option2.name],
            ['Admission Date', str(self.object.admission_date)],
            ['Date of Birth', str(self.object.date_of_birth)],
            ['Graduation Date', str(self.object.graduation_date)],
            ['Graduation Stream', self.object.graduation_stream.name],
            ['Graduation Percentage', str(self.object.graduation_percentage)],
            ['Guardian Name', self.object.guardian_name],
            ['Guardian Relationship', self.object.relationship_with_guardian],
            ['Guardian Contact Number', self.object.contact_number_of_guardian],
            ['Student Email', self.object.student_email],
        ]
        table = Table(data, colWidths=[1.5*inch, 3*inch])
        # table = Table(data, colWidths=[3*inch, 6*inch])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)

        try:
            doc.build(elements)
            pdf_content = buffer.getvalue()
            buffer.close()
            return pdf_content

        except Exception as e:
            return f"Error generating PDF: {e}"

    # def get_success_url(self):
    #     return reverse_lazy('registration_form')
    

def fetch_fee_detail(request):
    if request.method=='GET':

        student = Registration.objects.get(roll_number = request.GET['rollno'])
        if student != None:
            if student.selected_course.name.lower() == request.GET['course'].lower():             
                fees_data = student.selected_course.fee_structure
                if student.first_semester_fee_paid == None and student.second_semester_fee_paid == None and student.third_semester_fee_paid == None and student.fourth_semester_fee_paid == None:
                    data ={
                        '1stsem' : str(fees_data.first_semester) + ','+ 'FirstSemester',
                        '2stsem' : str(fees_data.second_semester)+ ',' + 'SecondSemester',
                        '3stsem' : str(fees_data.third_semester)+ ',' + 'ThirdSemester',
                        '4thsem' : str(fees_data.fourth_semester)+ ',' + 'FourthSemester',
                    }
                elif student.second_semester_fee_paid == None:
                    data ={
                        '2stsem' : str(fees_data.second_semester)+ ',' + 'SecondSemester',
                        '3stsem' : str(fees_data.third_semester)+ ',' + 'ThirdSemester',
                        '4thsem' : str(fees_data.fourth_semester)+ ',' + 'FourthSemester',
                    }
                elif student.third_semester_fee_paid == None:
                    data ={
                        '3stsem' : str(fees_data.third_semester)+ ',' + 'ThirdSemester',
                        '4thsem' : str(fees_data.fourth_semester)+ ',' + 'FourthSemester',
                    } 
                elif student.fourth_semester_fee_paid == None:
                    data ={
                        '4thsem' : str(fees_data.fourth_semester)+ ',' + 'FourthSemester',
                    }
                else:
                    data = {
                        "NA":"No Fees Pending"
                    }                              
                print(data)
                return JsonResponse(data)
            else:
                return JsonResponse({"error" : "invalid course"})
        else:
            return JsonResponse({"error" : "invalid Roll number"})

def payment_success(request):
    return render(request,"payment_success.html")  

def fee_payment(request):
    if request.method == "POST":
       rollno = request.POST.get("rollno")
       email = request.POST.get("email")
       fees_data = request.POST.get("semester")
       fees = fees_data.split(',')[0]
       purpose = fees_data.split(',')[1]
       purpose+=','+rollno
       print(fees)
       api = Instamojo(api_key = INSTA_MOJO_API_KEY, auth_token = INSTA_MOJO_AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
       response = api.payment_request_create(
           amount=fees,
           purpose=purpose,
           send_email = True,
           email = email,
           redirect_url = "http://127.0.0.1:8000/student/paymentsuccess/"
       )
        
       print(response.get('payment_request').get('id'))
       return render(request,"payment_link_generated.html",{
           'url' :response.get('payment_request').get('longurl'),
           'id' : response.get('payment_request').get('id') 
       })
    else:
        return render(request,'fee_payment.html')
    

def save_fee_details(student,response,semester):
    if response.get('success') == True and response.get('payment_request').get('status') == 'Completed':
        if semester == "FirstSemester" and student.first_semester_fee_paid == None:
            student.first_semester_fee_paid = timezone.now()
            student.save()
        elif semester == "SecondSemester" and student.second_semester_fee_paid == None:
            student.second_semester_fee_paid = timezone.now()
            student.save()
        elif semester == "ThirdSemester" and student.third_semester_fee_paid == None:
            student.third_semester_fee_paid = timezone.now()
            student.save()
        elif semester == "FourthSemester" and student.fourth_semester_fee_paid == None:
            student.fourth_semester_fee_paid = timezone.now()
            student.save()

def is_fee_paid(request):
    if request.method == "GET":
        payment_id = request.GET['payment_id']
        payment_request_id = request.GET['payment_request_id']
        api = Instamojo(api_key=INSTA_MOJO_API_KEY, auth_token=INSTA_MOJO_AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
        response = api.payment_request_payment_status(payment_request_id,payment_id)
        roll_no = response.get('payment_request').get('purpose').split(',')[1]
        print(response)
        print(response.get('success') == True)
        semester = response.get('payment_request').get('purpose').split(',')[0]
        student = Registration.objects.get(roll_number=roll_no)
        if student != None and student.selected_course != None:
            save_fee_details(student=student, response=response,semester=semester)
        return JsonResponse(response)