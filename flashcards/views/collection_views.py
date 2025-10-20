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
def collection_create(request, topic_pk):
    from ..models import Topic

    topic = get_object_or_404(Topic.objects.select_related('subject__curriculum'), pk=topic_pk)

    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{topic.subject.curriculum.pk}/subjects/'},
        {'name': topic.subject.name, 'url': f'/flashcards/subjects/{topic.subject.pk}/topics/'},
        {'name': topic.name, 'url': f'/flashcards/topics/{topic.pk}/collections/'},
        {'name': 'New Collection', 'url': None}
    ]

    if request.method == 'POST':
        form = FlashcardCollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.topic = topic
            collection.save()
            messages.success(request, 'Collection created successfully.')
            return redirect('topic_detail', topic_pk=topic.pk)
    else:
        form = FlashcardCollectionForm()

    context = {
        'form': form,
        'title': 'Create Collection',
        'topic': topic,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'flashcards/collections/form.html', context)


@login_required
def collection_edit(request, pk):
    collection = get_object_or_404(
        FlashcardCollection.objects.select_related('topic__subject__curriculum'),
        pk=pk
    )

    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': collection.topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{collection.topic.subject.curriculum.pk}/subjects/'},
        {'name': collection.topic.subject.name, 'url': f'/flashcards/subjects/{collection.topic.subject.pk}/topics/'},
        {'name': collection.topic.name, 'url': f'/flashcards/topics/{collection.topic.pk}/collections/'},
        {'name': collection.title, 'url': f'/flashcards/collections/{collection.pk}/'},
        {'name': 'Edit', 'url': None}
    ]

    if request.method == 'POST':
        form = FlashcardCollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collection updated successfully.')
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = FlashcardCollectionForm(instance=collection)
    return render(request, 'flashcards/collections/form.html', {
        'form': form,
        'title': 'Edit Collection',
        'topic': collection.topic,
        'breadcrumbs': breadcrumbs
    })


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
    collection = get_object_or_404(
        FlashcardCollection.objects.select_related('topic__subject__curriculum'),
        pk=pk
    )

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

    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': collection.topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{collection.topic.subject.curriculum.pk}/subjects/'},
        {'name': collection.topic.subject.name, 'url': f'/flashcards/subjects/{collection.topic.subject.pk}/topics/'},
        {'name': collection.topic.name, 'url': f'/flashcards/topics/{collection.topic.pk}/collections/'},
        {'name': collection.title, 'url': None}
    ]

    return render(request, 'flashcards/collections/detail.html', {
        'collection': collection,
        'breadcrumbs': breadcrumbs
    })


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
