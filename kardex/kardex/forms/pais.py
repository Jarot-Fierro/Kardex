from django import forms

from config.validations import validate_spaces, validate_exists
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

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Pais.objects.filter(nombre__iexact=nombre).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_spaces(nombre)
        validate_exists(nombre, exists)
        return nombre

    def clean_cod_pais(self):
        cod_pais = self.cleaned_data['cod_pais'].strip()

        validate_spaces(cod_pais)
        return cod_pais

    class Meta:
        model = Pais
        fields = ['nombre', 'cod_pais']
