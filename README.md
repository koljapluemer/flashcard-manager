# Flashcard Manager

Internal flashcard management app for author team.

## What it does

- Create/edit flashcards with rich text (front/back)
- Organize flashcards into collections
- Bulk import via CSV upload
- Export collections as business-card PDFs
- Full audit history (soft-delete only)
- Login required, no registration

## Structure

```
flashcards/                 # Main app (consolidated)
├── models.py              # Flashcard + FlashcardCollection
├── views/                 # Split into flashcard_views, collection_views, csv_upload
├── forms.py               # Flashcard forms
├── collection_forms.py    # Collection + CSV upload forms
├── utils.py               # PDF generation (WeasyPrint)
└── admin.py               # Admin interfaces

templates/flashcards/      # All templates
├── list.html, form.html   # Flashcard templates
└── collections/           # Collection templates

accounts/                  # Email+password auth only
```

## Tech stack

- Django 5.2 + Poetry
- PostgreSQL (SQLite for dev)
- django-summernote (rich text)
- django-simple-history (audit trail)
- WeasyPrint (PDF generation)
- Tailwind + DaisyUI (via CDN)

## URLs

```
/                          # Home (login required)
/login/                    # Login
/flashcards/               # Flashcard list
/flashcards/collections/   # Collection list + CSV upload
```

## Run locally

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

## CSV format

2 columns, no header:
```
What is 2+2?,4
Capital of France,Paris
```

Creates collection named after filename.