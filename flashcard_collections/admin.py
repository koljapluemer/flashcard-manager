from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import FlashcardCollection


@admin.register(FlashcardCollection)
class FlashcardCollectionAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'flashcard_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['flashcards']

    def flashcard_count(self, obj):
        return obj.flashcards.count()
    flashcard_count.short_description = 'Flashcards'
