from django import forms

from kardex.models import Ficha, Establecimiento, Profesional
from usuarios.models import UsuarioPersonalizado


class FormFicha(forms.ModelForm):
    ficha = forms.CharField(
        label='Número de Ficha',
        widget=forms.TextInput(attrs={
            'id': 'id_ficha',
            'class': 'form-control',
            'placeholder': 'Ingrese el número de ficha',
            'autocomplete': 'off'
        }),
        required=True
    )
    observacion = forms.CharField(
        label='Observación',
        widget=forms.Textarea(attrs={
            'id': 'observacion_ficha',
            'class': 'form-control',
            'placeholder': 'Ingrese una observación (opcional)',
            'rows': 3
        }),
        required=False
    )

    fecha_mov = forms.DateField(
        label='Fecha de Movimiento',
        widget=forms.DateInput(attrs={
            'id': 'fecha_mov_ficha',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={
            'id': 'establecimiento_ficha',
            'class': 'form-control'
        }),
        required=False
    )

    profesional = forms.ModelChoiceField(
        label='Profesional',
        queryset=Profesional.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={
            'id': 'profesional_ficha',
            'class': 'form-control'
        }),
        required=False
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={
            'id': 'usuario_ficha',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Ficha
        fields = [
            'ficha',
            'observacion',
            'fecha_mov',
            'establecimiento',
            'profesional',
            'usuario',
        ]
