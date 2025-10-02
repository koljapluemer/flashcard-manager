from django.urls import path
from .views import (
    flashcard_list, flashcard_create, flashcard_edit, flashcard_delete, flashcard_history,
    collection_list, collection_create, collection_edit, collection_delete,
    collection_detail, collection_history, collection_pdf, collection_upload_csv,
    collection_practice,
    curriculum_list, curriculum_create, curriculum_edit, curriculum_delete,
    subject_create, subject_edit, subject_delete,
    topic_create, topic_edit, topic_delete
)

urlpatterns = [
    # Flashcard URLs
    path('', flashcard_list, name='flashcard_list'),
    path('create/', flashcard_create, name='flashcard_create'),
    path('<int:pk>/edit/', flashcard_edit, name='flashcard_edit'),
    path('<int:pk>/delete/', flashcard_delete, name='flashcard_delete'),
    path('<int:pk>/history/', flashcard_history, name='flashcard_history'),

    # Collection URLs
    path('collections/', collection_list, name='collection_list'),
    path('collections/<int:pk>/', collection_detail, name='collection_detail'),
    path('collections/<int:pk>/edit/', collection_edit, name='collection_edit'),
    path('collections/<int:pk>/delete/', collection_delete, name='collection_delete'),
    path('collections/<int:pk>/history/', collection_history, name='collection_history'),
    path('collections/<int:pk>/pdf/', collection_pdf, name='collection_pdf'),
    path('collections/upload-csv/', collection_upload_csv, name='collection_upload_csv'),
    path('practice/<int:pk>/', collection_practice, name='collection_practice'),

    # Curriculum URLs
    path('curricula/', curriculum_list, name='curriculum_list'),
    path('curricula/create/', curriculum_create, name='curriculum_create'),
    path('curricula/<int:pk>/edit/', curriculum_edit, name='curriculum_edit'),
    path('curricula/<int:pk>/delete/', curriculum_delete, name='curriculum_delete'),

    # Subject URLs
    path('curricula/<int:curriculum_pk>/subjects/create/', subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', subject_delete, name='subject_delete'),

    # Topic URLs
    path('subjects/<int:subject_pk>/topics/create/', topic_create, name='topic_create'),
    path('topics/<int:pk>/edit/', topic_edit, name='topic_edit'),
    path('topics/<int:pk>/delete/', topic_delete, name='topic_delete'),

    # Collection creation under topic
    path('topics/<int:topic_pk>/collections/create/', collection_create, name='collection_create_for_topic'),
]