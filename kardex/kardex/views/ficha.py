from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.fichas import FormFicha
from kardex.mixin import DataTableMixin
from kardex.models import Ficha
from kardex.views.history import GenericHistoryListView

MODULE_NAME = 'Fichas'


class FichaListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/ficha/list.html'
    model = Ficha
    datatable_columns = ['ID', 'Número', 'Establecimiento', 'RUT', 'Código', 'Paciente', 'Fecha Creación']
    datatable_order_fields = ['id', 'numero_ficha_sistema', 'establecimiento__nombre',
                              'paciente__rut', 'paciente__codigo', None, 'created_at']
    datatable_search_fields = [
        'numero_ficha_sistema__icontains',
        'profesional__nombres__icontains',
        'usuario__username__icontains',
        'paciente__rut__icontains',
        'paciente__codigo__icontains',
        'establecimiento__nombre__icontains'
    ]

    permission_required = 'kardex.view_ficha'
    raise_exception = True

    permission_view = 'kardex.view_ficha'

    url_detail = 'kardex:ficha_detail'
    url_update = 'kardex:ficha_update'
    url_delete = 'kardex:ficha_delete'

    def render_row(self, obj):
        pac = getattr(obj, 'paciente', None)
        est = getattr(obj, 'establecimiento', None)
        nombre_completo = ''
        if pac:
            nombre_completo = f"{(getattr(pac, 'nombre', '') or '').upper()} {(getattr(pac, 'apellido_paterno', '') or '').upper()} {(getattr(pac, 'apellido_materno', '') or '').upper()}".strip()
        return {
            'ID': obj.id,
            'Número': obj.numero_ficha_sistema,
            'Establecimiento': (getattr(est, 'nombre', '') or '').upper(),
            'RUT': getattr(pac, 'rut', '') if pac else '',
            'Código': getattr(pac, 'codigo', '') if pac else '',
            'Paciente': nombre_completo,
            'Fecha Creación': obj.created_at.strftime('%Y-%m-%d %H:%M') if getattr(obj, 'created_at', None) else '',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Fichas',
            'list_url': reverse_lazy('kardex:ficha_list'),
            'create_url': reverse_lazy('kardex:ficha_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context

    def get_base_queryset(self):
        # Optimiza consultas y, si aplica la política del sistema, restringe por establecimiento del usuario
        qs = Ficha.objects.select_related(
            'paciente',
            'establecimiento',
        )
        # Si la app en otras vistas filtra por establecimiento, puede activarse aquí:
        user = getattr(self.request, 'user', None)
        establecimiento = getattr(user, 'establecimiento', None) if user else None
        if establecimiento:
            qs = qs.filter(establecimiento=establecimiento)
        return qs


class FichaDetailView(PermissionRequiredMixin, DetailView):
    model = Ficha
    template_name = 'kardex/ficha/detail.html'

    permission_required = 'kardex.view_ficha'
    raise_exception = True

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class FichaCreateView(PermissionRequiredMixin, CreateView):
    """
    Vista para crear o editar fichas:
    - Si no viene ficha_id en POST, crea una ficha nueva.
    - Si viene ficha_id, actualiza la ficha existente.
    """
    template_name = 'kardex/ficha/form.html'
    model = Ficha
    form_class = FormFicha
    success_url = reverse_lazy('kardex:ficha_list')

    permission_required = 'kardex.change_ficha'  # Cambiar si quieres que permita crear
    raise_exception = True

    def post(self, request, *args, **kwargs):
        self.object = None
        ficha_id = (request.POST.get('ficha_id') or '').strip()
        instance = None
        if ficha_id:
            try:
                instance = Ficha.objects.get(pk=ficha_id)
                self.object = instance
            except Ficha.DoesNotExist:
                from django.contrib import messages
                messages.error(request, 'La ficha seleccionada no existe.')
                return self.render_to_response(self.get_context_data(form=self.get_form(), open_modal=True))

        form = self.get_form()
        if instance is not None:
            form.instance = instance  # Edición
        # Si instance es None, form.save() creará una nueva ficha

        if form.is_valid():
            saved_obj = form.save()
            self.object = saved_obj
            from django.contrib import messages
            from django.shortcuts import redirect
            if instance:
                messages.success(request, 'Ficha actualizada correctamente')
            else:
                messages.success(request, 'Ficha creada correctamente')
            return redirect(self.success_url)

        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = instance
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear / Editar Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'edit' if getattr(self, 'object', None) else 'create'
        context['module_name'] = MODULE_NAME
        if getattr(self, 'object', None) is not None:
            context['ficha'] = self.object
        return context


class FichaUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/ficha/form.html'
    model = Ficha
    form_class = FormFicha
    success_url = reverse_lazy('kardex:ficha_list')
    permission_required = 'kardex.change_ficha'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Ficha actualizada correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class TogglePasivadoFichaView(PermissionRequiredMixin, View):
    permission_required = 'kardex.change_ficha'
    raise_exception = True

    def get(self, request, pk, *args, **kwargs):
        try:
            ficha = Ficha.objects.get(pk=pk)
        except Ficha.DoesNotExist:
            messages.error(request, 'La ficha indicada no existe.')
            return redirect('kardex:paciente_query')

        ficha.pasivado = not bool(ficha.pasivado)
        ficha.save(update_fields=['pasivado'])
        if ficha.pasivado:
            messages.success(request, 'La ficha fue pasivada correctamente.')
        else:
            messages.success(request, 'La ficha fue despasivada correctamente.')
        # Volver a la pantalla de consulta/creación
        return redirect('kardex:paciente_query')


class FichaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Ficha
    template_name = 'kardex/ficha/confirm_delete.html'
    success_url = reverse_lazy('kardex:ficha_list')

    permission_required = 'kardex.delete_ficha'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Ficha eliminada correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la ficha: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Ficha'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context


class FichaHistoryListView(GenericHistoryListView):
    base_model = Ficha
    permission_required = 'kardex.view_ficha'
    template_name = 'kardex/history/list.html'
