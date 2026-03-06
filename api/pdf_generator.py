from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def generate_pdf(file_path, draft_text, score, risk):

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>AI Compliance Proposal</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Compliance Score: {score}%", styles["Normal"]))
    elements.append(Paragraph(f"Risk Level: {risk}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(draft_text.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(elements)