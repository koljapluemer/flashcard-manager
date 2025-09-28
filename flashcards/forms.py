from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Flashcard, FlashcardCollection


class FlashcardForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=FlashcardCollection.objects.all().order_by('-created_at'),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        label='Collections'
    )
    class Meta:
        model = Flashcard
        fields = ['front', 'back', 'collections']
        widgets = {
            'front': SummernoteWidget(),
            'back': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-select collections for existing instance
        if self.instance and self.instance.pk:
            self.fields['collections'].initial = self.instance.flashcardcollection_set.all()

    def clean_collections(self):
        cols = self.cleaned_data.get('collections')
        if not cols or len(cols) == 0:
            raise forms.ValidationError('Select at least one collection.')
        return cols

    def save(self, commit=True):
        flashcard = super().save(commit=commit)
        # Sync collections membership
        selected = set(self.cleaned_data.get('collections', []))
        if flashcard.pk:
            current = set(flashcard.flashcardcollection_set.all())
            # Add to newly selected
            for col in selected - current:
                col.flashcards.add(flashcard)
            # Remove from unselected
            for col in current - selected:
                col.flashcards.remove(flashcard)
        return flashcard
