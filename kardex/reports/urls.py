from django.urls import path

from .views import *

app_name = 'reports'

urlpatterns = [
    # ---- MODELOS PRINCIPALES ---- #
    path('reportes/articulos/exportar-excel/', export_article, name='export_article'),
    path('reportes/marcas/exportar-excel/', export_brand, name='export_brand'),
    path('reportes/categorias/exportar-excel/', export_category, name='export_category'),
    path('reportes/subcategorias/exportar-excel/', export_subcategory, name='export_subcategory'),
    path('reportes/modelos/exportar-excel/', export_model, name='export_model'),
    path('reportes/lideres/exportar-excel/', export_leadership, name='export_leadership'),
    path('reportes/sistemas-operativos/exportar-excel/', export_operative_system, name='export_operative_system'),
    path('reportes/propietarios-dispositivos/exportar-excel/', export_device_owner, name='export_device_owner'),
    path('reportes/planes/exportar-excel/', export_plan, name='export_plan'),
    path('reportes/chips/exportar-excel/', export_chip, name='export_chip'),
    path('reportes/funcionarios/exportar-excel/', export_official, name='export_official'),
    path('reportes/telefonos/exportar-excel/', export_phone, name='export_phone'),
    path('reportes/licencias-sistemas/exportar-excel/', export_licence_os, name='export_licence_os'),
    path('reportes/microsoft-office/exportar-excel/', export_microsoft_office, name='export_microsoft_office'),
    path('reportes/computadores/exportar-excel/', export_computer, name='export_computer'),
    path('reportes/tintas/exportar-excel/', export_inks, name='export_inks'),
    path('reportes/impresoras/exportar-excel/', export_printer, name='export_printer'),
    path('reportes/establecimientos/exportar-excel/', export_establishment, name='export_establishment'),
    path('reportes/departamentos/exportar-excel/', export_departament, name='export_departament'),

    # -------- TRANSACCIONES------------#

    path('reportes/transacciones/entrada/exportar-excel/', export_transaction_entry, name='export_transaction_entry'),
    path('reportes/transacciones/salida/exportar-excel/', export_transaction_output, name='export_transaction_output'),
    path('reportes/transacciones/soporte/exportar-excel/', export_transaction_support,
         name='export_transaction_support'),

]
