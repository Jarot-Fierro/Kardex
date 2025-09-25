from django import forms

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Pais


class FormPais(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre del pais',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_pais',
                'class': 'form-control',
                'placeholder': 'Chile',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    cod_pais = forms.CharField(
        label='Código del Pais',
        widget=forms.TextInput(
            attrs={
                'id': 'codigo_pais',
                'class': 'form-control',
                'placeholder': '1132',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    class Meta:
        model = Pais
        fields = ['nombre', 'cod_pais']
