from django import forms

from kardex.models import IngresoPaciente, Establecimiento
from kardex.models import Paciente


class FormIngresoPaciente(forms.ModelForm):
    fecha_ingreso = forms.DateField(
        label='Fecha de Ingreso',
        widget=forms.DateInput(
            attrs={
                'id': 'fecha_ingreso',
                'class': 'form-control',
                'type': 'date'
            }
        ),
        required=True
    )
    motivo_ingreso = forms.CharField(
        label='Motivo de Ingreso',
        widget=forms.Textarea(attrs={
            'id': 'motivo_ingreso',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese el motivo del ingreso (opcional)'
        }),
        required=False
    )

    diagnostico_ingreso = forms.CharField(
        label='Diagnóstico de Ingreso',
        widget=forms.Textarea(attrs={
            'id': 'diagnostico_ingreso',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese el diagnóstico del ingreso (opcional)'
        }),
        required=False
    )

    estado_actual = forms.CharField(
        label='Estado Actual',
        widget=forms.Textarea(attrs={
            'id': 'estado_actual',
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese el estado actual del paciente (opcional)'
        }),
        required=False
    )

    fecha_egreso = forms.DateField(
        label='Fecha de Egreso',
        widget=forms.DateInput(
            attrs={
                'id': 'fecha_egreso',
                'class': 'form-control',
                'type': 'date'
            }
        ),
        required=False
    )

    paciente = forms.ModelChoiceField(
        label='Paciente',
        empty_label="Selecciona un Paciente",
        queryset=Paciente.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'paciente',
                'class': 'form-control select2'
            }
        ),
        required=True
    )

    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        empty_label="Selecciona un Establecimiento",
        queryset=Establecimiento.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'establecimiento',
                'class': 'form-control select2'
            }
        ),
        required=True
    )

    class Meta:
        model = IngresoPaciente
        fields = [
            'fecha_ingreso',
            'motivo_ingreso',
            'diagnostico_ingreso',
            'estado_actual',
            'fecha_egreso',
            'paciente',
            'establecimiento'
        ]
