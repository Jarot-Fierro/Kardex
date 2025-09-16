from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView


class BaseCRUDView(TemplateView, FormMixin, ProcessFormView):
    model = None
    form_class = None
    template_name = None
    success_url = None
    history_model = None
    pk_url_kwarg = 'pk'
    exclude_fields = None
    title = None

    active_url_name = None
    inactive_url_name = None
    update_url_name = None
    toggle_url_name = None
    history_url_name = None
    export_report_url_name = None

    def dispatch(self, request, *args, **kwargs):
        """Detecta si es create o update según pk"""
        pk = kwargs.get(self.pk_url_kwarg)
        self.object = get_object_or_404(self.model, pk=pk) if pk else None
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs['instance'] = self.object
        return kwargs

    def format_value(self, obj, field, pk_field_name):
        """Formatea el valor de un campo para mostrarlo en la plantilla"""
        value = getattr(obj, field.name)
        if field.name == pk_field_name:  # Si es la PK
            if hasattr(value, "hex"):  # UUID
                return f"{value.hex[-3:]}"
            return f"{str(value)[-3:]}"  # String u otro tipo

        # Manejar campos de tipo choices
        if hasattr(field, 'choices') and field.choices:
            # Intentar obtener el valor de display usando get_FOO_display
            display_method = f'get_{field.name}_display'
            if hasattr(obj, display_method):
                return getattr(obj, display_method)()

        return value

    def prepare_items_for_template(self, queryset, fields, pk_field_name):
        """Prepara los items para la plantilla"""
        items = []
        for obj in queryset:
            item = {
                'object': obj,
                'values': [self.format_value(obj, f, pk_field_name) for f in fields],
                'pk': getattr(obj, pk_field_name)
            }
            items.append(item)
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_widgets = self.model.objects.filter(status__in=['ACTIVE', 'INACTIVE'])

        # Detectar el campo PK automáticamente
        pk_field_name = self.model._meta.pk.name

        # Excluir campos (si no está definido, lo dejamos como lista vacía)
        exclude = self.exclude_fields or []
        fields = [f for f in self.model._meta.fields if f.name not in exclude]

        # Preparar objetos completos para la plantilla
        objects = list(self.get_queryset())

        # Encabezados y filas
        context['columns'] = [f.verbose_name for f in fields]

        # Crear una estructura de datos que incluya tanto los valores formateados como el objeto original
        context['items'] = self.prepare_items_for_template(objects, fields, pk_field_name)

        # URLs dinámicas para la plantilla
        model_name = self.model._meta.model_name
        context['active_url_name'] = self.active_url_name or f'inventory:{model_name}_active'
        context['inactive_url_name'] = self.inactive_url_name or f'inventory:{model_name}_inactive'
        context['update_url_name'] = self.update_url_name or f'inventory:{model_name}_update'
        context['toggle_url_name'] = self.toggle_url_name or f'inventory:{model_name}_toggle_status'
        context['history_url_name'] = self.history_url_name or f'inventory:{model_name}_history'
        context['export_report_url_name'] = self.export_report_url_name

        # Conteos optimizados
        counts = queryset_widgets.aggregate(
            total=Count(pk_field_name),
            activos=Count(pk_field_name, filter=Q(status='ACTIVE')),
            inactivos=Count(pk_field_name, filter=Q(status='INACTIVE'))
        )

        context['object'] = self.object
        context['title'] = self.title
        context['total'] = counts['total']
        context['actives'] = counts['activos']
        context['inactives'] = counts['inactivos']
        return context

    def get(self, request, *args, **kwargs):
        form = self.get_form()  # aquí ya respeta self.object si es update
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = self.get_context_data(form=form, object=self.object)
            return render(request, 'crud/includes/crud_form.html', context)

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            action = 'update' if self.object else 'create'
            if action == 'update' and not form.has_changed():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'No hubo cambios en el registro',
                        'level': 'info'
                    })
                messages.info(request, 'No hubo cambios en el registro')
                return redirect(self.success_url)

            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Registro {action} correctamente',
                    'level': 'success'
                })
            messages.success(request, f'Registro {action} correctamente')
            return redirect(self.success_url)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                    'message': 'Hay errores en el formulario',
                    'level': 'error'
                })

        messages.error(request, 'Hay errores en el formulario')
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))


