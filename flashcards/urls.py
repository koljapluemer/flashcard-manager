from django.urls import path
from .views import (
    flashcard_list, flashcard_create, flashcard_edit, flashcard_delete, flashcard_history,
    collection_list, collection_create, collection_edit, collection_delete,
    collection_detail, collection_history, collection_pdf, collection_upload_csv,
    collection_practice
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
    path('collections/create/', collection_create, name='collection_create'),
    path('collections/upload-csv/', collection_upload_csv, name='collection_upload_csv'),
    path('collections/<int:pk>/', collection_detail, name='collection_detail'),
    path('collections/<int:pk>/edit/', collection_edit, name='collection_edit'),
    path('collections/<int:pk>/delete/', collection_delete, name='collection_delete'),
    path('collections/<int:pk>/history/', collection_history, name='collection_history'),
    path('collections/<int:pk>/pdf/', collection_pdf, name='collection_pdf'),
    path('practice/<int:pk>/', collection_practice, name='collection_practice'),
]