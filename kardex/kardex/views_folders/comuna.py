import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView

from kardex.forms.comunas import FormComuna
from kardex.models import Comuna

MODULE_NAME = 'Comunas'


class ComunaListView(TemplateView):
    template_name = 'comuna/list.html'
    permission_required = 'view_comuna'

    def get(self, request, *args, **kwargs):
        # DataTables server-side
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_data(request)
        return super().get(request, *args, **kwargs)

    def get_datatable_data(self, request):
        qs = Comuna.objects.all()

        # Parámetros de DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 100))
        search_value = request.GET.get('search[value]', '').strip()

        # Búsqueda básica por texto en campos relevantes
        if search_value:
            qs = qs.filter(
                Q(nombre__icontains=search_value) |
                Q(codigo__icontains=search_value)
            )

        records_total = Comuna.objects.count()
        records_filtered = qs.count()

        # Ordenamiento
        # Mapa de índices de columnas a campos de modelo (coincide con columnas en template/JS)
        # 0: ID, 1: actions (ignorar), 2: Nombre, 3: Provincia, 4: Región
        column_map = ['id', None, 'nombre', 'codigo']
        try:
            order_col = int(request.GET.get('order[0][column]', 0))
        except (TypeError, ValueError):
            order_col = 0
        order_dir = request.GET.get('order[0][dir]', 'asc')
        order_field = column_map[order_col] if 0 <= order_col < len(column_map) else 'id'
        if not order_field:
            order_field = 'id'
        if order_dir == 'desc':
            order_field = f'-{order_field}'
        qs = qs.order_by(order_field)

        # Paginación
        qs_page = qs[start:start + length]

        # Construcción de filas
        data = []
        for obj in qs_page:
            edit_url = reverse_lazy('kardex:comuna_update', kwargs={'pk': obj.pk})
            delete_url = reverse_lazy('kardex:comuna_delete', kwargs={'pk': obj.pk})
            actions_html = f"""
                <a href=\"{edit_url}\" class=\"btn p-1 btn-sm btn-info\"><i class=\"fas fa-edit\"></i></a>
                <a href=\"{delete_url}\" class=\"btn p-1 btn-sm btn-danger\"><i class=\"fas fa-trash\"></i></a>
            """
            data.append({
                'ID': obj.id,
                'actions': actions_html,
                'Nombre': getattr(obj, 'nombre', ''),
                'Codigo': getattr(obj, 'codigo', ''),
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        })

    def post(self, request, *args, **kwargs):
        # Conservamos la compatibilidad si aún alguien llama al POST 'search'
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'search':
                data = []
                for i in Comuna.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Comunas'
        context['list_url'] = reverse_lazy('kardex:comuna_list')
        context['create_url'] = reverse_lazy('kardex:comuna_create')
        context['module_name'] = MODULE_NAME

        # Configuración DataTables específica para esta vista
        context['datatable_enabled'] = True
        context['datatable_page_length'] = 100  # 100 en 100
        context['datatable_order'] = [[0, 'asc']]
        context['columns'] = ['ID', 'Nombre', 'Codigo']

        # No necesitamos object_list para server-side
        return context


class ComunaCreateView(CreateView):
    template_name = 'comuna/form.html'
    model = Comuna
    form_class = FormComuna
    success_url = reverse_lazy('kardex:comuna_list')
    permission_required = 'add_comuna'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Comuna creada correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Comuna'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class ComunaUpdateView(UpdateView):
    template_name = 'comuna/form.html'
    model = Comuna
    form_class = FormComuna
    success_url = reverse_lazy('kardex:comuna_list')
    permission_required = 'change_comuna'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Comuna actualizada correctamente')
            return redirect(self.success_url)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Comuna'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class ComunaDeleteView(DeleteView):
    model = Comuna
    template_name = 'comuna/confirm_delete.html'
    success_url = reverse_lazy('kardex:comuna_list')
    permission_required = 'delete_comuna'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Comuna eliminada correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la comuna: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Comuna'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
