from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from kardex.models import Establecimiento

# from config.validation_forms import validate_email

User = get_user_model()

from django import forms


class UsuarioPersonalizadoChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'tipo_perfil', 'establecimiento']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'username': 'RUT',
            'establecimiento': 'Establecimiento',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'username': forms.TextInput(attrs={'class': 'form-control id_rut', 'placeholder': '12.345.678-9'}),
            'establecimiento': forms.Select(
                attrs={'id': 'usuario_establecimiento', 'class': 'form-control select2'}
            ),
            'tipo_perfil': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limitar establecimientos activos únicamente
        self.fields['establecimiento'].queryset = Establecimiento.objects.filter(status="ACTIVE")

        # Forzar todos los campos como obligatorios
        for field in self.fields.values():
            field.required = True


class UsuarioPersonalizadoCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'tipo_perfil', 'establecimiento']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'username': 'RUT',
            'tipo_perfil': 'Tipo de perfil',
            'establecimiento': 'Establecimiento',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'username': forms.TextInput(attrs={'class': 'form-control id_rut', 'placeholder': '12.345.678-9'}),
            'tipo_perfil': forms.Select(attrs={'class': 'form-control'}),
            'establecimiento': forms.Select(attrs={'id': 'usuario_establecimiento', 'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limitar establecimientos activos
        self.fields['establecimiento'].queryset = Establecimiento.objects.filter(status="ACTIVE")

        # Forzar todos los campos obligatorios (incluye password1 y password2)
        for field in self.fields.values():
            field.required = True


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={
            'id': 'id_rut',
            'class': 'form-control',
            'placeholder': 'Ej: 12.345.678-9'
        }),
        required=True
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            # print(username, password)
            # print(User.objects.filter(username='20.930.055-9'))

            if not user:
                raise forms.ValidationError("Credenciales Inválidas.")

            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

    def save(self, commit=True):
        return self.get_user()


class ChangePasswordLoggedUserForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña actual'
        }),
        required=True,
        label='Contraseña actual'
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        }),
        required=True,
        label='Nueva contraseña'
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        }),
        required=True,
        label='Confirmar nueva contraseña'
    )

    class Meta:
        model = User
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        user = self.instance
        if not user.check_password(current_password or ''):
            self.add_error('current_password', 'La contraseña actual es incorrecta.')

        if password1 and password2 and password1 != password2:
            self.add_error('new_password2', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = self.instance
        password = self.cleaned_data.get('new_password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
