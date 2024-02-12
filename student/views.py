
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
from django.urls import reverse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
# Create your views here.

class RegistrationCreateView(CreateView):
    model = Registration
    form_class = StudentRegistrationForm
    template_name = 'student_registration.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        pdf_filename =  f'registration_{self.object.pk}.pdf'
        pdf_content = self.generate_pdf()
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response
    
    # def generate_pdf(self):
    #     buffer = BytesIO()
    #     doc = SimpleDocTemplate(buffer, pagesize=letter)
    #     elements=[]
    #     photo_path = self.object.photo.path
    #     photo = Image(photo_path, width=1.5*inch, height=1.5*inch)
    #     photo.wrapOn(doc, 100, 700)  
    #     photo.drawOn(doc, 100, 700) 
    #     data = [
    #         ['First Name', self.object.first_name],
    #         ['Last Name', self.object.last_name],
    #         ['Course Option 1', self.object.course_option1.name],
    #         ['Course Option 2', self.object.course_option2.name],
    #         ['Admission Date', str(self.object.admission_date)],
    #         ['Date of Birth', str(self.object.date_of_birth)],
    #         ['Graduation Date', str(self.object.graduation_date)],
    #         ['Graduation Stream', self.object.graduation_stream.name],
    #         ['Graduation Percentage', str(self.object.graduation_percentage)],
    #         ['Guardian Name', self.object.guardian.name],
    #         ['Guardian Relationship', self.object.guardian.relationship],
    #         ['Guardian Contact Number', self.object.guardian.contact_number],
    #         ['Student Email', self.object.student_email],
    #     ]
    #     table = Table(data)
    #     table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    #     elements.append(table)
    #     doc.build(elements)
    #     pdf_content = buffer.getvalue()
    #     buffer.close()

    #     return pdf_content

    # def generate_pdf(self):
    #     buffer = BytesIO()
    #     c = canvas.Canvas(buffer, pagesize=letter)
    #     width, height = letter

    #     # Draw photo
    #     photo_path = self.object.photo.path
    #     photo = Image(photo_path, width=1.5*inch, height=1.5*inch)
    #     photo.drawHeight = 1.5*inch
    #     photo.drawWidth = 1.5*inch
    #     c.drawImage(photo_path, width - 150, height - 100)

    #     # Draw data table
    #     data = [
    #         ['First Name', self.object.first_name],
    #         ['Last Name', self.object.last_name],
    #         ['Course Option 1', self.object.course_option1.name],
    #         ['Course Option 2', self.object.course_option2.name],
    #         ['Admission Date', str(self.object.admission_date)],
    #         ['Date of Birth', str(self.object.date_of_birth)],
    #         ['Graduation Date', str(self.object.graduation_date)],
    #         ['Graduation Stream', self.object.graduation_stream.name],
    #         ['Graduation Percentage', str(self.object.graduation_percentage)],
    #         ['Guardian Name', self.object.guardian_name],
    #         ['Guardian Relationship', self.object.relationship_with_guardian],
    #         ['Guardian Contact Number', self.object.contact_number_of_guardian],
    #         ['Student Email', self.object.student_email],
    #     ]
    #     y = height - 120
    #     for row in data:
    #         for col in row:
    #             c.drawString(50, y, col)
    #             y -= 20
    #         y -= 10

    #     c.save()
    #     pdf_content = buffer.getvalue()
    #     buffer.close()
    #     return pdf_content

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

    def get_success_url(self):
        return None
