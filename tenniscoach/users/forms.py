from django import forms
from .models import Profile

class OptionalFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.required = False

class UserProfileForm(OptionalFieldsMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'description', 'email', 'picture']
        labels = {
            'name': 'Nome',
            'surname': 'Cognome',
            'description': 'Descrizione personale',
            'email': 'Indirizzo email',
            'picture': 'Immagine del profilo',
        }