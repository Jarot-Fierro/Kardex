from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.messages import add_message, SUCCESS
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from usuarios.forms import CustomLoginForm


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

# class UserProfileView(LoginRequiredMixin, View):
#     template_name = 'user_profile.html'
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#
#         try:
#             perfil = user.perfiluser
#         except PerfilUser.DoesNotExist:
#             perfil = None
#
#         usuarios = User.objects.all().select_related('perfiluser').order_by('-date_joined')[:5]
#
#         context = {
#             'users': user,
#             'perfil': perfil,
#             'list_user': usuarios
#         }
#         return render(request, self.template_name, context)

#
# class UserCreateView(CreateView):
#     model = User
#     form_class = FormUsuario
#     template_name = 'user_form.html'
#     success_url = reverse_lazy('user_profile')
#     success_message = "Usuario creado exitosamente."
#
#     def form_valid(self, form):
#         print("✅ form_valid ejecutado")
#         user = form.save(commit=False)
#
#         password = form.cleaned_data.get('password')
#         if password:
#             user.set_password(password)
#             print("🔐 Contraseña seteada")
#
#         user.save()
#         print("👤 Usuario guardado:", user)
#
#         PerfilUser.objects.get_or_create(user=user)
#         messages.success(self.request, self.success_message)
#
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         print("❌ Formulario inválido")
#         print(form.errors)
#         return super().form_invalid(form)
#
#
# class UserUpdateView(View):
#     template_name = 'components/form.html'
#
#     def get(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         form = FormUsuario(instance=user)
#         return render(request, self.template_name, {'form': form, 'id': pk})
#
#     def post(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         form = FormUsuario(request.POST, instance=user)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#
#             password = form.cleaned_data.get('password')
#             if password:
#                 user.set_password(password)
#
#             user.save()
#             messages.success(request, 'Usuario actualizado correctamente.')
#             return redirect('users:user_profile')
#         return render(request, self.template_name, {'form': form, 'id': pk})
#
#
# class UserUpdatePasswordView(View):
#     template_name = 'components/form_password.html'
#
#     def get(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         form = FormUpdatePasswordUser()
#         return render(request, self.template_name, {'form': form, 'id': pk})
#
#     def post(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#
#         form = FormUpdatePasswordUser(request.POST, instance=user)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Contraseña actualizada correctamente.')
#             return redirect('users:user_profile')
#
#         return render(request, self.template_name, {'form': form, 'id': pk})
