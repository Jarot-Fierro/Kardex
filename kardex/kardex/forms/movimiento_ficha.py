from django import forms

from kardex.choices import ESTADO_RESPUESTA
from kardex.models import MovimientoFicha, Establecimiento, Ficha
from usuarios.models import UsuarioPersonalizado


class FormEntradaFicha(forms.ModelForm):
    fecha_mov = forms.DateTimeField(
        label='Fecha de Movimiento',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_mov_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    fecha_entrada = forms.DateTimeField(
        label='Fecha de Entrada',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_entrada_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    observacion_entrada = forms.CharField(
        label='Observación de Entrada',
        widget=forms.Textarea(attrs={
            'id': 'observacion_entrada_ficha',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una observación de entrada (opcional)'
        }),
        required=False
    )

    usuario_entrada = forms.CharField(
        label='Usuario que Recibe',
        widget=forms.TextInput(attrs={
            'id': 'usuario_entrada_ficha',
            'class': 'form-control',
            'placeholder': 'Nombre del usuario que recibe'
        }),
        required=True
    )

    estado_respuesta = forms.ChoiceField(
        label='Estado',
        choices=ESTADO_RESPUESTA,
        widget=forms.Select(
            attrs={
                'id': 'estado2_ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(
            attrs={
                'id': 'establecimiento_ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'ficha_movimiento',
                'class': 'form-control'
            }
        ),
        required=True
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'usuario_ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_mov',
            'fecha_entrada',
            'observacion_entrada',
            'usuario_entrada',
            'estado_respuesta',
            'establecimiento',
            'ficha',
            'usuario',
        ]


class FormSalidaFicha(forms.ModelForm):
    fecha_mov = forms.DateTimeField(
        label='Fecha de Movimiento',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_mov_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    fecha_salida = forms.DateTimeField(
        label='Fecha de Salida',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_salida_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    observacion_salida = forms.CharField(
        label='Observación de Salida',
        widget=forms.Textarea(attrs={
            'id': 'observacion_salida_ficha',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una observación de salida (opcional)'
        }),
        required=False
    )

    usuario_entrega = forms.CharField(
        label='Usuario que Entrega',
        widget=forms.TextInput(attrs={
            'id': 'usuario_entrega_ficha',
            'class': 'form-control',
            'placeholder': 'Nombre del usuario que entrega'
        }),
        required=True
    )

    estado_respuesta = forms.ChoiceField(
        label='Estado',
        choices=ESTADO_RESPUESTA,
        widget=forms.Select(
            attrs={
                'id': 'estado2_ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(
            attrs={
                'id': 'establecimiento_ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'usuario_ficha',
                'class': 'form-control'
            }
        ),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_mov',
            'fecha_salida',
            'observacion_salida',
            'usuario_entrega',
            'estado_respuesta',
            'establecimiento',
            'ficha',
            'usuario',
        ]
