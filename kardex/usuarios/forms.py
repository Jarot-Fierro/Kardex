# users/forms.py
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# from config.validation_forms import validate_email

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioPersonalizado


class UsuarioPersonalizadoCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'rut', 'tipo_perfil', 'comuna')


class UsuarioPersonalizadoChangeForm(UserChangeForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'rut', 'tipo_perfil', 'comuna')


class CustomLoginForm(forms.Form):
    identifier = forms.CharField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'placeholder': 'example@gmail.com'
        }),
        required=True
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Contraseña'
        }),
        required=True
    )

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')
        # validate_email(identifier)
        return identifier

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')

        if identifier and password:
            # Intentar autenticar por username
            user = authenticate(username=identifier, password=password)

            if not user:
                # Buscar por correo
                try:
                    user_obj = User.objects.get(email=identifier)
                    print(f"{user_obj.email}-EL USUARIO")
                    user = authenticate(username=user_obj.username, password=password)
                    print(user)
                except User.DoesNotExist:
                    user = None

            if not user:
                raise forms.ValidationError("Credenciales inválidas.")

            self.user = user
        print(f"Asignando usuario: {self.user}")
        return cleaned_data

    def save(self, commit=True):
        user = self.instance
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # <- aquí está la magia
        if commit:
            user.save()
        return user

    def get_user(self):
        return getattr(self, 'user', None)


class FormUpdatePasswordUser(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la contraseña'
        }),
        required=True,
        label='Nueva contraseña'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme la contraseña'
        }),
        required=True,
        label='Confirmar contraseña'
    )

    class Meta:
        model = User
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')

    def save(self, commit=True):
        user = self.instance
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class FormUsuario(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        }),
        required=False
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        }),
        required=False
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        }),
        required=True
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario único'
        }),
        required=True
    )

    is_active = forms.ChoiceField(
        choices=[
            (True, 'Activo'),
            (False, 'Inactivo')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=True
    )
    is_staff = forms.ChoiceField(
        choices=[
            (True, 'Está en el equipo'),
            (False, 'Sin permisos')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=True
    )
    is_superuser = forms.ChoiceField(
        choices=[
            (True, 'Administrador'),
            (False, 'Sin permisos')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'is_active',
                  'is_staff', 'is_superuser']

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance.pk:
            # Si estamos editando, evitar que se choque con otro
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este nombre de usuario ya existe.')
        else:
            if User.objects.filter(username=username).exists():
                raise ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este correo ya está en uso.')
        else:
            if User.objects.filter(email=email).exists():
                raise ValidationError('Este correo ya está registrado.')
        return email
