from inventory.models import *
from .utils import export_queryset_to_excel, export_extended_queryset_to_excel


def export_brand(request):
    queryset = Brand.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='marcas')


def export_category(request):
    queryset = Category.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='categorias')


def export_subcategory(request):
    queryset = SubCategory.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='subcategorias')


def export_model(request):
    queryset = Model.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='modelos')


def export_leadership(request):
    queryset = Leadership.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='lideres')


def export_operative_system(request):
    queryset = OperativeSystem.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='sistemas_operativos')


def export_device_owner(request):
    queryset = DeviceOwner.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='propietarios_dispositivos')


def export_plan(request):
    queryset = Plan.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='planes')


def export_chip(request):
    queryset = Chip.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='chips')


def export_official(request):
    queryset = Official.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='funcionarios')


def export_phone(request):
    queryset = Phone.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='telefonos')


def export_licence_os(request):
    queryset = LicenceOs.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='licencias_sistemas')


def export_microsoft_office(request):
    queryset = MicrosoftOffice.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='microsoft_office')


def export_computer(request):
    queryset = Computer.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='computadores')


def export_inks(request):
    queryset = Inks.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tintas')


def export_printer(request):
    queryset = Printer.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='impresoras')


def export_article(request):
    queryset = Article.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='articulos')


def export_establishment(request):
    queryset = Establishment.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='establecimientos')


def export_departament(request):
    queryset = Departament.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='departamentos')


def export_transaction_entry(request):
    queryset = Transaction.objects.filter(type='ENTRY').select_related().order_by('-updated_at')

    fields = [
        ('Código', 'code'),
        ('Tipo', 'type'),
        ('Observación', 'observation'),
        ('Estado', 'status'),
        ('Funcionario', 'official'),
        ('Usuario', 'login_user__username'),
        ('Fecha Creación', 'created_at'),
    ]

    return export_extended_queryset_to_excel(queryset, fields, filename='transacciones_entrada')


def export_transaction_output(request):
    queryset = Transaction.objects.filter(type='OUTPUT').select_related(
        'output_info', 'official', 'login_user'
    ).order_by('-updated_at')

    fields = [
        ('Código', 'code'),
        ('Tipo Salida', 'output_info__type_output'),
        ('Fecha Devolución', 'output_info__return_date'),
        ('Estado Salida', 'output_info__status'),
        ('Observación', 'observation'),
        ('Estado Transacción', 'status'),
        ('Funcionario', 'official'),
        ('Usuario', 'login_user__username'),
        ('Fecha Creación', 'created_at'),
    ]

    return export_extended_queryset_to_excel(queryset, fields, filename='transacciones_salida')


def export_transaction_support(request):
    queryset = Transaction.objects.filter(type='SUPPORT').select_related(
        'support_info', 'official', 'login_user'
    ).order_by('-updated_at')

    fields = [
        ('Código', 'code'),
        ('Tipo Soporte', 'support_info__type_soporte__name'),
        ('Problema', 'support_info__problem'),
        ('Solución', 'support_info__solution'),
        ('Fecha Inicio', 'support_info__date_start'),
        ('Fecha Fin', 'support_info__date_end'),
        ('Estado Soporte', 'support_info__status'),
        ('Observación', 'observation'),
        ('Estado Transacción', 'status'),
        ('Funcionario', 'official'),
        ('Usuario', 'login_user__username'),
        ('Fecha Creación', 'created_at'),
    ]

    return export_extended_queryset_to_excel(queryset, fields, filename='transacciones_soporte')
