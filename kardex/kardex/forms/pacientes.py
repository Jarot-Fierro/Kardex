from django import forms

from kardex.models import Paciente, Comuna, Prevision
from usuarios.models import UsuarioPersonalizado


class FormPaciente(forms.ModelForm):
    rut = forms.CharField(
        label='R.U.T.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el RUT'
        }),
        required=True
    )

    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre'
        }),
        required=True
    )

    apellido_paterno = forms.CharField(
        label='Apellido Paterno',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido paterno'
        }),
        required=True
    )

    apellido_materno = forms.CharField(
        label='Apellido Materno',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido materno'
        }),
        required=True
    )

    rut_madre = forms.CharField(
        label='R.U.T. Madre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=True
    )

    sexo = forms.ChoiceField(
        label='Sexo',
        choices=Paciente._meta.get_field('sexo').choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    estado_civil = forms.ChoiceField(
        label='Estado Civil',
        choices=Paciente._meta.get_field('estado_civil').choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    nombres_pabre = forms.CharField(
        label='Nombres del Padre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    nombres_madre = forms.CharField(
        label='Nombres de la Madre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    nombre_pareja = forms.CharField(
        label='Nombre de la Pareja',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: O’Higgins 123'
        }),
        required=True
    )

    numero_telefono1 = forms.CharField(
        label='Teléfono 1',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56912345678'
        }),
        required=False
    )

    numero_telefono2 = forms.CharField(
        label='Teléfono 2',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    pasaporte = forms.CharField(
        label='Pasaporte',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    recien_nacido = forms.BooleanField(
        label='¿Es recién nacido?',
        required=False
    )

    extranjero = forms.BooleanField(
        label='¿Es extranjero?',
        required=False
    )

    fallecido = forms.BooleanField(
        label='¿Está fallecido?',
        required=False
    )

    fecha_fallecimiento = forms.DateField(
        label='Fecha de Fallecimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    ocupacion = forms.CharField(
        label='Ocupación',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: Profesor(a)'
        }),
        required=False
    )

    representante_legal = forms.CharField(
        label='Representante Legal',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    nombre_social = forms.CharField(
        label='Nombre Social',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional'
        }),
        required=False
    )

    comuna = forms.ModelChoiceField(
        label='Comuna',
        queryset=Comuna.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    prevision = forms.ModelChoiceField(
        label='Previsión',
        queryset=Prevision.objects.filter(status='ACTIVE'),
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
