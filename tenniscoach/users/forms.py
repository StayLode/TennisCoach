from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

# Validator per assicurarsi che il nome sia in un formato consono
def validate_name(value):
    parts = value.split()
    for part in parts:
        if not part.isalpha():
            raise ValidationError('Il nome deve contenere solo lettere.')

# Validator per assicurarsi che il cognome sia in un formato consono
def validate_surname(value):
    parts = value.split()
    for part in parts:
        if not part.isalpha():
                raise ValidationError('Il cognome deve contenere solo lettere.')


class OptionalFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.required = False

class UserProfileForm(OptionalFieldsMixin, forms.ModelForm):
    name = forms.CharField(
        max_length=20,
        validators=[validate_name],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    surname = forms.CharField(
        max_length=20,
        validators=[validate_surname],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['name', 'surname','description', 'email', 'picture']
        labels = {
            'name': 'Nome',
            'surname': 'Cognome',
            'description': 'Descrizione',
            'email': 'Indirizzo email',
            'picture': 'Immagine del profilo',
        }
        widgets ={
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'picture': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'picture' in self.fields:
            self.fields['picture'].widget.attrs.pop('clear', None)