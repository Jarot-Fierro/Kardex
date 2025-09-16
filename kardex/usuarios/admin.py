from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UsuarioPersonalizado


@admin.register(UsuarioPersonalizado)
class CustomUserAdmin(UserAdmin):
    model = UsuarioPersonalizado
    # Opcional: personaliza los campos que se muestran en el admin
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Campos adicionales', {
            'fields': ('comuna', 'establecimiento', 'tipo_perfil'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos adicionales', {
            'fields': ('comuna', 'establecimiento', 'tipo_perfil'),
        }),
    )
