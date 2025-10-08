from django.urls import path

from .views import LoginViewCustom, LogoutViewCustom, PerfilUsuarioView, CambiarPasswordView

app_name = 'usuarios'
urlpatterns = [
    path('login/', LoginViewCustom.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
    path('cambiar-password/', CambiarPasswordView.as_view(), name='cambiar_password'),
]
