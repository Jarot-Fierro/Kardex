from django import forms

from kardex.models import MovimientoFicha, Ficha, ServicioClinico, Profesional


class FormEntradaFicha(forms.ModelForm):
    fecha_recepcion = forms.DateTimeField(
        label='Fecha de Recepción',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_recepcion_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=False
    )

    rut = forms.CharField(
        label='RUT',
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'id_rut',
            'class': 'form-control id_rut',
            'placeholder': 'Ingrese RUT (sin puntos, con guión)'
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

    servicio_clinico_recepcion = forms.ModelChoiceField(
        label='Servicio Clínico de Recepción',
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        empty_label="Seleccione un Servicio Clínico",
        widget=forms.Select(
            attrs={
                'id': 'servicio_clinico_ficha',
                'class': 'form-control select2',
                'readonly': 'readonly'
            }
        ),
        required=False
    )

    observacion_recepcion = forms.CharField(
        label='Observación de Recepción',
        widget=forms.Textarea(attrs={
            'id': 'observacion_recepcion_ficha',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una observación de recepción (opcional)'
        }),
        required=False
    )

    ficha = forms.CharField(
        label='Ficha',
        widget=forms.TextInput(
            attrs={
                'id': 'id_ficha',
                'class': 'form-control id_ficha'
            }
        ),
        required=True
    )

    profesional_recepcion = forms.ModelChoiceField(
        label='Profesional que recibe',
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

    def clean_ficha(self):
        ficha_value = self.cleaned_data['ficha']

        # Intentamos obtener la instancia de Ficha usando ficha_value
        # Aquí debes definir la lógica para convertir ese string a instancia
        # Por ejemplo, si es el ID numérico:
        try:
            print(Ficha.objects.all())
            print(int(ficha_value))
            ficha_instance = Ficha.objects.get(numero_ficha_sistema=int(ficha_value))
        except (ValueError, Ficha.DoesNotExist):
            raise forms.ValidationError("Ficha no válida o no encontrada.")

        return ficha_instance


    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_recepcion',
            'servicio_clinico_recepcion',
            'observacion_recepcion',
            'ficha',
            'profesional_recepcion',
            'rut',
            'nombre',
        ]


class FormSalidaFicha(forms.ModelForm):
    ficha = forms.CharField(
        label='Ficha',
        widget=forms.TextInput(
            attrs={
                'id': 'id_ficha',
                'class': 'form-control id_ficha'
            }
        ),
        required=True
    )

    rut = forms.CharField(
        label='RUT',
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'id_rut',
                'class': 'form-control id_rut',
                'autocomplete': 'off',
                'inputmode': 'text'
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
    servicio_clinico_envio = forms.ModelChoiceField(
        label='Servicio Clínico de Envío',
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

    servicio_clinico_recepcion = forms.ModelChoiceField(
        label='Servicio Clínico de Recepción',
        empty_label="Selecciona un Servicio Clínico",
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        widget=forms.Select(
            attrs={
                'id': 'servicio_clinico_recepcion',
                'class': 'form-control select2'
            }
        ),
        required=True
    )

    fecha_envio = forms.DateTimeField(
        label='Fecha de Envío',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_envio_ficha',
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=False
    )

    observacion_envio = forms.CharField(
        label='Observación de Envío',
        widget=forms.Textarea(attrs={
            'id': 'observacion_envio_ficha',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una observación de envío (opcional)'
        }),
        required=False
    )
    profesional_envio = forms.ModelChoiceField(
        label='Profesional que envía',
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

    def clean_ficha(self):
        ficha_value = self.cleaned_data['ficha']

        # Intentamos obtener la instancia de Ficha usando ficha_value
        # Aquí debes definir la lógica para convertir ese string a instancia
        # Por ejemplo, si es el ID numérico:
        try:
            print(Ficha.objects.all())
            print(int(ficha_value))
            ficha_instance = Ficha.objects.get(numero_ficha_sistema=int(ficha_value))
        except (ValueError, Ficha.DoesNotExist):
            raise forms.ValidationError("Ficha no válida o no encontrada.")

        return ficha_instance

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

        # --- RUT como texto: mantener valor tipeado si viene en POST o instancia ---
        if 'rut' in self.data:
            self.fields['rut'].initial = self.data.get('rut')
        elif self.instance.pk:
            try:
                self.fields['rut'].initial = self.instance.ficha.paciente.rut
            except Exception:
                pass

    class Meta:
        model = MovimientoFicha
        fields = [
            'ficha',
            'fecha_envio',
            'servicio_clinico_envio',
            'servicio_clinico_recepcion',
            'observacion_envio',
            'profesional_envio',
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
