from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.fichas import FormFicha
from kardex.mixin import DataTableMixin
from kardex.models import Ficha

MODULE_NAME = 'Fichas'


class FichaListView(DataTableMixin, TemplateView):
    template_name = 'kardex/ficha/list.html'
    model = Ficha
    datatable_columns = ['ID', 'Número', 'Profesional', 'Usuario', 'Paciente', 'Fecha Movimiento']
    datatable_order_fields = ['id', None, 'numero_ficha', 'profesional__nombres', 'usuario__username', 'ingreso_paciente__paciente__rut', 'fecha_mov']
    datatable_search_fields = [
        'numero_ficha__icontains', 'profesional__nombres__icontains', 'usuario__username__icontains',
        'ingreso_paciente__paciente__rut__icontains'
    ]

    url_detail = 'kardex:ficha_detail'
    url_update = 'kardex:ficha_update'
    url_delete = 'kardex:ficha_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Número': obj.numero_ficha,
            'Profesional': (getattr(obj.profesional, 'nombres', '') or '').upper(),
            'Usuario': getattr(obj.usuario, 'username', '') or '',
            'Paciente': getattr(getattr(obj.ingreso_paciente, 'paciente', None), 'rut', '') or '',
            'Fecha Movimiento': obj.fecha_mov.strftime('%Y-%m-%d') if obj.fecha_mov else '',
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


class FichaDetailView(DetailView):
    model = Ficha
    template_name = 'kardex/ficha/detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class FichaCreateView(CreateView):
    template_name = 'kardex/ficha/form.html'
    model = Ficha
    form_class = FormFicha
    success_url = reverse_lazy('kardex:ficha_list')
    permission_required = 'add_ficha'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Ficha creada correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class FichaUpdateView(UpdateView):
    template_name = 'kardex/ficha/form.html'
    model = Ficha
    form_class = FormFicha
    success_url = reverse_lazy('kardex:ficha_list')
    permission_required = 'change_ficha'

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


class FichaDeleteView(DeleteView):
    model = Ficha
    template_name = 'kardex/ficha/confirm_delete.html'
    success_url = reverse_lazy('kardex:ficha_list')
    permission_required = 'delete_ficha'

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
