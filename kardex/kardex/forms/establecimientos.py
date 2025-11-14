from django import forms
from django.core.validators import MaxLengthValidator

from config.validations import validate_spaces, validate_exists
# from config.validation_forms import validate_nombre, validate_description, validate_spaces, validate_exists
from kardex.models import Establecimiento, Comuna


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
                'placeholder': '(44) 123 4567 ',
            }),
        required=False,
        validators=[MaxLengthValidator(15, message='No puedes escribir más de 15 caracteres.')],
    )
    comuna = forms.ModelChoiceField(
        label="Comuna",
        empty_label="Selecciona una Comuna",
        queryset=Comuna.objects.filter(status="ACTIVE"),
        widget=forms.Select(
            attrs={
                'id': 'comuna_establecimiento',
                'class': 'form-control select2',
            }),
        required=True
    )

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Establecimiento.objects.filter(nombre__iexact=nombre).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_spaces(nombre)
        validate_exists(nombre, exists)

        return nombre

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion'].strip()

        validate_spaces(direccion)

        return direccion

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()

        validate_spaces(telefono)

        return telefono

    class Meta:
        model = Establecimiento
        fields = ['nombre', 'direccion', 'telefono', 'comuna']
