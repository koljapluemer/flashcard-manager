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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title
