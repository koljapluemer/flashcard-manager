from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from ..models import Flashcard
from ..forms import FlashcardForm


@login_required
def flashcard_list(request):
    # Redirect away from all-flashcards view to curricula list
    return redirect('curriculum_list')


@login_required
def flashcard_create(request, collection_pk):
    from ..models import FlashcardCollection
    collection = get_object_or_404(FlashcardCollection, pk=collection_pk)

    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.collection = collection
            flashcard.save()
            messages.success(request, 'Flashcard created successfully.')
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = FlashcardForm()

    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': collection.topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{collection.topic.subject.curriculum.pk}/subjects/'},
        {'name': collection.topic.subject.name, 'url': f'/flashcards/subjects/{collection.topic.subject.pk}/topics/'},
        {'name': collection.topic.name, 'url': f'/flashcards/topics/{collection.topic.pk}/collections/'},
        {'name': collection.title, 'url': f'/flashcards/collections/{collection.pk}/'},
        {'name': 'New Flashcard', 'url': None}
    ]

    return render(request, 'flashcards/form.html', {
        'form': form,
        'title': 'Create Flashcard',
        'collection': collection,
        'breadcrumbs': breadcrumbs
    })


@login_required
def flashcard_edit(request, pk):
    flashcard = get_object_or_404(
        Flashcard.objects.select_related('collection__topic__subject__curriculum'),
        pk=pk
    )

    collection = flashcard.collection
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': collection.topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{collection.topic.subject.curriculum.pk}/subjects/'},
        {'name': collection.topic.subject.name, 'url': f'/flashcards/subjects/{collection.topic.subject.pk}/topics/'},
        {'name': collection.topic.name, 'url': f'/flashcards/topics/{collection.topic.pk}/collections/'},
        {'name': collection.title, 'url': f'/flashcards/collections/{collection.pk}/'},
        {'name': f'{flashcard.front[:30]}...', 'url': None}
    ]

    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES, instance=flashcard)
        if form.is_valid():
            flashcard = form.save()
            messages.success(request, 'Flashcard updated successfully.')
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = FlashcardForm(instance=flashcard)

    return render(request, 'flashcards/form.html', {
        'form': form,
        'title': 'Edit Flashcard',
        'collection': collection,
        'breadcrumbs': breadcrumbs
    })


@login_required
def flashcard_delete(request, pk):
    flashcard = get_object_or_404(Flashcard.objects.select_related('collection'), pk=pk)
    collection_pk = flashcard.collection.pk
    if request.method == 'POST':
        flashcard.delete()
        messages.success(request, 'Flashcard deleted successfully.')
        return redirect('collection_detail', pk=collection_pk)
    return render(request, 'flashcards/delete.html', {'flashcard': flashcard, 'collection': flashcard.collection})


@login_required
def flashcard_history(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    history = flashcard.history.all()
    return render(request, 'flashcards/history.html', {'flashcard': flashcard, 'history': history})
