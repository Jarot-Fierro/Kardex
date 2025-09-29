from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UsuarioPersonalizado


@admin.register(UsuarioPersonalizado)
class CustomUserAdmin(UserAdmin):
    model = UsuarioPersonalizado

    list_display = (
        'username',
        'rut',
        'first_name',
        'last_name',
        'email',
        'tipo_perfil',
        'establecimiento',
        'is_staff',
        'is_superuser',
    )

    search_fields = ('username', 'rut', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': (
                'rut',
                'first_name',
                'last_name',
                'email',
                'establecimiento',
                'tipo_perfil',
            ),
        }),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'rut',
                'first_name',
                'last_name',
                'email',
                'establecimiento',
                'tipo_perfil',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            ),
        }),
    )
