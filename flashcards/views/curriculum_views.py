from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Curriculum, Subject, Topic, FlashcardCollection
from ..curriculum_forms import CurriculumForm, SubjectForm, TopicForm


@login_required
def curriculum_list(request):
    curricula = Curriculum.objects.all()
    breadcrumbs = [
        {'name': 'Curricula', 'url': None}
    ]
    return render(request, 'flashcards/curriculum/list.html', {
        'curricula': curricula,
        'breadcrumbs': breadcrumbs
    })


@login_required
def curriculum_create(request):
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': 'New Curriculum', 'url': None}
    ]
    if request.method == 'POST':
        form = CurriculumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curriculum created successfully.')
            return redirect('curriculum_list')
    else:
        form = CurriculumForm()
    return render(request, 'flashcards/curriculum/curriculum_form.html', {
        'form': form,
        'action': 'Create',
        'breadcrumbs': breadcrumbs
    })


@login_required
def curriculum_edit(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': curriculum.name, 'url': f'/flashcards/curricula/{curriculum.pk}/subjects/'},
        {'name': 'Edit', 'url': None}
    ]
    if request.method == 'POST':
        form = CurriculumForm(request.POST, instance=curriculum)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curriculum updated successfully.')
            return redirect('curriculum_list')
    else:
        form = CurriculumForm(instance=curriculum)
    return render(request, 'flashcards/curriculum/curriculum_form.html', {
        'form': form,
        'action': 'Edit',
        'breadcrumbs': breadcrumbs
    })


@login_required
def curriculum_delete(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    if request.method == 'POST':
        curriculum.delete()
        messages.success(request, 'Curriculum deleted successfully.')
        return redirect('curriculum_list')
    return render(request, 'flashcards/curriculum/delete.html', {'object': curriculum, 'type': 'Curriculum'})


@login_required
def subject_create(request, curriculum_pk):
    curriculum = get_object_or_404(Curriculum, pk=curriculum_pk)
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': curriculum.name, 'url': f'/flashcards/curricula/{curriculum.pk}/subjects/'},
        {'name': 'New Subject', 'url': None}
    ]
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.curriculum = curriculum
            subject.save()
            messages.success(request, 'Subject created successfully.')
            return redirect('curriculum_detail', curriculum_pk=curriculum.pk)
    else:
        form = SubjectForm()
    return render(request, 'flashcards/curriculum/subject_form.html', {
        'form': form,
        'curriculum': curriculum,
        'action': 'Create',
        'breadcrumbs': breadcrumbs
    })


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': subject.curriculum.name, 'url': f'/flashcards/curricula/{subject.curriculum.pk}/subjects/'},
        {'name': subject.name, 'url': f'/flashcards/subjects/{subject.pk}/topics/'},
        {'name': 'Edit', 'url': None}
    ]
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('curriculum_detail', curriculum_pk=subject.curriculum.pk)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'flashcards/curriculum/subject_form.html', {
        'form': form,
        'curriculum': subject.curriculum,
        'action': 'Edit',
        'breadcrumbs': breadcrumbs
    })


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('curriculum_list')
    return render(request, 'flashcards/curriculum/delete.html', {'object': subject, 'type': 'Subject'})


@login_required
def topic_create(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': subject.curriculum.name, 'url': f'/flashcards/curricula/{subject.curriculum.pk}/subjects/'},
        {'name': subject.name, 'url': f'/flashcards/subjects/{subject.pk}/topics/'},
        {'name': 'New Topic', 'url': None}
    ]
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.save()
            messages.success(request, 'Topic created successfully.')
            return redirect('subject_detail', subject_pk=subject.pk)
    else:
        form = TopicForm()
    return render(request, 'flashcards/curriculum/topic_form.html', {
        'form': form,
        'subject': subject,
        'action': 'Create',
        'breadcrumbs': breadcrumbs
    })


@login_required
def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{topic.subject.curriculum.pk}/subjects/'},
        {'name': topic.subject.name, 'url': f'/flashcards/subjects/{topic.subject.pk}/topics/'},
        {'name': topic.name, 'url': f'/flashcards/topics/{topic.pk}/collections/'},
        {'name': 'Edit', 'url': None}
    ]
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated successfully.')
            return redirect('subject_detail', subject_pk=topic.subject.pk)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'flashcards/curriculum/topic_form.html', {
        'form': form,
        'subject': topic.subject,
        'action': 'Edit',
        'breadcrumbs': breadcrumbs
    })


@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Topic deleted successfully.')
        return redirect('curriculum_list')
    return render(request, 'flashcards/curriculum/delete.html', {'object': topic, 'type': 'Topic'})


@login_required
def subject_list(request, curriculum_pk):
    curriculum = get_object_or_404(Curriculum, pk=curriculum_pk)
    subjects = curriculum.subjects.all()
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': curriculum.name, 'url': None}
    ]
    return render(request, 'flashcards/curriculum/subject_list.html', {
        'curriculum': curriculum,
        'subjects': subjects,
        'breadcrumbs': breadcrumbs
    })


@login_required
def topic_list(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    topics = subject.topics.all()
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': subject.curriculum.name, 'url': f'/flashcards/curricula/{subject.curriculum.pk}/subjects/'},
        {'name': subject.name, 'url': None}
    ]
    return render(request, 'flashcards/curriculum/topic_list.html', {
        'subject': subject,
        'topics': topics,
        'breadcrumbs': breadcrumbs
    })


@login_required
def collection_list_for_topic(request, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    collections = topic.collections.all()
    breadcrumbs = [
        {'name': 'Curricula', 'url': '/flashcards/curricula/'},
        {'name': topic.subject.curriculum.name, 'url': f'/flashcards/curricula/{topic.subject.curriculum.pk}/subjects/'},
        {'name': topic.subject.name, 'url': f'/flashcards/subjects/{topic.subject.pk}/topics/'},
        {'name': topic.name, 'url': None}
    ]
    return render(request, 'flashcards/collections/topic_collections.html', {
        'topic': topic,
        'collections': collections,
        'breadcrumbs': breadcrumbs
    })
