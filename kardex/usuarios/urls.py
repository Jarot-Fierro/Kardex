from django.urls import path

from .views import *

app_name = 'usuarios'
urlpatterns = [
    path('login/', LoginViewCustom.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
    # path('perfil/', UserProfileView.as_view(), name='user_profile'),
    # path('crear-usuario/', UserCreateView.as_view(), name='create_user'),
    # path('actualizar-usuario/<int:pk>', UserUpdateView.as_view(), name='update_user'),
    # path('actualizar-contraseña<int:pk>', UserUpdatePasswordView.as_view(), name='change_password')
]
