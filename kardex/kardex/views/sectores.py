from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.sectores import FormSector
from kardex.mixin import DataTableMixin
from kardex.models import Sector
from kardex.views.history import GenericHistoryListView

MODULE_NAME = 'Sectors'


class SectorListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/sector/list.html'
    model = Sector
    datatable_columns = ['ID', 'Código', 'Color', 'Observación', 'Establecimiento']
    datatable_order_fields = ['id', 'codigo', 'color', 'observacion', 'establecimiento__nombre']
    datatable_search_fields = [
        'codigo__icontains',
        'color__icontains',
        'observacion__icontains',
        'establecimiento__nombre__icontains'
    ]

    permission_required = 'kardex.view_sector'
    raise_exception = True

    permission_view = 'kardex.view_sector'
    permission_update = 'kardex.change_sector'
    permission_delete = 'kardex.delete_sector'

    url_detail = 'kardex:sector_detail'
    url_update = 'kardex:sector_update'
    url_delete = 'kardex:sector_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Código': (obj.codigo or '').upper(),
            'Color': (obj.color or '').capitalize(),  # Solo primera mayúscula para mostrar
            'Observación': (obj.observacion or '').capitalize(),  # Si usas SECTOR_COLORS
            'Establecimiento': (obj.establecimiento.nombre or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Sectores',
            'list_url': reverse_lazy('kardex:sector_list'),
            'create_url': reverse_lazy('kardex:sector_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class SectorDetailView(PermissionRequiredMixin, DetailView):
    model = Sector
    template_name = 'kardex/sector/detail.html'
    permission_required = 'kardex.view_sector'
    raise_exception = True

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class SectorCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/sector/form.html'
    model = Sector
    form_class = FormSector
    success_url = reverse_lazy('kardex:sector_list')
    permission_required = 'kardex:add_sector'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Sector creado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Sector'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class SectorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/sector/form.html'
    model = Sector
    form_class = FormSector
    success_url = reverse_lazy('kardex:sector_list')
    permission_required = 'kardex:change_sector'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Sector actualizado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Sector'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class SectorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Sector
    template_name = 'kardex/sector/confirm_delete.html'
    success_url = reverse_lazy('kardex:sector_list')
    permission_required = 'kardex:delete_sector'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Sector eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el sector: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Sector'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context


class SectorHistoryListView(GenericHistoryListView):
    base_model = Sector
    permission_required = 'kardex.view_sector'
    template_name = 'kardex/history/list.html'
