from django import forms

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Comuna


class FormComuna(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre de la comuna',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_comuna',
                'class': 'form-control',
                'placeholder': 'Lebu',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    codigo = forms.CharField(
        label='Código de Comuna',
        widget=forms.TextInput(
            attrs={
                'id': 'codigo_comuna',
                'class': 'form-control',
                'placeholder': '1132',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    class Meta:
        model = Comuna
        fields = ['nombre', 'codigo']
