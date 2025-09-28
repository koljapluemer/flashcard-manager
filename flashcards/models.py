from django.db import models
from simple_history.models import HistoricalRecords


class Flashcard(models.Model):
    front = models.TextField()
    back = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Flashcard {self.id}"


class FlashcardCollection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    flashcards = models.ManyToManyField(Flashcard, blank=True)
    # Appearance settings
    header_text = models.CharField(max_length=200, blank=True, default='')
    header_text_color = models.CharField(max_length=7, blank=True, default='#111827')  # near-black
    header_bg_color = models.CharField(max_length=7, blank=True, default='#e5e7eb')   # light gray
    card_text_color = models.CharField(max_length=7, blank=True, default='#333333')   # dark grey
    card_bg_color = models.CharField(max_length=7, blank=True, default='#f7f7f5')     # light bone
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title
