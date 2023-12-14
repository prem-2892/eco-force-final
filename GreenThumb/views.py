# views.py
import io
import json
from django.core.mail import send_mail , EmailMessage
from Ecoforce.settings import EMAIL_HOST_USER
from django.http import HttpResponse, FileResponse
from django.forms import modelformset_factory
from .models import Company, Program ,Feedback
from .forms import CompanyForm , FeedbackForm
from django.shortcuts import render
from django.db.models import Q
# from .generate_PDF import generate_programs_pdf
from .models import Program
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Image, PageTemplate, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings
CompanyFormSet = modelformset_factory(Company, form=CompanyForm, extra=1)


def index(request):
    suitable_programs = []
    if request.method == 'POST':

        formset = CompanyFormSet(request.POST)
        if formset.is_valid():
            # pass
            formset.save()
            # user_email = formset.cleaned_data[0].get('contact_info')
            # if user_email:
            #     subject = 'Hello from Green Thumb '
            #     message = 'Hope you are doing well. We see you got the Suitable funding programs based on your company information. We would like to add there would be lot of funding opportunites added if ur intrested write us back and our specilists will guide you Thanks!!!'
            #     from_email = settings.EMAIL_HOST_USER  # Use the email you configured in settings.py
            #     recipient_list = [user_email]
            #
            #     send_mail(subject, message, from_email, recipient_list)

            suitable_programs = list(Program.objects.filter(
                Q(eligible_employee_count__count__contains=formset.cleaned_data[0]['employee_count']) | Q(
                    eligible_employee_count=None),
                Q(eligible_annual_electricity_budget__budget__contains=formset.cleaned_data[0][
                    'annual_electricity_budget']) | Q(eligible_annual_electricity_budget=None),
                Q(eligible_company_sector__name__contains=formset.cleaned_data[0]['company_sector']) | Q(
                    eligible_company_sector=None),
                Q(eligible_annual_natural_gas_budget__budget__contains=formset.cleaned_data[0][
                    'annual_natural_gas_budget']) | Q(eligible_annual_natural_gas_budget=None)
            ))


    else:
        formset = CompanyFormSet(queryset=Company.objects.none())

    program_ids = [program.id for program in suitable_programs]
    request.session['result_ids'] = program_ids
    return render(request, 'home.html', {'formset': formset, 'suitable_programs': suitable_programs, "form": CompanyForm,})


def as_pdf(request):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=inch, bottomMargin=inch, leftMargin=inch, rightMargin=inch)

    suitable_program_ids = request.session.get('result_ids', [])
    suitable_programs = Program.objects.filter(id__in=suitable_program_ids)

    elements = []

    # Title
    title_style = getSampleStyleSheet()['Title']
    title = Paragraph("Green Thumb - A product of E2F systems", title_style)
    elements.append(title)

    # Add a horizontal line
    line = HRFlowable(width="100%", thickness=1, spaceAfter=12, color=colors.black)
    elements.append(line)
    additional_content_style = ParagraphStyle(name='AdditionalContent', fontSize=10, textColor=colors.dimgrey,
                                              spaceAfter=12)
    additional_content = Paragraph(
        "Hello from Green Thumb. Thankyou for visitng us. There could be other incentives available for your company since funding is constantly updated. "
        "Get in touch with one of our specialists to discuss your project.\n"
        "Phone No: +1.647.704.3915\n"
        "Email : info@e2fsystems.com\n",
        additional_content_style
    )
    elements.append(additional_content)

    for program in suitable_programs:
        # Program Name as Heading
        program_name_style = ParagraphStyle(name='ProgramName', fontSize=14, textColor=colors.blue, spaceAfter=12)
        program_name = Paragraph(program.program_name, program_name_style)
        elements.append(program_name)

        # Program Variables
        bullet_points_style = getSampleStyleSheet()['Bullet']
        bullet_points = [
            Paragraph(f'<a href="{program.link}">Click here to navigate to the program</a>', bullet_points_style),
            Paragraph(f"Description: {program.description}", bullet_points_style),
            Paragraph(f"Supporting Documents : ", bullet_points_style)

        ]
        # Check if supporting_docs is a list
        # Check if supporting_docs is a list
        if isinstance(program.supporting_docs, list):
            for documnet in program.supporting_docs:
                print("Document:", documnet)
                if isinstance(documnet, dict):
                    for doc_name, doc_link in documnet.items():
                        print("Doc Name:", doc_name)
                        print("Doc Link:", doc_link)

                        bullet_points.append(
                            Paragraph(f'<a href="{doc_link}" target="_blank">{doc_name}</a>', bullet_points_style)
                        )
                else:
                    # Handle other cases or raise an error
                    pass
        else:
            # Handle other cases or raise an error
            pass

        elements.extend(bullet_points)


        # Add a page break to separate programs
        #elements.append(PageBreak())

    doc.build(elements)

    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Suitable_programs.pdf')

def all_programs(request):

    suitable_programs = Program.objects.all()
    return render(request, 'home.html',{'suitable_programs': suitable_programs })

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = FeedbackForm()



    return render(request, 'home.html', {'aform': form})