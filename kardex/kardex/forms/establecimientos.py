from django import forms
from django.core.validators import MaxLengthValidator

# from config.validation_forms import validate_nombre, validate_description, validate_spaces, validate_exists
from kardex.models import Establecimiento


class FormEstablecimiento(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre del Establecimiento',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_establecimiento',
                'class': 'form-control',
                'placeholder': 'Nombre del Establecimiento',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(
            attrs={
                'id': 'direccion_establecimiento',
                'class': 'form-control',
                'placeholder': 'Ohiggins 20',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    telefono = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(
            attrs={
                'id': 'telefono_establecimiento',
                'class': 'form-control',
                'placeholder': '+56912345678',
            }),
        required=False,
        validators=[MaxLengthValidator(15, message='No puedes escribir más de 15 caracteres.')],
    )

    class Meta:
        model = Establecimiento
        fields = ['nombre', 'direccion', 'telefono']
