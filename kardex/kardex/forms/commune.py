from django import forms

# from config.validation_forms import validate_name, validate_description, validate_spaces, validate_exists
from kardex.models import Commune


class FormCommune(forms.ModelForm):
    name = forms.CharField(
        label='Nombre de la comuna',
        widget=forms.TextInput(
            attrs={
                'id': 'name_establishment',
                'class': 'form-control',
                'placeholder': 'Lebu',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    code = forms.CharField(
        label='Código de Comuna',
        widget=forms.TextInput(
            attrs={
                'id': 'code_establishment',
                'class': 'form-control',
                'placeholder': '1132',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    class Meta:
        model = Commune
        fields = ['name', 'code']
