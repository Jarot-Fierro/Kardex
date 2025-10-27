from django import forms

from kardex.models import ServicioClinico, Establecimiento


class FormServicioClinico(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre del Servicio',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Urgencias, Pediatría, etc.',
            'id': 'nombre_servicioclinico'
        }),
        required=True
    )

    correo_jefe = forms.EmailField(
        label='Correo del Jefe a Cargo',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.cl',
            'id': 'correo_jefe_servicioclinico'
        }),
        required=True
    )

    telefono = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-control telefono_personal',
            'placeholder': '+56912345678',
            'id': 'telefono_servicioclinico'
        }),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        empty_label='Seleccione un Establecimiento',
        queryset=Establecimiento.objects.filter(status='ACTIVE'),
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'id': 'establecimiento_servicioclinico'
        }),
        required=True
    )

    class Meta:
        model = ServicioClinico
        fields = [
            'nombre',
            'correo_jefe',
            'telefono',
            'establecimiento'
        ]
