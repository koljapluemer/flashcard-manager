from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from io import BytesIO


def generate_pdf(request, collection):
    """Generate business card sized PDF for flashcards using WeasyPrint - preserves HTML formatting"""
    flashcards = list(collection.flashcards.all())

    # Render HTML template with flashcard data
    html_content = render_to_string('flashcards/collections/flashcard_pdf.html', {
        'collection': collection,
        'flashcards': flashcards
    })

    # Generate PDF from HTML using WeasyPrint
    # Provide base_url so WeasyPrint can resolve absolute/relative URLs, including MEDIA
    base_url = request.build_absolute_uri('/')
    html_doc = HTML(string=html_content, base_url=base_url)
    pdf_buffer = BytesIO()
    html_doc.write_pdf(pdf_buffer)

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
