from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.messages import add_message, SUCCESS
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, UpdateView
from django.views.generic.base import View

from .forms import CustomLoginForm, UsuarioPersonalizadoChangeForm, ChangePasswordLoggedUserForm
from .models import UsuarioPersonalizado


@method_decorator(sensitive_post_parameters('password'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class LoginViewCustom(FormView):
    template_name = 'auth/login2.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('index')  # Cambia por la vista principal después de login
    redirect_authenticated_user = True  # lo mantendremos como propiedad manual

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return self.redirect_to_success_url()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if user is None or not user.is_authenticated:
            form.add_error(None, 'Credenciales inválidas. Intente nuevamente.')
            return self.form_invalid(form)

        login(self.request, user)
        self.request.session.set_expiry(0)

        add_message(self.request, SUCCESS, 'Inicio de sesión exitoso.', extra_tags='auth_success')
        return super().form_valid(form)

    def redirect_to_success_url(self):
        return redirect(self.get_success_url())


@method_decorator(never_cache, name='dispatch')
class LogoutViewCustom(LogoutView):
    next_page = 'usuarios:login'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.session.flush()
        add_message(self.request, SUCCESS, 'Se cerró la sesión correctamente.', extra_tags='auth_success')
        return response


class UserUpdateView(View):
    template_name = 'components/form.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UsuarioPersonalizadoChangeForm(instance=user)
        return render(request, self.template_name, {'form': form, 'id': pk})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UsuarioPersonalizadoChangeForm(request.POST, instance=user)

        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)

            user.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('users:user_profile')
        return render(request, self.template_name, {'form': form, 'id': pk})


class PerfilUsuarioView(LoginRequiredMixin, UpdateView):
    template_name = 'usuarios/perfil.html'
    model = UsuarioPersonalizado
    form_class = UsuarioPersonalizadoChangeForm
    success_url = reverse_lazy('usuarios:perfil')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        add_message(self.request, SUCCESS, 'Perfil actualizado correctamente.')
        return response


class CambiarPasswordView(LoginRequiredMixin, FormView):
    template_name = 'usuarios/cambiar_password.html'
    form_class = ChangePasswordLoggedUserForm
    success_url = reverse_lazy('usuarios:perfil')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        add_message(self.request, SUCCESS, 'Contraseña actualizada correctamente.')
        return super().form_valid(form)
