from django.db import models
from simple_history.models import HistoricalRecords


class Flashcard(models.Model):
    front = models.TextField()
    back = models.TextField()
    # Optional images + layout per side
    LAYOUT_TEXT_ONLY = 'text_only'
    LAYOUT_TEXT_LEFT_IMAGE_RIGHT = 'text_left_image_right'
    LAYOUT_TEXT_RIGHT_IMAGE_LEFT = 'text_right_image_left'
    LAYOUT_CHOICES = [
        (LAYOUT_TEXT_ONLY, 'Text only'),
        (LAYOUT_TEXT_LEFT_IMAGE_RIGHT, 'Text left, image right'),
        (LAYOUT_TEXT_RIGHT_IMAGE_LEFT, 'Text right, image left'),
    ]

    front_layout = models.CharField(max_length=32, choices=LAYOUT_CHOICES, default=LAYOUT_TEXT_ONLY)
    back_layout = models.CharField(max_length=32, choices=LAYOUT_CHOICES, default=LAYOUT_TEXT_ONLY)
    front_image = models.ImageField(upload_to='flashcards/', blank=True, null=True)
    back_image = models.ImageField(upload_to='flashcards/', blank=True, null=True)
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
