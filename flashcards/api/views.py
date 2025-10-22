from rest_framework import viewsets

from flashcards.models import Flashcard, FlashcardCollection
from .serializers import FlashcardCollectionSerializer, FlashcardSerializer


class FlashcardCollectionViewSet(viewsets.ModelViewSet):
    """CRUD operations for flashcard collections."""

    queryset = FlashcardCollection.objects.all().order_by('id')
    serializer_class = FlashcardCollectionSerializer


class FlashcardViewSet(viewsets.ModelViewSet):
    """CRUD operations for individual flashcards."""

    serializer_class = FlashcardSerializer

    def get_queryset(self):
        queryset = Flashcard.objects.select_related('collection').all().order_by('id')
        collection_id = self.request.query_params.get('collection')
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset
