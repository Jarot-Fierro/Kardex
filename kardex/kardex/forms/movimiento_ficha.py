from django import forms

from kardex.choices import ESTADO_RESPUESTA
from kardex.models import MovimientoFicha, Establecimiento, Ficha
from usuarios.models import UsuarioPersonalizado


class FormEntradaFicha(forms.ModelForm):
    fecha_mov = forms.DateTimeField(
        label='Fecha de Movimiento',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    fecha_entrada = forms.DateTimeField(
        label='Fecha de Entrada',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    observacion_entrada = forms.CharField(
        label='Observación de Entrada',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una observación de entrada (opcional)'
        }),
        required=False
    )

    usuario_entrada = forms.CharField(
        label='Usuario que Recibe',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del usuario que recibe'
        }),
        required=True
    )

    status2 = forms.ChoiceField(
        label='Estado',
        choices=ESTADO_RESPUESTA,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_mov',
            'fecha_entrada',
            'observacion_entrada',
            'usuario_entrada',
            'status2',
            'establecimiento',
            'ficha',
            'usuario',
        ]


class FormSalidaFicha(forms.ModelForm):
    fecha_mov = forms.DateTimeField(
        label='Fecha de Movimiento',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    fecha_salida = forms.DateTimeField(
        label='Fecha de Salida',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    observacion_salida = forms.CharField(
        label='Observación de Salida',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una observación de salida (opcional)'
        }),
        required=False
    )

    usuario_entrega = forms.CharField(
        label='Usuario que Entrega',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del usuario que entrega'
        }),
        required=True
    )

    status2 = forms.ChoiceField(
        label='Estado',
        choices=ESTADO_RESPUESTA,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_mov',
            'fecha_salida',
            'observacion_salida',
            'usuario_entrega',
            'status2',
            'establecimiento',
            'ficha',
            'usuario',
        ]
