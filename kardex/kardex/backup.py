# class ComunaListView(TemplateView):
#     template_name = 'kardex/comuna/list.html'
#     permission_required = 'view_comuna'
#
#     def get(self, request, *args, **kwargs):
#         # DataTables server-side
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
#             return self.get_datatable_data(request)
#         return super().get(request, *args, **kwargs)
#
#     def get_datatable_data(self, request):
#         qs = Comuna.objects.all()
#
#         # Parámetros de DataTables
#         draw = int(request.GET.get('draw', 1))
#         start = int(request.GET.get('start', 0))
#         length = int(request.GET.get('length', 100))
#         search_value = request.GET.get('search[value]', '').strip()
#
#         # Búsqueda básica por texto en campos relevantes
#         if search_value:
#             qs = qs.filter(
#                 Q(nombre__icontains=search_value) |
#                 Q(codigo__icontains=search_value)
#             )
#
#         records_total = Comuna.objects.count()
#         records_filtered = qs.count()
#
#         # Ordenamiento
#         # Mapa de índices de columnas a campos de modelo (coincide con columnas en template/JS)
#         # 0: ID, 1: actions (ignorar), 2: Nombre, 3: Provincia, 4: Región
#         column_map = ['id', None, 'nombre', 'codigo']
#         try:
#             order_col = int(request.GET.get('order[0][column]', 0))
#         except (TypeError, ValueError):
#             order_col = 0
#         order_dir = request.GET.get('order[0][dir]', 'asc')
#         order_field = column_map[order_col] if 0 <= order_col < len(column_map) else 'id'
#         if not order_field:
#             order_field = 'id'
#         if order_dir == 'desc':
#             order_field = f'-{order_field}'
#         qs = qs.order_by(order_field)
#
#         # Paginación
#         qs_page = qs[start:start + length]
#
#         # Construcción de filas
#         data = []
#         for obj in qs_page:
#             edit_url = reverse_lazy('kardex:comuna_update', kwargs={'pk': obj.pk})
#             delete_url = reverse_lazy('kardex:comuna_delete', kwargs={'pk': obj.pk})
#             view_url = reverse_lazy('kardex:comuna_detail', kwargs={'pk': obj.pk})
#             actions_html = f"""
#                 <a href=\"{view_url}\" class=\"btn p-1 btn-sm btn-secondary view-btn\" title=\"Ver detalle\"><i class=\"fas fa-search\"></i></a>
#                 <a href=\"{edit_url}\" class=\"btn p-1 btn-sm btn-info\"><i class=\"fas fa-edit\"></i></a>
#                 <a href=\"{delete_url}\" class=\"btn p-1 btn-sm btn-danger\"><i class=\"fas fa-trash\"></i></a>
#             """
#             data.append({
#                 'ID': obj.id,
#                 'actions': actions_html,
#                 'Nombre': getattr(obj, 'nombre', ''),
#                 'Codigo': getattr(obj, 'codigo', ''),
#             })
#
#         return JsonResponse({
#             'draw': draw,
#             'recordsTotal': records_total,
#             'recordsFiltered': records_filtered,
#             'data': data,
#         })
#
#     def post(self, request, *args, **kwargs):
#         # Conservamos la compatibilidad si aún alguien llama al POST 'search'
#         data = {}
#         action = request.POST.get('action')
#         try:
#             if action == 'search':
#                 data = []
#                 for i in Comuna.objects.all():
#                     data.append(i.toJSON())
#             else:
#                 data['error'] = 'No ha seleccionado ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return HttpResponse(json.dumps(data), content_type='application/json')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listado de Comunas'
#         context['list_url'] = reverse_lazy('kardex:comuna_list')
#         context['create_url'] = reverse_lazy('kardex:comuna_create')
#         context['module_name'] = MODULE_NAME
#
#         # Configuración DataTables específica para esta vista
#         context['datatable_enabled'] = True
#         context['datatable_page_length'] = 100  # 100 en 100
#         context['datatable_order'] = [[0, 'asc']]
#         context['columns'] = ['ID', 'Nombre', 'Codigo']
#
#         # No necesitamos object_list para server-side
#         return context
