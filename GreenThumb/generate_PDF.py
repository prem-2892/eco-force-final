from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_programs_pdf(programs):
    doc = SimpleDocTemplate("Results_by_GreenThumb.pdf", pagesize=letter)
    story = []

    # Add a table to the PDF with program information
    data = [['Program Name', 'Link', 'Project Type', 'Supporting Docs', 'Description']]
    for program in programs:
        data.append([program.program_name, program.link, program.project_type, program.supporting_docs, program.description])

    # Create a table style
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    story.append(table)

    # Build the PDF document
    doc.build(story)
