from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Flashcard


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front', 'back']
        widgets = {
            'front': SummernoteWidget(),
            'back': SummernoteWidget(),
        }