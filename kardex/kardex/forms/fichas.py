from django import forms

from kardex.models import Ficha, Establecimiento, Profesional
from usuarios.models import UsuarioPersonalizado


class FormFicha(forms.ModelForm):
    numero_ficha = forms.IntegerField(
        label='Número de Ficha',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número de ficha',
        }),
        required=True
    )
    observacion = forms.CharField(
        label='Observación',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese una observación (opcional)',
            'rows': 3
        }),
        required=False
    )

    fecha_mov = forms.DateField(
        label='Fecha de Movimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    profesional = forms.ModelChoiceField(
        label='Profesional',
        queryset=Profesional.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Ficha
        fields = [
            'numero_ficha',
            'observacion',
            'fecha_mov',
            'establecimiento',
            'profesional',
            'usuario',
        ]
