from django import forms
from .models import FlashcardCollection, Flashcard
import csv
import os


class FlashcardCollectionForm(forms.ModelForm):
    class Meta:
        model = FlashcardCollection
        fields = [
            'topic', 'title', 'description',
            'header_text', 'header_text_color', 'header_bg_color',
            'card_text_color', 'card_bg_color',
        ]
        widgets = {
            'topic': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'header_text': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'e.g. Chapter 1: Basics'}),
            'header_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'h-10 w-20 border border-base-300 rounded bg-base-100'}),
            'header_bg_color': forms.TextInput(attrs={'type': 'color', 'class': 'h-10 w-20 border border-base-300 rounded bg-base-100'}),
            'card_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'h-10 w-20 border border-base-300 rounded bg-base-100'}),
            'card_bg_color': forms.TextInput(attrs={'type': 'color', 'class': 'h-10 w-20 border border-base-300 rounded bg-base-100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered w-full',
            'accept': '.csv'
        }),
        help_text='Upload a CSV file with 2 columns (no header): front, back'
    )

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']

        # Check file extension
        if not file.name.lower().endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file (.csv extension).')

        # Check file size (5MB limit)
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File size must be less than 5MB.')

        # Check if file is readable and has valid CSV format
        try:
            file.seek(0)
            content = file.read().decode('utf-8')
            file.seek(0)

            # Parse CSV and validate structure
            csv_reader = csv.reader(content.splitlines())
            rows = list(csv_reader)

            if not rows:
                raise forms.ValidationError('CSV file is empty.')

            # Check that all non-empty rows have exactly 2 columns
            valid_rows = 0
            for i, row in enumerate(rows, 1):
                # Skip completely empty rows
                if not any(cell.strip() for cell in row):
                    continue

                if len(row) != 2:
                    raise forms.ValidationError(f'Row {i} must have exactly 2 columns (front, back).')

                # Check that both columns have content
                if not row[0].strip() or not row[1].strip():
                    raise forms.ValidationError(f'Row {i} has empty front or back content.')

                valid_rows += 1

            if valid_rows == 0:
                raise forms.ValidationError('No valid rows found in CSV file.')

        except UnicodeDecodeError:
            raise forms.ValidationError('File must be UTF-8 encoded.')
        except Exception as e:
            raise forms.ValidationError(f'Error reading CSV file: {str(e)}')

        return file
