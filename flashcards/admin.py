from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import Flashcard, FlashcardCollection


@admin.register(Flashcard)
class FlashcardAdmin(SummernoteModelAdmin, SimpleHistoryAdmin):
    list_display = ['id', 'front_preview', 'back_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['front', 'back']
    summernote_fields = ('front', 'back')

    def front_preview(self, obj):
        return obj.front[:50] + '...' if len(obj.front) > 50 else obj.front
    front_preview.short_description = 'Front'

    def back_preview(self, obj):
        return obj.back[:50] + '...' if len(obj.back) > 50 else obj.back
    back_preview.short_description = 'Back'


@admin.register(FlashcardCollection)
class FlashcardCollectionAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'flashcard_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['flashcards']

    def flashcard_count(self, obj):
        return obj.flashcards.count()
    flashcard_count.short_description = 'Flashcards'
