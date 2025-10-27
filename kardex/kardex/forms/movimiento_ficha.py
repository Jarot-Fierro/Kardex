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

    # Nuevo campo de solo lectura para mostrar el Servicio Clínico de Envío (origen)
    servicio_clinico_envio = forms.CharField(
        label='Servicio Clínico de Envío',
        widget=forms.TextInput(
            attrs={
                'id': 'servicio_clinico_envio_ficha',
                'class': 'form-control',
                'readonly': 'readonly',
            }
        ),
        required=False
    )

    servicio_clinico_recepcion = forms.CharField(
        label='Servicio Clínico de Recepción',
        widget=forms.TextInput(
            attrs={
                'id': 'servicio_clinico_ficha',
                'class': 'form-control',
                'readonly': 'readonly',
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

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if hasattr(user, 'servicio_clinico'):
            initial['servicio_clinico_recepcion'] = user.servicio_clinico.nombre
        return initial

    def clean_ficha(self):
        ficha_id = self.cleaned_data['ficha']
        try:
            return Ficha.objects.get(pk=ficha_id)
        except Ficha.DoesNotExist:
            raise forms.ValidationError("Ficha no encontrada")

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_recepcion',
            'observacion_recepcion',
            'rut',
            'ficha',
            'profesional_recepcion',
            'nombre',
        ]


class FormSalidaFicha(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    rut = forms.CharField(
        label='RUT',
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'id_rut',
                'class': 'form-control id_rut',
                'name': 'rut',
                'autocomplete': 'off',
                'inputmode': 'text'
            }
        )
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

    def clean(self):
        cleaned_data = super().clean()
        print("---- DEBUG POST DATA ----")
        print(self.data)
        print("--------------------------")
        return cleaned_data

    def clean_ficha(self):
        ficha_value = self.cleaned_data.get('ficha')
        rut_value = self.cleaned_data.get('rut')  # El nombre del campo es 'rut', no 'id_rut'

        print(ficha_value)
        print(rut_value)

        try:
            # Validaciones básicas
            if not ficha_value or not rut_value:
                raise forms.ValidationError("Debe ingresar el número de ficha y el RUT del paciente.")

            # Conversión a tipos adecuados
            ficha_numero = int(ficha_value)

            # ✅ Obtenemos el establecimiento del usuario logueado
            if not self.user or not hasattr(self.user, 'establecimiento'):
                raise forms.ValidationError("No se encontró el establecimiento asociado al usuario.")

            # Filtro compuesto: ficha + rut + establecimiento
            filtro = {
                'numero_ficha_sistema': ficha_numero,
                'paciente__rut': rut_value,
                'establecimiento': self.user.establecimiento,
            }

            qs = Ficha.objects.filter(**filtro)
            print(qs)

            print('Aqui van los datos')
            print(f'{ficha_numero} {rut_value} {self.user.establecimiento}')
            print('Aqui termina')

            # Validaciones de resultados
            if not qs.exists():
                raise forms.ValidationError("No se encontró ninguna ficha que coincida con los datos ingresados.")

            if qs.count() > 1:
                raise forms.ValidationError(
                    "Existen múltiples fichas con los mismos datos. Contacte al administrador."
                )

            ficha_instance = qs.get()

        except ValueError:
            raise forms.ValidationError("El número de ficha debe ser un valor numérico válido.")
        except Ficha.DoesNotExist:
            raise forms.ValidationError("Ficha no válida o no encontrada.")

        return ficha_instance

    class Meta:
        model = MovimientoFicha
        fields = [
            'rut',
            'ficha',
            'fecha_envio',
            'servicio_clinico_envio',
            'servicio_clinico_recepcion',
            'observacion_envio',
            'profesional_envio',
            'nombre',
        ]


class FormTraspasoFicha(forms.ModelForm):
    fecha_traspaso = forms.DateTimeField(
        label='Fecha de Traspaso',
        widget=forms.DateTimeInput(attrs={
            'id': 'fecha_traspaso_ficha',
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

    servicio_clinico_traspaso = forms.ModelChoiceField(
        label='Servicio Clínico de Traspaso',
        queryset=ServicioClinico.objects.filter(status='ACTIVE').all(),
        empty_label="Seleccione un Servicio Clínico",
        widget=forms.Select(
            attrs={
                'id': 'servicio_clinico_ficha',
                'class': 'form-control select2',
            }
        ),
        required=True
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

    profesional_traspaso = forms.ModelChoiceField(
        label='Profesional que traslada',
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
        # Validación robusta para evitar múltiples coincidencias
        try:
            numero = int(ficha_value)
        except (TypeError, ValueError):
            raise forms.ValidationError("Ficha no válida o no encontrada.")
        qs = Ficha.objects.filter(numero_ficha_sistema=numero)
        if not qs.exists():
            raise forms.ValidationError("Ficha no válida o no encontrada.")
        if qs.count() > 1:
            raise forms.ValidationError(
                "La búsqueda de ficha es ambigua (existen varias con ese número). Use el RUT para cargar o contacte al administrador.")
        return qs.get()

    class Meta:
        model = MovimientoFicha
        fields = [
            'fecha_traspaso',
            'servicio_clinico_traspaso',
            'ficha',
            'profesional_traspaso',
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
