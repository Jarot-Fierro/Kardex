from django import forms

from kardex.models import MovimientoFicha, Ficha, ServicioClinico, Profesional


class FormEntradaFicha(forms.ModelForm):
    fecha_entrada = forms.DateTimeField(
        label='Fecha de Recepción',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_entrada_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

    rut = forms.ChoiceField(
        label='RUT',
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'id': 'id_rut',
            'class': 'form-control select2-ajax',
            'readonly': 'readonly'
        })
    )

    nombre = forms.CharField(
        label='Nombre del paciente',
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'nombre_mov',
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )

    servicio_clinico = forms.ModelChoiceField(
        label='Servicio Clínico',
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        empty_label="Seleccione un Servicio Clínico",
        widget=forms.Select(
            attrs={
                'id': 'servicio_clinico_ficha',
                'class': 'form-control select2',
                'readonly': 'readonly'
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
        empty_label="Seleccione una Ficha",
        queryset=Ficha.objects.none(),
        widget=forms.Select(
            attrs={
                'id': 'id_ficha',
                'class': 'form-control select2',
                'readonly': 'readonly'
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
                'class': 'form-control select2',

            }
        ),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = args[0] if args else None

        if data:
            ficha_id = data.get('ficha')
            if ficha_id and ficha_id.isdigit():
                from kardex.models import Ficha
                try:
                    ficha = Ficha.objects.get(pk=ficha_id)
                    self.fields['ficha'].queryset = Ficha.objects.filter(pk=ficha.pk)
                except Ficha.DoesNotExist:
                    pass

            rut_id = data.get('rut')
            if rut_id and rut_id.isdigit():
                from kardex.models import MovimientoFicha
                try:
                    mov = MovimientoFicha.objects.get(pk=rut_id)
                    self.fields['rut'].choices = [
                        (mov.pk,
                         f"{mov.ficha.ingreso_paciente.paciente.rut} - {mov.ficha.ingreso_paciente.paciente.nombre}")
                    ]
                except MovimientoFicha.DoesNotExist:
                    pass

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_entrada',
            'servicio_clinico',
            'observacion_entrada',
            'ficha',
            'profesional',
            'rut',
            'nombre',
        ]


class FormSalidaFicha(forms.ModelForm):
    ficha = forms.ModelChoiceField(
        label='Ficha',
        queryset=Ficha.objects.none(),
        widget=forms.Select(
            attrs={
                'id': 'id_ficha',
                'class': 'form-control select2-ajax'
            }
        ),
        required=True
    )

    rut = forms.ChoiceField(
        label='RUT',
        required=False,
        choices=[],
        widget=forms.Select(
            attrs={
                'id': 'id_rut',
                'class': 'form-control select2-ajax'
            }
        )
    )

    nombre = forms.CharField(
        label='Nombre del paciente',
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_mov',
                'class': 'form-control',
                'readonly': 'readonly'
            }
        )
    )
    servicio_clinico = forms.ModelChoiceField(
        label='Servicio Clínico',
        empty_label="Selecciona un Servicio Clínico",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si el formulario viene con un valor ya seleccionado en POST (como ocurre con Select2 AJAX)
        if 'ficha' in self.data:
            try:
                ficha_id = int(self.data.get('ficha'))
                self.fields['ficha'].queryset = Ficha.objects.filter(id=ficha_id)
            except (ValueError, TypeError):
                pass  # Si por alguna razón el ID no es válido, dejamos el queryset vacío

        # Si estamos editando una instancia existente
        elif self.instance.pk:
            self.fields['ficha'].queryset = Ficha.objects.filter(pk=self.instance.ficha_id)

        # --- RUT ---
        if 'rut' in self.data:
            rut_value = self.data.get('rut')
            # Asumimos que rut_value es texto como "12345678-9"
            self.fields['rut'].choices = [(rut_value, rut_value)]
        elif self.instance.pk:
            # Si estás editando, podrías mostrar el rut original si lo tienes
            self.fields['rut'].choices = [(self.instance.ficha.paciente.rut, self.instance.ficha.paciente.rut)]

    class Meta:
        model = MovimientoFicha
        fields = [
            'ficha',
            'fecha_salida',
            'servicio_clinico',
            'observacion_salida',
            'profesional',
            'rut',
            'nombre',
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