#
# class HistoryBase(ListView):
#     model = None
#     history_model = None
#     template_name = 'crud/history.html'
#     context_object_name = 'history_records'
#     pk_url_kwarg = 'pk'
#
#     def get_queryset(self):
#         if not self.model or not hasattr(self.model, 'history'):
#             return []
#
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         if not pk:
#             return []
#
#         if not self.history_model:
#             self.history_model = self.model.history.model
#
#         pk_field = self.model._meta.pk.name
#         filter_kwargs = {pk_field: pk}
#         history_records = list(self.history_model.objects.filter(**filter_kwargs).order_by('-history_date'))
#
#         for i, record in enumerate(history_records):
#             if i < len(history_records) - 1 and record.history_type == '~':
#                 previous_record = history_records[i + 1]
#
#                 def get_changes(current=record, previous=previous_record):
#                     return {'changes': self._get_changes(current, previous)}
#
#                 record.diff_against = get_changes
#
#         return history_records
#
#     def _get_changes(self, new_record, old_record):
#         changes = {}
#         skip_fields = ['history_id', 'history_date', 'history_change_reason',
#                        'history_type', 'history_user_id', 'id', 'updated_at']
#
#         for field in new_record._meta.fields:
#             field_name = field.name
#             if field_name in skip_fields:
#                 continue
#
#             old_value = getattr(old_record, field_name)
#             new_value = getattr(new_record, field_name)
#
#             if old_value != new_value:
#                 verbose_name = field_name
#                 try:
#                     model_field = self.model._meta.get_field(field_name)
#                     verbose_name = model_field.verbose_name
#                 except:
#                     pass
#
#                 changes[verbose_name] = {
#                     'old': old_value,
#                     'new': new_value
#                 }
#
#         return changes
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get(self.pk_url_kwarg)
#
#         if pk and self.model:
#             # Get the current object
#             context['object'] = get_object_or_404(self.model, pk=pk)
#             context['model_name'] = self.model._meta.verbose_name
#             context['model_name_plural'] = self.model._meta.verbose_name_plural
#
#             # Add URLs for navigation
#             model_name = self.model._meta.model_name
#             context['active_url_name'] = f'inventory:{model_name}_active'
#             context['title'] = getattr(self, 'title', f'Historial de {context["model_name"]}')
#
#         return context


class BaseToggleStatusView(View):
    model = None
    success_url_active = None
    success_url_inactive = None

    def get_toggle_url_name(self):
        """Obtiene el nombre de la URL para el toggle de estado"""
        model_name = self.model._meta.model_name
        return f'inventory:{model_name}_toggle_status'

    def get_success_url(self, status=None):
        model_name = self.model._meta.model_name

        if status == 'ACTIVE' and self.success_url_active:
            return self.success_url_active
        elif status == 'INACTIVE' and self.success_url_inactive:
            return self.success_url_inactive

        # URL por defecto
        return reverse_lazy(f'inventory:{model_name}_active')

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        if getattr(obj, 'status', None) not in ['ACTIVE', 'INACTIVE']:
            messages.error(request, 'Estado inválido')
            return redirect(self.get_success_url() or '/')

        # Cambiar estado
        new_status = 'INACTIVE' if obj.status == 'ACTIVE' else 'ACTIVE'
        obj.status = new_status
        obj.save(update_fields=['status', 'updated_at'])

        messages.success(request, 'Estado actualizado correctamente')
        return redirect(self.get_success_url(new_status))
