from django import forms

from kardex.models import Ficha, Establecimiento, Profesional, Paciente
from usuarios.models import UsuarioPersonalizado


class FormFicha(forms.ModelForm):
    numero_ficha_sistema = forms.CharField(
        label='Número de Ficha',
        widget=forms.TextInput(attrs={
            'id': 'id_numero_ficha_sistema',
            'class': 'form-control',
            'placeholder': 'Ingrese el número de numero_ficha_sistema',
            'autocomplete': 'off'
        }),
        required=True
    )
    observacion = forms.CharField(
        label='Observación',
        widget=forms.Textarea(attrs={
            'id': 'observacion_numero_ficha_sistema',
            'class': 'form-control',
            'placeholder': 'Ingrese una observación (opcional)',
            'rows': 3
        }),
        required=False
    )

    fecha_mov = forms.DateField(
        label='Fecha de Movimiento',
        widget=forms.DateInput(attrs={
            'id': 'fecha_mov_numero_ficha_sistema',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={
            'id': 'establecimiento_numero_ficha_sistema',
            'class': 'form-control'
        }),
        required=False
    )
    paciente = forms.ModelChoiceField(
        label='Paciente',
        queryset=Paciente.objects.filter(nombre='SILVIA').all(),
        widget=forms.Select(attrs={
            'id': 'paciente_numero_ficha_sistema',
            'class': 'form-control select2'
        }),
        required=False
    )

    profesional = forms.ModelChoiceField(
        label='Profesional',
        queryset=Profesional.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={
            'id': 'profesional_numero_ficha_sistema',
            'class': 'form-control'
        }),
        required=False
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={
            'id': 'usuario_numero_ficha_sistema',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Ficha
        fields = [
            'numero_ficha_sistema',
            'paciente',
            'observacion',
            'fecha_mov',
            'establecimiento',
            'profesional',
            'usuario',
        ]
