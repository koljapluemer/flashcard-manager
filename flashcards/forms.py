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
    class Meta:
        model = Flashcard
        fields = [
            'front', 'front_layout', 'front_image', 'front_extra_style', 'front_extra',
            'back', 'back_layout', 'back_image', 'back_extra_style', 'back_extra'
        ]
        widgets = {
            'front': SummernoteWidget(),
            'back': SummernoteWidget(),
            'front_layout': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'back_layout': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'front_image': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full', 'accept': 'image/*'}),
            'back_image': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full', 'accept': 'image/*'}),
            'front_extra_style': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'back_extra_style': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'front_extra': SummernoteWidget(),
            'back_extra': SummernoteWidget(),
        }

    def save(self, commit=True):
        flashcard = super().save(commit=False)
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
