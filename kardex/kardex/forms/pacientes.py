from django import forms

from kardex.models import Paciente, Comuna, Prevision
from usuarios.models import UsuarioPersonalizado


class FormPaciente(forms.ModelForm):
    rut = forms.CharField(
        label='R.U.T.',
        widget=forms.TextInput(attrs={
            'class': 'form-control id_rut',
            'placeholder': 'Ingrese el RUT',
            'id': 'id_rut'
        }),
        required=True
    )

    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre',
            'id': 'nombre_paciente'
        }),
        required=True
    )

    apellido_paterno = forms.CharField(
        label='Apellido Paterno',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido paterno',
            'id': 'apellido_paterno_paciente'
        }),
        required=True
    )

    apellido_materno = forms.CharField(
        label='Apellido Materno',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido materno',
            'id': 'apellido_materno_paciente'
        }),
        required=True
    )

    rut_madre = forms.CharField(
        label='R.U.T. Madre',
        widget=forms.TextInput(attrs={
            'class': 'form-control id_rut',
            'placeholder': 'Opcional',
            'id': 'id_rut_madre'
        }),
        required=False
    )

    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control fecha-input',
            'type': 'date',
            'id': 'fecha_nacimiento_paciente'
        }),
        required=True
    )

    sexo = forms.ChoiceField(
        label='Sexo',
        choices=Paciente._meta.get_field('sexo').choices,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'sexo_paciente'}),
        required=True
    )

    estado_civil = forms.ChoiceField(
        label='Estado Civil',
        choices=Paciente._meta.get_field('estado_civil').choices,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'estado_civil_paciente'}),
        required=True
    )

    nombres_padre = forms.CharField(
        label='Nombres del Padre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'nombres_padre_paciente'
        }),
        required=False
    )

    nombres_madre = forms.CharField(
        label='Nombres de la Madre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'nombres_madre_paciente'
        }),
        required=False
    )

    nombre_pareja = forms.CharField(
        label='Nombre de la Pareja',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'nombre_pareja_paciente'
        }),
        required=False
    )

    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: O’Higgins 123',
            'id': 'direccion_paciente'
        }),
        required=True
    )

    numero_telefono1 = forms.CharField(
        label='Teléfono 1',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56912345678',
            'id': 'numero_telefono1_paciente'
        }),
        required=False
    )

    numero_telefono2 = forms.CharField(
        label='Teléfono 2',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'numero_telefono2_paciente'
        }),
        required=False
    )

    pasaporte = forms.CharField(
        label='Pasaporte',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'pasaporte_paciente'
        }),
        required=False
    )

    nie = forms.CharField(
        label='NIE',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'nie_paciente'
        }),
        required=False
    )

    rut_responsable_temporal = forms.CharField(
        label='RUT Responsable Temporal',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'rut_responsable_temporal_paciente'
        }),
        required=False
    )

    usar_rut_madre_como_responsable = forms.BooleanField(
        label='Usar RUT de la madre como responsable',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'usar_rut_madre_como_responsable_paciente'})
    )

    recien_nacido = forms.BooleanField(
        label='¿Es recién nacido?',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'recien_nacido_paciente'})
    )

    extranjero = forms.BooleanField(
        label='¿Es extranjero?',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'extranjero_paciente'})
    )

    fallecido = forms.BooleanField(
        label='¿Está fallecido?',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'fallecido_paciente'})
    )

    fecha_fallecimiento = forms.DateField(
        label='Fecha de Fallecimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control fecha-input',
            'type': 'date',
            'id': 'fecha_fallecimiento_paciente'
        }),
        required=False
    )

    ocupacion = forms.CharField(
        label='Ocupación',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: Docente',
            'id': 'ocupacion_paciente'
        }),
        required=False
    )

    representante_legal = forms.CharField(
        label='Representante Legal',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'representante_legal_paciente'
        }),
        required=False
    )

    nombre_social = forms.CharField(
        label='Nombre Social',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'nombre_social_paciente'
        }),
        required=False
    )

    comuna = forms.ModelChoiceField(
        label='Comuna',
        empty_label='Seleccione una Comuna',
        queryset=Comuna.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'comuna_paciente'}),
        required=True
    )

    prevision = forms.ModelChoiceField(
        label='Previsión',
        empty_label='Seleccione una Previsión',
        queryset=Prevision.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'prevision_paciente'}),
        required=True
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        empty_label='Seleccione un Usuario',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'usuario_paciente'}),
        required=False
    )

    class Meta:
        model = Paciente
        fields = [
            'rut',
            'nie',
            'pasaporte',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'rut_madre',
            'rut_responsable_temporal',
            'usar_rut_madre_como_responsable',
            'fecha_nacimiento',
            'sexo',
            'estado_civil',
            'nombres_padre',
            'nombres_madre',
            'nombre_pareja',
            'direccion',
            'numero_telefono1',
            'numero_telefono2',
            'recien_nacido',
            'extranjero',
            'fallecido',
            'fecha_fallecimiento',
            'ocupacion',
            'representante_legal',
            'nombre_social',
            'comuna',
            'prevision',
            'usuario',
        ]


class PacienteFechaRangoForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha inicio',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True,
    )
    fecha_fin = forms.DateField(
        label='Fecha fin',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True,
    )
