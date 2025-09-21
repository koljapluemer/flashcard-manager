from django import forms
from .models import FlashcardCollection
from flashcards.models import Flashcard


class FlashcardCollectionForm(forms.ModelForm):
    class Meta:
        model = FlashcardCollection
        fields = ['title', 'description', 'flashcards']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'flashcards': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flashcards'].queryset = Flashcard.objects.all().order_by('-created_at')