from rest_framework import serializers
from flashcards.models import Flashcard, FlashcardCollection


class FlashcardCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashcardCollection
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = [
            'id',
            'collection',
            'front',
            'back',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
