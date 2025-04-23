from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, FileInput

from .models import Publication


class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'full_text', 'date', 'post_image']
