from django import forms
from .models import Course, Lesson
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

import os

def validate_video(value):
    """
    Funzione di validazione per controllare che il file sia un video.
    """
    ext = os.path.splitext(value.name)[1]  # Ottieni l'estensione del file
    valid_extensions = ['.mp4', '.avi', '.mov', '.wmv']  # Estensioni di file video supportate
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Il file caricato non è un video valido. Carica un file con estensione .mp4, .avi, .mov o .wmv.'))

class CreateLessonForm(forms.ModelForm):
    
    video = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[validate_video]
    )
    
    class Meta:
        model = Lesson
        fields = ['title', 'video']
        labels = {
            'title': 'Titolo',
            'video': 'Video'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CreateCorsoForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'picture', 'category', 'price']
        labels = {
            'title': 'Titolo',
            'description': 'Descrizione',
            'picture': 'Immagine',
            'category': 'Categoria',
            'price': 'Prezzo',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=(
                ('Principiante', 'Principiante'),
                ('Intermedio', 'Intermedio'),
                ('Esperto', 'Esperto'),
            ), attrs={'class': 'form-control'})
        }
        price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
            validators=[MinValueValidator(0)]
        )