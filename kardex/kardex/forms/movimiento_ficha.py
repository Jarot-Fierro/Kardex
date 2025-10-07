from django import forms

from kardex.models import MovimientoFicha, Ficha, ServicioClinico


class FormEntradaFicha(forms.ModelForm):
    fecha_entrada = forms.DateTimeField(
        label='Fecha de Entrada',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_entrada_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    servicio_clinico = forms.ModelChoiceField(
        label='Servicio Clínico',
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(
            attrs={
                'id': 'servicio_clinico_ficha',
                'class': 'form-control select2'
            }
        ),
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

    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'ficha_movimiento',
                'class': 'form-control select2'
            }
        ),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_entrada',
            'observacion_entrada',
            'ficha',
        ]


class FormSalidaFicha(forms.ModelForm):
    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'ficha_movimiento',
                'class': 'form-control select2'
            }
        ),
        required=True
    )
    servicio_clinico = forms.ModelChoiceField(
        label='Servicio Clínico',
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(
            attrs={
                'id': 'servicio_clinico_ficha',
                'class': 'form-control select2'
            }
        ),
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

    class Meta:
        model = MovimientoFicha
        fields = [
            'ficha',
            'fecha_salida',
            'observacion_salida',
        ]


class RangoFechaPacienteForm(forms.Form):
    fecha_inicio = forms.DateField(
        label="Fecha Hora Inicio",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False
    )
    fecha_fin = forms.DateField(
        label="Fecha Hora Término",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False
    )
    servicio_clinico = forms.ModelChoiceField(
        label="Servicio Clínico",
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    profesional = forms.ModelChoiceField(
        label="Profesional",
        queryset=None,  # To be set in the view
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
