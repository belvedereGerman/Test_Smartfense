from django.forms import ModelForm
from .models import Snippet, Language

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ["name", "description", "language", "public", "snippet"]
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "language": "Lenguaje",
            "public": "Público",
            "snippet": "Snippet",
        }
