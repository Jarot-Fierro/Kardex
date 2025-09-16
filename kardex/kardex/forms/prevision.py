from django import forms

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Prevision


class FormPrevision(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre de la Previsión',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_establishment',
                'class': 'form-control',
                'placeholder': 'Lebu',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    class Meta:
        model = Prevision
        fields = ['nombre']
