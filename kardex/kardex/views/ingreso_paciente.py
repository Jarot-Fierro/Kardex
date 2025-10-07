from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.ingreso_pacientes import FormIngresoPaciente
from kardex.mixin import DataTableMixin
from kardex.models import IngresoPaciente

MODULE_NAME = 'Ingresos de Paciente'


class IngresoPacienteListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/ingreso_paciente/list.html'
    model = IngresoPaciente
    datatable_columns = ['ID', 'Paciente', 'Establecimiento', 'Fecha Ingreso']
    # El orden debe mapear 1:1 con las columnas visibles
    datatable_order_fields = ['id', 'paciente__rut', 'establecimiento__nombre', 'created_at']
    datatable_search_fields = [
        'paciente__rut__icontains'
    ]

    permission_required = 'kardex.view_ingreso_paciente'
    raise_exception = True

    permission_view = 'kardex.view_ingreso_paciente'
    permission_update = 'kardex.change_ingreso_paciente'
    permission_delete = 'kardex.delete_ingreso_paciente'

    url_detail = 'kardex:ingreso_paciente_detail'
    url_update = 'kardex:ingreso_paciente_update'
    url_delete = 'kardex:ingreso_paciente_delete'

    def get_base_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        # Asegura filtrar por el establecimiento del usuario logueado
        qs = super().get_base_queryset()
        user = getattr(self, 'request', None).user if hasattr(self, 'request') else None
        est = getattr(self.request, 'establecimiento', None)
        if not est and user is not None:
            est = getattr(user, 'establecimiento', None)
        if est:
            qs = qs.filter(establecimiento=est)
        return qs

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Paciente': getattr(obj.paciente, 'rut', '') or '',
            'Establecimiento': getattr(obj.establecimiento, 'nombre', '') or '',
            'Fecha Ingreso': obj.created_at.strftime('%Y-%m-%d') if obj.created_at else '',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Ingresos de Paciente',
            'list_url': reverse_lazy('kardex:ingreso_paciente_list'),
            'create_url': reverse_lazy('kardex:ingreso_paciente_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class IngresoPacienteDetailView(PermissionRequiredMixin, DetailView):
    model = IngresoPaciente
    template_name = 'kardex/ingreso_paciente/detail.html'

    permission_required = 'kardex.view_ingreso_paciente'
    raise_exception = True

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class IngresoPacienteCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/ingreso_paciente/form.html'
    model = IngresoPaciente
    form_class = FormIngresoPaciente
    success_url = reverse_lazy('kardex:ingreso_paciente_list')

    permission_required = 'kardex.add_ingreso_paciente'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Ingreso de paciente creado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Ingreso de Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class IngresoPacienteUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/ingreso_paciente/form.html'
    model = IngresoPaciente
    form_class = FormIngresoPaciente
    success_url = reverse_lazy('kardex:ingreso_paciente_list')

    permission_required = 'kardex.change_ingreso_paciente'
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
            messages.success(request, 'Ingreso de paciente actualizado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Ingreso de Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class IngresoPacienteDeleteView(PermissionRequiredMixin, DeleteView):
    model = IngresoPaciente
    template_name = 'kardex/ingreso_paciente/confirm_delete.html'
    success_url = reverse_lazy('kardex:ingreso_paciente_list')

    permission_required = 'kardex.delete_ingreso_paciente'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Ingreso de paciente eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el ingreso de paciente: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Ingreso de Paciente'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
