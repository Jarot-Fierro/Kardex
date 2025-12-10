from django import forms

from config.validations import validate_spaces
from kardex.choices import SECTOR_COLORS
# from config.validation_forms import validate_nombre, validate_description, validate_spaces, validate_exists
from kardex.models import Sector, Establecimiento


class FormSector(forms.ModelForm):
    codigo = forms.CharField(
        label='Código del Sector',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_sector',
                'class': 'form-control',
                'placeholder': 'Nombre del Sector',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    color = forms.ChoiceField(
        label='Color del Sector',
        choices=SECTOR_COLORS,
        widget=forms.Select(
            attrs={
                'id': 'nombre_sector',
                'class': 'form-control select2',
                'placeholder': 'Color del Sector',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    observacion = forms.CharField(
        label='Observaciones',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_sector',
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=False
    )

    establecimiento = forms.ModelChoiceField(
        label="Establecimiento",
        empty_label="Selecciona una Establecimiento",
        queryset=Establecimiento.objects.filter(status="ACTIVE"),
        widget=forms.Select(
            attrs={
                'id': 'establecimiento_sector',
                'class': 'form-control select2',
            }),
        required=True
    )

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Sector.objects.filter(codigo__iexact=codigo).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_spaces(codigo)

        return codigo

    class Meta:
        model = Sector
        fields = ['codigo', 'color', 'observacion', 'establecimiento']
