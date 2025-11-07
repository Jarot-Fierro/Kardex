from kardex.models import *
from .fields_export_csv import *
from .utils import export_queryset_to_excel, export_queryset_to_excel_advance, export_queryset_to_csv_fast


def export_comuna(request):
    queryset = Comuna.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='comunas')


def export_establecimiento(request):
    queryset = Establecimiento.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='establecimientos')


def export_ficha(request):
    queryset = Ficha.objects.filter(
        establecimiento=request.user.establecimiento
    )
    return export_queryset_to_excel_advance(queryset, filename='fichas')


def export_ficha_csv(request):
    queryset = Paciente.objects.filter(
        establecimiento=request.user.establecimiento
    )
    return export_queryset_to_csv_fast(queryset, filename='fichas', fields=fields_ficha_csv)


def export_ficha_pasivadas_csv(request):
    queryset = Paciente.objects.filter(
        establecimiento=request.user.establecimiento, pasivado=True
    )
    return export_queryset_to_csv_fast(queryset, filename='fichas', fields=fields_ficha_csv)


def export_movimiento_ficha(request):
    queryset = MovimientoFicha.objects.filter(ficha__establecimiento=request.user.establecimiento).order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='movimientos_ficha')


def export_movimiento_ficha_envio(request):
    queryset = MovimientoFicha.objects.filter(ficha__establecimiento=request.user.establecimiento,
                                              estado_envio='ENVIADO').order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='movimientos_ficha_enviadas')


def export_movimiento_ficha_recepcion(request):
    queryset = MovimientoFicha.objects.filter(ficha__establecimiento=request.user.establecimiento,
                                              estado_recepcion='RECIBIDO').order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='movimientos_ficha_recepcionadas')


def export_movimiento_ficha_traspaso(request):
    queryset = MovimientoFicha.objects.filter(ficha__establecimiento=request.user.establecimiento,
                                              estado_traspaso='TRASPASDO').order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='movimientos_ficha_traspasadas')


## CSV
def export_paciente_csv(request):
    queryset = Paciente.objects.all()
    return export_queryset_to_csv_fast(queryset, filename='pacientes', fields=fields_paciente_csv)


def export_paciente_recien_nacido_csv(request):
    queryset = Paciente.objects.filter(recien_nacido=True)
    return export_queryset_to_csv_fast(queryset, filename='pacientes_recien_nacidos_csv', fields=fields_paciente_csv)


def export_paciente_extranjero_csv(request):
    queryset = Paciente.objects.filter(extranjero=True)
    return export_queryset_to_csv_fast(queryset, filename='pacientes_extranjeros_csv', fields=fields_paciente_csv)


def export_paciente_fallecido_csv(request):
    queryset = Paciente.objects.filter(fallecido=True)
    return export_queryset_to_csv_fast(queryset, filename='pacientes_fallecids_csv', fields=fields_paciente_csv)


def export_paciente_pueblo_indigena_csv(request):
    queryset = Paciente.objects.filter(pueblo_indigena=True)
    return export_queryset_to_csv_fast(queryset, filename='pacientes_pueblo_indigena_csv', fields=fields_paciente_csv)


## TERMINO

def export_pais(request):
    queryset = Pais.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='paises')


def export_prevision(request):
    queryset = Prevision.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='previsiones')


def export_profesion(request):
    queryset = Profesion.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='profesiones')


def export_profesional(request):
    queryset = Profesional.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='profesionales')


def export_sector(request):
    queryset = Sector.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='sectores')


def export_servicio_clinico(request):
    queryset = ServicioClinico.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='servicios_clinicos')
