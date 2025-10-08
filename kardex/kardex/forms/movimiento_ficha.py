from django import forms

from kardex.models import MovimientoFicha, Ficha, ServicioClinico, Profesional


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
    profesional = forms.ModelChoiceField(
        label='Profesional',
        empty_label="Seleccione un Profesional",
        queryset=Profesional.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(
            attrs={
                'id': 'profesional_movimiento',
                'class': 'form-control select2'
            }
        ),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_entrada',
            'servicio_clinico',
            'observacion_entrada',
            'ficha',
            'profesional',
        ]


class FormSalidaFicha(forms.ModelForm):
    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'ficha_mov',
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
    profesional = forms.ModelChoiceField(
        label='Profesional',
        empty_label="Seleccione un Profesional",
        queryset=Profesional.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(
            attrs={
                'id': 'profesional_movimiento',
                'class': 'form-control select2'
            }
        ),
        required=True
    )

    class Meta:
        model = MovimientoFicha
        fields = [
            'ficha',
            'fecha_salida',
            'servicio_clinico',
            'observacion_salida',
            'profesional',
        ]


class FiltroSalidaFichaForm(forms.Form):
    hora_inicio = forms.DateTimeField(
        label="Hora inicio",
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=False
    )
    hora_termino = forms.DateTimeField(
        label="Hora término",
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=False
    )
    servicio_clinico = forms.ModelChoiceField(
        label="Servicio Clínico",
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    profesional = forms.ModelChoiceField(
        label="Profesional asignado",
        queryset=Profesional.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )
