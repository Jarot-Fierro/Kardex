from django import forms

from kardex.models import Profesional, Establecimiento


class FormProfesional(forms.ModelForm):
    rut = forms.CharField(
        label='R.U.T.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el RUT del profesional'
        }),
        required=True
    )

    nombres = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del profesional'
        }),
        required=True
    )

    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.cl'
        }),
        required=True
    )

    telefono = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56912345678'
        }),
        required=True
    )

    tipo_usuario = forms.ChoiceField(
        label='Tipo de Usuario',
        choices=Profesional._meta.get_field('tipo_usuario').choices,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Profesional
        fields = [
            'rut',
            'nombres',
            'correo',
            'telefono',
            'tipo_usuario',
            'establecimiento'
        ]
