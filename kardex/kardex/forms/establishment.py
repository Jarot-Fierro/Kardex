from django import forms
from django.core.validators import MaxLengthValidator

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Establishment


class FormEstablishment(forms.ModelForm):
    name = forms.CharField(
        label='Nombre del Establecimiento',
        widget=forms.TextInput(
            attrs={
                'id': 'name_establishment',
                'class': 'form-control',
                'placeholder': 'Nombre del Establecimiento',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    address = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(
            attrs={
                'id': 'address_establishment',
                'class': 'form-control',
                'placeholder': 'Ohiggins 20',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    phone = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(
            attrs={
                'id': 'phone_establishment',
                'class': 'form-control',
                'placeholder': '+56912345678',
            }),
        required=False,
        validators=[MaxLengthValidator(15, message='No puedes escribir más de 15 caracteres.')],
    )

    class Meta:
        model = Establishment
        fields = ['name', 'address', 'phone']
