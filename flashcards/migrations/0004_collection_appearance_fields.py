from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0003_flashcardcollection_historicalflashcardcollection'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcardcollection',
            name='header_text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='flashcardcollection',
            name='header_text_color',
            field=models.CharField(blank=True, default='#111827', max_length=7),
        ),
        migrations.AddField(
            model_name='flashcardcollection',
            name='header_bg_color',
            field=models.CharField(blank=True, default='#e5e7eb', max_length=7),
        ),
        migrations.AddField(
            model_name='flashcardcollection',
            name='card_text_color',
            field=models.CharField(blank=True, default='#333333', max_length=7),
        ),
        migrations.AddField(
            model_name='flashcardcollection',
            name='card_bg_color',
            field=models.CharField(blank=True, default='#f7f7f5', max_length=7),
        ),
    ]

