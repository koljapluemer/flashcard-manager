from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
import re


def clean_html(html_text):
    """Remove HTML tags for PDF generation"""
    clean_text = re.sub('<[^<]+?>', '', html_text)
    clean_text = clean_text.replace('&nbsp;', ' ')
    clean_text = clean_text.replace('&amp;', '&')
    clean_text = clean_text.replace('&lt;', '<')
    clean_text = clean_text.replace('&gt;', '>')
    return clean_text.strip()


def generate_pdf(collection):
    """Generate business card sized PDF for flashcards in collection"""
    buffer = BytesIO()

    # Business card size: 3.5" x 2" (standard US business card)
    card_width = 3.5 * inch
    card_height = 2 * inch

    doc = SimpleDocTemplate(buffer, pagesize=(card_width, card_height),
                           topMargin=0.1*inch, bottomMargin=0.1*inch,
                           leftMargin=0.1*inch, rightMargin=0.1*inch)

    styles = getSampleStyleSheet()

    # Custom styles for business card sized content
    front_style = ParagraphStyle(
        'Front',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        spaceAfter=0.05*inch,
        leading=10
    )

    back_style = ParagraphStyle(
        'Back',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        leading=10
    )

    story = []

    for flashcard in collection.flashcards.all():
        # Front of card
        front_text = clean_html(flashcard.front)
        story.append(Paragraph(f"<b>Front:</b>", front_style))
        story.append(Paragraph(front_text, front_style))
        story.append(Spacer(1, 0.1*inch))

        # Back of card
        back_text = clean_html(flashcard.back)
        story.append(Paragraph(f"<b>Back:</b>", back_style))
        story.append(Paragraph(back_text, back_style))

        # Page break for next card
        story.append(PageBreak())

    # Remove last page break
    if story and isinstance(story[-1], PageBreak):
        story.pop()

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()