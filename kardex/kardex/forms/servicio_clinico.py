from django import forms

from kardex.models import ServicioClinico, Establecimiento


class FormServicioClinico(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre del Servicio',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Urgencias, Pediatría, etc.'
        }),
        required=True
    )

    tiempo_horas = forms.IntegerField(
        label='Tiempo en Horas',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad de horas asignadas'
        }),
        required=True
    )

    correo_jefe = forms.EmailField(
        label='Correo del Jefe a Cargo',
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

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = ServicioClinico
        fields = [
            'nombre',
            'tiempo_horas',
            'correo_jefe',
            'telefono',
            'establecimiento'
        ]
