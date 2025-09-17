from django import forms

from kardex.models import Paciente, Comuna, Prevision
from usuarios.models import UsuarioPersonalizado


class FormPaciente(forms.ModelForm):
    rut = forms.CharField(
        label='R.U.T.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el RUT',
            'id': 'rut_paciente'
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
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'rut_madre_paciente'
        }),
        required=False
    )

    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
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

    nombres_pabre = forms.CharField(
        label='Nombres del Padre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional',
            'id': 'nombres_pabre_paciente'
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
            'class': 'form-control',
            'type': 'date',
            'id': 'fecha_fallecimiento_paciente'
        }),
        required=False
    )

    ocupacion = forms.CharField(
        label='Ocupación',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: Profesor(a)',
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
        queryset=Comuna.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'comuna_paciente'}),
        required=True
    )

    prevision = forms.ModelChoiceField(
        label='Previsión',
        queryset=Prevision.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'prevision_paciente'}),
        required=True
    )

    usuario = forms.ModelChoiceField(
        label='Usuario Login',
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'usuario_paciente'}),
        required=True
    )

    class Meta:
        model = Paciente
        fields = [
            'rut',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'rut_madre',
            'fecha_nacimiento',
            'sexo',
            'estado_civil',
            'nombres_pabre',
            'nombres_madre',
            'nombre_pareja',
            'direccion',
            'numero_telefono1',
            'numero_telefono2',
            'pasaporte',
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
