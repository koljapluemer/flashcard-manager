from .flashcard_views import (
    flashcard_list,
    flashcard_create,
    flashcard_edit,
    flashcard_delete,
    flashcard_history
)
from .collection_views import (
    collection_list,
    collection_create,
    collection_edit,
    collection_delete,
    collection_detail,
    collection_history,
    collection_pdf,
    collection_practice
)
from .csv_upload import collection_upload_csv

__all__ = [
    'flashcard_list',
    'flashcard_create',
    'flashcard_edit',
    'flashcard_delete',
    'flashcard_history',
    'collection_list',
    'collection_create',
    'collection_edit',
    'collection_delete',
    'collection_detail',
    'collection_history',
    'collection_pdf',
    'collection_practice',
    'collection_upload_csv'
]