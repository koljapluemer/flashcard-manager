from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Flashcard, FlashcardCollection
from django.core.files.base import ContentFile
from io import BytesIO
try:
    from PIL import Image
except Exception:
    Image = None


class FlashcardForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=FlashcardCollection.objects.all().order_by('-created_at'),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        label='Collections'
    )
    class Meta:
        model = Flashcard
        fields = ['front', 'front_layout', 'front_image', 'back', 'back_layout', 'back_image', 'collections']
        widgets = {
            'front': SummernoteWidget(),
            'back': SummernoteWidget(),
            'front_layout': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'back_layout': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'front_image': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full', 'accept': 'image/*'}),
            'back_image': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full', 'accept': 'image/*'}),
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
        # Process images (resize/compress) if provided
        def process_image(field_name):
            if Image is None:
                return
            file = self.cleaned_data.get(field_name)
            if not file:
                return
            try:
                img = Image.open(file)
                img = img.convert('RGB') if img.mode not in ('RGB', 'L') else img
                max_size = (1200, 800)
                img.thumbnail(max_size, Image.LANCZOS)
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=82, optimize=True)
                buffer.seek(0)
                content = ContentFile(buffer.read())
                # Replace the uploaded file content
                getattr(flashcard, field_name).save(file.name.rsplit('.', 1)[0] + '.jpg', content, save=False)
            except Exception:
                # If processing fails, keep original uploaded file
                pass

        process_image('front_image')
        process_image('back_image')
        if commit:
            flashcard.save()
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

    def clean(self):
        cleaned = super().clean()
        # Disallow image upload when layout is text-only
        fl = cleaned.get('front_layout')
        fi = cleaned.get('front_image')
        if fl == Flashcard.LAYOUT_TEXT_ONLY and fi:
            self.add_error('front_layout', 'Layout cannot be text-only when an image is uploaded.')
        bl = cleaned.get('back_layout')
        bi = cleaned.get('back_image')
        if bl == Flashcard.LAYOUT_TEXT_ONLY and bi:
            self.add_error('back_layout', 'Layout cannot be text-only when an image is uploaded.')
        return cleaned
