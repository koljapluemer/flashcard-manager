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
    """Generate business card sized PDF for flashcards - proper front/back layout for printing"""
    buffer = BytesIO()

    # Business card size: 3.5" x 2" (standard US business card)
    card_width = 3.5 * inch
    card_height = 2 * inch

    doc = SimpleDocTemplate(buffer, pagesize=(card_width, card_height),
                           topMargin=0.15*inch, bottomMargin=0.15*inch,
                           leftMargin=0.15*inch, rightMargin=0.15*inch)

    styles = getSampleStyleSheet()

    # Custom style for flashcard content
    card_style = ParagraphStyle(
        'Card',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=0,
        leading=12,
        wordWrap='CJK'
    )

    story = []
    flashcards = list(collection.flashcards.all())

    for flashcard in flashcards:
        # FRONT of flashcard (odd page)
        front_text = clean_html(flashcard.front)
        story.append(Paragraph(front_text, card_style))
        story.append(PageBreak())

        # BACK of flashcard (even page - will be on reverse when printed duplex)
        back_text = clean_html(flashcard.back)
        story.append(Paragraph(back_text, card_style))

        # Add page break unless this is the last card
        if flashcard != flashcards[-1]:
            story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()