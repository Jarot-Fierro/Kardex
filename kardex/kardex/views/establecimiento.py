from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.establecimientos import FormEstablecimiento
from kardex.mixin import DataTableMixin
from kardex.models import Establecimiento

MODULE_NAME = 'Establecimientos'


class EstablecimientoListView(DataTableMixin, TemplateView):
    template_name = 'kardex/establecimiento/list.html'
    model = Establecimiento
    datatable_columns = ['ID', 'Nombre', 'Dirección', 'Teléfono', 'Comuna']
    datatable_order_fields = ['id', None, 'nombre', 'direccion', 'telefono', 'comuna__nombre']
    datatable_search_fields = ['nombre__icontains', 'direccion__icontains', 'telefono__icontains',
                               'comuna__nombre__icontains']

    url_detail = 'kardex:establecimiento_detail'
    url_update = 'kardex:establecimiento_update'
    url_delete = 'kardex:establecimiento_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Nombre': obj.nombre.upper(),
            'Dirección': (obj.direccion or '').upper(),
            'Teléfono': (obj.telefono or ''),
            'Comuna': (obj.comuna.nombre or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Establecimientos',
            'list_url': reverse_lazy('kardex:establecimiento_list'),
            'create_url': reverse_lazy('kardex:establecimiento_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class EstablecimientoDetailView(DetailView):
    model = Establecimiento
    template_name = 'kardex/establecimiento/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class EstablecimientoCreateView(CreateView):
    template_name = 'kardex/establecimiento/form.html'
    model = Establecimiento
    form_class = FormEstablecimiento
    success_url = reverse_lazy('kardex:establecimiento_list')
    permission_required = 'add_establecimiento'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Establecimiento creado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Establecimiento'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class EstablecimientoUpdateView(UpdateView):
    template_name = 'kardex/establecimiento/form.html'
    model = Establecimiento
    form_class = FormEstablecimiento
    success_url = reverse_lazy('kardex:establecimiento_list')
    permission_required = 'change_establecimiento'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Establecimiento actualizado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Establecimiento'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class EstablecimientoDeleteView(DeleteView):
    model = Establecimiento
    template_name = 'kardex/establecimiento/confirm_delete.html'
    success_url = reverse_lazy('kardex:establecimiento_list')
    permission_required = 'delete_establecimiento'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Establecimiento eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el establecimiento: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Establecimiento'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
