from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from ..models import Flashcard, FlashcardCollection
from ..collection_forms import CSVUploadForm
import csv
import os


@login_required
def collection_upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            try:
                with transaction.atomic():
                    # Create collection name from filename
                    filename = os.path.splitext(csv_file.name)[0]
                    collection_title = filename.replace('_', ' ').replace('-', ' ').title()

                    # Create the collection
                    collection = FlashcardCollection.objects.create(
                        title=collection_title,
                        description=f'Imported from {csv_file.name}'
                    )

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
                            flashcards_to_create.append(Flashcard(front=front, back=back))
                            valid_rows += 1

                    # Bulk create flashcards
                    created_flashcards = Flashcard.objects.bulk_create(flashcards_to_create)

                    # Add all flashcards to the collection
                    collection.flashcards.set(created_flashcards)

                    messages.success(
                        request,
                        f'Successfully created collection "{collection_title}" with {valid_rows} flashcards.'
                    )
                    return redirect('collection_detail', pk=collection.pk)

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVUploadForm()

    return render(request, 'flashcards/collections/upload_csv.html', {'form': form})