from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.mixin import DataTableMixin
from kardex.models import MovimientoFicha

MODULE_NAME = 'Movimientos de Ficha'


class MovimientoFichaListView(DataTableMixin, TemplateView):
    template_name = 'kardex/movimiento_ficha/list.html'
    model = MovimientoFicha
    datatable_columns = ['ID', 'Ficha', 'Servicio Clínico', 'Estado', 'Fecha Movimiento']
    datatable_order_fields = ['id', None, 'ficha__numero_ficha', 'servicio_clinico__nombre', 'estado_respuesta', 'fecha_mov']
    datatable_search_fields = [
        'ficha__numero_ficha__icontains', 'servicio_clinico__nombre__icontains', 'estado_respuesta__icontains'
    ]

    url_detail = 'kardex:movimiento_ficha_detail'
    url_update = 'kardex:movimiento_ficha_update'
    url_delete = 'kardex:movimiento_ficha_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Ficha': getattr(obj.ficha, 'numero_ficha', '') if obj.ficha else '',
            'Servicio Clínico': (getattr(obj.servicio_clinico, 'nombre', '') or '').upper(),
            'Estado': obj.estado_respuesta,
            'Fecha Movimiento': obj.fecha_mov.strftime('%Y-%m-%d %H:%M') if obj.fecha_mov else '',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Movimientos de Ficha',
            'list_url': reverse_lazy('kardex:movimiento_ficha_list'),
            'create_url': reverse_lazy('kardex:movimiento_ficha_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class MovimientoFichaDetailView(DetailView):
    model = MovimientoFicha
    template_name = 'kardex/movimiento_ficha/detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class MovimientoFichaCreateView(CreateView):
    template_name = 'kardex/movimiento_ficha/form.html'
    model = MovimientoFicha
    fields = '__all__'
    success_url = reverse_lazy('kardex:movimiento_ficha_list')
    permission_required = 'add_movimientoficha'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Movimiento de ficha creado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Movimiento de Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class MovimientoFichaUpdateView(UpdateView):
    template_name = 'kardex/movimiento_ficha/form.html'
    model = MovimientoFicha
    fields = '__all__'
    success_url = reverse_lazy('kardex:movimiento_ficha_list')
    permission_required = 'change_movimientoficha'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Movimiento de ficha actualizado correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Movimiento de Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class MovimientoFichaDeleteView(DeleteView):
    model = MovimientoFicha
    template_name = 'kardex/movimiento_ficha/confirm_delete.html'
    success_url = reverse_lazy('kardex:movimiento_ficha_list')
    permission_required = 'delete_movimientoficha'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Movimiento de ficha eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el movimiento de ficha: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Movimiento de Ficha'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
