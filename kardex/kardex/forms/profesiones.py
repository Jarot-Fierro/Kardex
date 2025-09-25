from django import forms

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Profesion


class FormProfesion(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre de la profesion',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_profesion',
                'class': 'form-control',
                'placeholder': 'Ej: Médico, Enfermera, etc...',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    class Meta:
        model = Profesion
        fields = ['nombre']
