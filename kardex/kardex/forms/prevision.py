from django import forms

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Prevision


class FormPrevision(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre de la Previsión',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_prevision',
                'class': 'form-control',
                'placeholder': 'Fonasa A, Isapre, etc...',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    class Meta:
        model = Prevision
        fields = ['nombre']
