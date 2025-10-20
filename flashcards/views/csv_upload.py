from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from ..models import Flashcard, FlashcardCollection
from ..collection_forms import CSVUploadForm
import csv
import os


@login_required
def collection_upload_csv(request, pk):
    """Upload CSV to add flashcards to existing collection."""
    from django.shortcuts import get_object_or_404
    collection = get_object_or_404(FlashcardCollection, pk=pk)

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            try:
                with transaction.atomic():
                    # Parse CSV and create flashcards
                    csv_file.seek(0)
                    content = csv_file.read().decode('utf-8')
                    csv_reader = csv.reader(content.splitlines())

                    flashcards_to_create = []
                    valid_rows = 0

                    for row in csv_reader:
                        # Skip empty rows
                        if not any(cell.strip() for cell in row):
                            continue

                        front = row[0].strip()
                        back = row[1].strip()

                        if front and back:
                            flashcards_to_create.append(Flashcard(
                                collection=collection,
                                front=front,
                                back=back
                            ))
                            valid_rows += 1

                    # Bulk create flashcards with collection assigned
                    Flashcard.objects.bulk_create(flashcards_to_create)

                    messages.success(
                        request,
                        f'Successfully added {valid_rows} flashcards to "{collection.title}".'
                    )
                    return redirect('collection_detail', pk=collection.pk)

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVUploadForm()

    context = {
        'form': form,
        'collection': collection
    }
    return render(request, 'flashcards/collections/upload_csv.html', context)