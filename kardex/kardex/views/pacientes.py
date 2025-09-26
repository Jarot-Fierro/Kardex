from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.pacientes import FormPaciente
from kardex.mixin import DataTableMixin
from kardex.models import Paciente

MODULE_NAME = 'Pacientes'


class PacienteListView(DataTableMixin, TemplateView):
    template_name = 'kardex/paciente/list.html'
    model = Paciente
    datatable_columns = ['ID', 'RUT', 'Nombre', 'Sexo', 'Estado Civil', 'Comuna', 'Previsión']
    datatable_order_fields = [
        'id',
        None,
        None,
        'sexo',
        'estado_civil',
        'comuna__nombre',
        'prevision__nombre'
    ]

    datatable_search_fields = [
        'rut__icontains',
        'nombre__icontains',
        'apellido_paterno__icontains',
        'apellido_materno__icontains',
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    url_detail = 'kardex:paciente_detail'
    url_update = 'kardex:paciente_update'
    url_delete = 'kardex:paciente_delete'

    def render_row(self, obj):
        nombre_completo = f"{(obj.nombre or '').upper()} {(obj.apellido_paterno or '').upper()} {(obj.apellido_materno or '').upper()}".strip()
        return {
            'ID': obj.id,
            'RUT': obj.rut,
            'Nombre': nombre_completo,
            'Sexo': obj.sexo or '',
            'Estado Civil': obj.estado_civil or '',
            'Comuna': (getattr(obj.comuna, 'nombre', '') or '').upper(),
            'Previsión': (getattr(obj.prevision, 'nombre', '') or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Pacientes',
            'list_url': reverse_lazy('kardex:paciente_list'),
            'create_url': reverse_lazy('kardex:paciente_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'kardex/paciente/detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class PacienteCreateView(CreateView):
    template_name = 'kardex/paciente/form.html'
    model = Paciente
    form_class = FormPaciente
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'add_paciente'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado correctamente')
            return redirect(self.success_url)
        messages.error(request, 'Hay errores en el formulario')
        print(form.errors)
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class PacienteUpdateView(UpdateView):
    template_name = 'kardex/paciente/form.html'
    model = Paciente
    form_class = FormPaciente
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'change_paciente'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado correctamente')
            return redirect(self.success_url)
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'kardex/paciente/confirm_delete.html'
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'delete_paciente'

    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Paciente eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el paciente: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Paciente'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
