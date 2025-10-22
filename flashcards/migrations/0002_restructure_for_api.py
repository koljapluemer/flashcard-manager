from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcardcollection',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='flashcardcollection',
            name='header_text',
        ),
        migrations.RemoveField(
            model_name='flashcardcollection',
            name='header_text_color',
        ),
        migrations.RemoveField(
            model_name='flashcardcollection',
            name='header_bg_color',
        ),
        migrations.RemoveField(
            model_name='flashcardcollection',
            name='card_text_color',
        ),
        migrations.RemoveField(
            model_name='flashcardcollection',
            name='card_bg_color',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='front_layout',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='back_layout',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='front_image',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='back_image',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='front_extra',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='front_extra_style',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='back_extra',
        ),
        migrations.RemoveField(
            model_name='flashcard',
            name='back_extra_style',
        ),
        migrations.DeleteModel(
            name='HistoricalFlashcardCollection',
        ),
        migrations.DeleteModel(
            name='HistoricalFlashcard',
        ),
        migrations.DeleteModel(
            name='HistoricalTopic',
        ),
        migrations.DeleteModel(
            name='HistoricalSubject',
        ),
        migrations.DeleteModel(
            name='HistoricalCurriculum',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.DeleteModel(
            name='Curriculum',
        ),
        migrations.AlterModelOptions(
            name='flashcardcollection',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='flashcard',
            options={'ordering': ['id']},
        ),
    ]
