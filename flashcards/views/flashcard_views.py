from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from ..models import Flashcard
from ..forms import FlashcardForm


@login_required
def flashcard_list(request):
    # Redirect away from all-flashcards view to collections list
    return redirect('collection_list')


@login_required
def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES)
        if form.is_valid():
            flashcard = form.save()
            messages.success(request, 'Flashcard created successfully.')
            selected = list(form.cleaned_data.get('collections', []))
            if len(selected) == 1:
                return redirect('collection_detail', pk=selected[0].pk)
            return redirect('collection_list')
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/form.html', {'form': form, 'title': 'Create Flashcard'})


@login_required
def flashcard_edit(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES, instance=flashcard)
        if form.is_valid():
            flashcard = form.save()
            messages.success(request, 'Flashcard updated successfully.')
            selected = list(form.cleaned_data.get('collections', []))
            if len(selected) == 1:
                return redirect('collection_detail', pk=selected[0].pk)
            return redirect('collection_list')
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'flashcards/form.html', {'form': form, 'title': 'Edit Flashcard'})


@login_required
def flashcard_delete(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    if request.method == 'POST':
        # capture related collections before delete
        related = list(flashcard.flashcardcollection_set.all())
        flashcard.delete()
        messages.success(request, 'Flashcard deleted successfully.')
        if len(related) == 1:
            return redirect('collection_detail', pk=related[0].pk)
        return redirect('collection_list')
    return render(request, 'flashcards/delete.html', {'flashcard': flashcard})


@login_required
def flashcard_history(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    history = flashcard.history.all()
    return render(request, 'flashcards/history.html', {'flashcard': flashcard, 'history': history})
