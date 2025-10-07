from django import forms

from kardex.models import IngresoPaciente, Establecimiento
from kardex.models import Paciente


class FormIngresoPaciente(forms.ModelForm):
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
            'paciente',
            'establecimiento'
        ]
