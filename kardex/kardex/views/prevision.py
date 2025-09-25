from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.prevision import FormPrevision
from kardex.mixin import DataTableMixin
from kardex.models import Prevision

MODULE_NAME = 'Previsiones'


class PrevisionListView(DataTableMixin, TemplateView):
    template_name = 'kardex/prevision/list.html'
    model = Prevision
    datatable_columns = ['ID', 'Nombre']
    datatable_order_fields = ['id', None, 'nombre']
    datatable_search_fields = ['nombre__icontains']

    url_detail = 'kardex:prevision_detail'
    url_update = 'kardex:prevision_update'
    url_delete = 'kardex:prevision_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Nombre': obj.nombre.upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Previsiones',
            'list_url': reverse_lazy('kardex:prevision_list'),
            'create_url': reverse_lazy('kardex:prevision_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class PrevisionDetailView(DetailView):
    model = Prevision
    template_name = 'kardex/prevision/detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class PrevisionCreateView(CreateView):
    template_name = 'kardex/prevision/form.html'
    model = Prevision
    form_class = FormPrevision
    success_url = reverse_lazy('kardex:prevision_list')
    permission_required = 'add_prevision'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Previsión creada correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Previsión'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class PrevisionUpdateView(UpdateView):
    template_name = 'kardex/prevision/form.html'
    model = Prevision
    form_class = FormPrevision
    success_url = reverse_lazy('kardex:prevision_list')
    permission_required = 'change_prevision'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Previsión actualizada correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Previsión'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class PrevisionDeleteView(DeleteView):
    model = Prevision
    template_name = 'kardex/prevision/confirm_delete.html'
    success_url = reverse_lazy('kardex:prevision_list')
    permission_required = 'delete_prevision'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Previsión eliminada correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la previsión: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Previsión'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
