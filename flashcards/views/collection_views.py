from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from ..models import FlashcardCollection
from ..collection_forms import FlashcardCollectionForm
from ..utils import generate_pdf


@login_required
def collection_list(request):
    collections = FlashcardCollection.objects.all().order_by('-created_at')
    return render(request, 'flashcards/collections/list.html', {'collections': collections})


@login_required
def collection_create(request):
    if request.method == 'POST':
        form = FlashcardCollectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collection created successfully.')
            return redirect('collection_list')
    else:
        form = FlashcardCollectionForm()
    return render(request, 'flashcards/collections/form.html', {'form': form, 'title': 'Create Collection'})


@login_required
def collection_edit(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    if request.method == 'POST':
        form = FlashcardCollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collection updated successfully.')
            return redirect('collection_list')
    else:
        form = FlashcardCollectionForm(instance=collection)
    return render(request, 'flashcards/collections/form.html', {'form': form, 'title': 'Edit Collection'})


@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    if request.method == 'POST':
        collection.delete()
        messages.success(request, 'Collection deleted successfully.')
        return redirect('collection_list')
    return render(request, 'flashcards/collections/delete.html', {'collection': collection})


@login_required
def collection_detail(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)

    if request.method == 'POST':
        ids = request.POST.getlist('flashcards')
        if ids:
            try:
                # Remove selected flashcards from this collection
                removed = collection.flashcards.filter(pk__in=ids)
                count = removed.count()
                for fc in removed:
                    collection.flashcards.remove(fc)
                messages.success(request, f'Removed {count} flashcard(s) from the collection.')
            except Exception:
                messages.error(request, 'Failed to remove selected flashcards. Please try again.')
        else:
            messages.info(request, 'No flashcards selected.')
        return redirect('collection_detail', pk=collection.pk)

    return render(request, 'flashcards/collections/detail.html', {'collection': collection})


@login_required
def collection_history(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    history = collection.history.all()
    return render(request, 'flashcards/collections/history.html', {'collection': collection, 'history': history})


@login_required
def collection_pdf(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{collection.title}.pdf"'

    pdf_content = generate_pdf(request, collection)
    response.write(pdf_content)
    return response


def collection_practice(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    flashcards = collection.flashcards.all()

    if not flashcards:
        raise Http404("This collection has no flashcards.")

    flashcard_data = [
        {
            'front': flashcard.front,
            'back': flashcard.back
        }
        for flashcard in flashcards
    ]

    context = {
        'collection': collection,
        'flashcard_data': flashcard_data,
    }

    return render(request, 'flashcards/collections/practice.html', context)
