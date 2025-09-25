from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.servicio_clinico import FormServicioClinico
from kardex.mixin import DataTableMixin
from kardex.models import ServicioClinico

MODULE_NAME = 'Servicios Clínicos'


class ServicioClinicoListView(DataTableMixin, TemplateView):
    template_name = 'kardex/servicio_clinico/list.html'
    model = ServicioClinico
    datatable_columns = ['ID', 'Nombre', 'Descripción']
    datatable_order_fields = ['id', None, 'nombre', 'descripcion']
    datatable_search_fields = ['nombre__icontains', 'descripcion__icontains']

    url_detail = 'kardex:servicio_clinico_detail'
    url_update = 'kardex:servicio_clinico_update'
    url_delete = 'kardex:servicio_clinico_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Nombre': (obj.nombre or '').upper(),
            'Descripción': (obj.descripcion or ''),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Servicios Clínicos',
            'list_url': reverse_lazy('kardex:servicio_clinico_list'),
            'create_url': reverse_lazy('kardex:servicio_clinico_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class ServicioClinicoDetailView(DetailView):
    model = ServicioClinico
    template_name = 'kardex/servicio_clinico/detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class ServicioClinicoCreateView(CreateView):
    template_name = 'kardex/servicio_clinico/form.html'
    model = ServicioClinico
    form_class = FormServicioClinico
    success_url = reverse_lazy('kardex:servicio_clinico_list')
    permission_required = 'add_servicioclinico'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Servicio clínico creado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Servicio Clínico'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class ServicioClinicoUpdateView(UpdateView):
    template_name = 'kardex/servicio_clinico/form.html'
    model = ServicioClinico
    form_class = FormServicioClinico
    success_url = reverse_lazy('kardex:servicio_clinico_list')
    permission_required = 'change_servicioclinico'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Servicio clínico actualizado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Servicio Clínico'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class ServicioClinicoDeleteView(DeleteView):
    model = ServicioClinico
    template_name = 'kardex/servicio_clinico/confirm_delete.html'
    success_url = reverse_lazy('kardex:servicio_clinico_list')
    permission_required = 'delete_servicioclinico'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Servicio clínico eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el servicio clínico: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Servicio Clínico'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
