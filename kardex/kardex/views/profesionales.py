from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.profesionales import FormProfesional
from kardex.mixin import DataTableMixin
from kardex.models import Profesional
from kardex.views.history import GenericHistoryListView

MODULE_NAME = 'Profesionales'


class ProfesionalListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/profesional/list.html'
    model = Profesional
    datatable_columns = ['ID', 'RUT', 'Nombre', 'Correo', 'Teléfono', 'Profesión', 'Establecimiento']
    datatable_order_fields = ['id', None, 'rut', 'nombres', 'correo', 'telefono', 'profesion__nombre',
                              'establecimiento__nombre']
    datatable_search_fields = [
        'rut__icontains', 'nombres__icontains', 'correo__icontains', 'telefono__icontains',
        'profesion__nombre__icontains', 'establecimiento__nombre__icontains'
    ]

    permission_required = 'kardex.view_profesionales'
    raise_exception = True

    permission_view = 'kardex.view_profesionales'
    permission_update = 'kardex.change_profesionales'
    permission_delete = 'kardex.delete_profesionales'

    url_detail = 'kardex:profesional_detail'
    url_update = 'kardex:profesional_update'
    url_delete = 'kardex:profesional_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'RUT': obj.rut,
            'Nombre': (obj.nombres or '').upper(),
            'Correo': (obj.correo or ''),
            'Teléfono': (obj.telefono or ''),
            'Profesión': (getattr(obj.profesion, 'nombre', '') or '').upper(),
            'Establecimiento': (getattr(obj.establecimiento, 'nombre', '') or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Profesionales',
            'list_url': reverse_lazy('kardex:profesional_list'),
            'create_url': reverse_lazy('kardex:profesional_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class ProfesionalDetailView(PermissionRequiredMixin, DetailView):
    model = Profesional
    template_name = 'kardex/profesional/detail.html'
    permission_required = 'kardex.view_profesionales'
    raise_exception = True

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class ProfesionalCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/profesional/form.html'
    model = Profesional
    form_class = FormProfesional
    success_url = reverse_lazy('kardex:profesional_list')
    permission_required = 'kardex.add_profesionales'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Profesional creado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Profesional'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class ProfesionalUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/profesional/form.html'
    model = Profesional
    form_class = FormProfesional
    success_url = reverse_lazy('kardex:profesional_list')
    permission_required = 'kardex.change_profesionales'
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
            messages.success(request, 'Profesional actualizado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Profesional'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class ProfesionalDeleteView(PermissionRequiredMixin, DeleteView):
    model = Profesional
    template_name = 'kardex/profesional/confirm_delete.html'
    success_url = reverse_lazy('kardex:profesional_list')
    permission_required = 'kardex.delete_profesionales'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Profesional eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el profesional: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Profesional'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context


class ProfesionalHistoryListView(GenericHistoryListView):
    base_model = Profesional
    permission_required = 'kardex.view_profesional'
    template_name = 'kardex/history/list.html'
