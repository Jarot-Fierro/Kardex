from kardex.models import *
from .utils import export_queryset_to_excel, export_queryset_to_excel_advance


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


import pandas as pd
from django.http import HttpResponse


def export_ficha_fast(request):
    # Traemos solo los campos necesarios
    qs = Ficha.objects.filter(
        establecimiento=request.user.establecimiento
    ).values(
        'id', 'numero_ficha_sistema', 'numero_ficha_tarjeta', 'pasivado', 'observacion', 'usuario__username',
        'profesional__nombres', 'fecha_creacion_anterior', 'paciente__rut', 'sector__color',
        'establecimiento__nombre', 'updated_at'
    )

    df = pd.DataFrame.from_records(qs)

    # Convertir datetime con zona horaria a naive (compatible con Excel)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Si es tz-aware, lo hacemos naive
            if df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_convert(None)
            else:
                df[col] = df[col]

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fichas.xlsx'

    df.to_excel(response, index=False, engine='xlsxwriter')
    return response


def export_ficha_pasivada(request):
    queryset = Ficha.objects.filter(establecimiento=request.user.establecimiento, pasivado=True).order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='fichas_pasivadas')


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


def export_paciente(request):
    queryset = Paciente.objects.filter(establecimiento=request.user.establecimiento).order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='pacientes')


def export_paciente_recien_nacido(request):
    queryset = Paciente.objects.filter(establecimiento=request.user.establecimiento, recien_nacido=True).order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='pacientes_recien_nacidos')


def export_paciente_extranjero(request):
    queryset = Paciente.objects.filter(establecimiento=request.user.establecimiento, extranjero=True).order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='pacientes_extranjeros')


def export_paciente_fallecido(request):
    queryset = Paciente.objects.filter(establecimiento=request.user.establecimiento, fallecido=True).order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='pacientes_fallecidos')


def export_paciente_pueblo_indigena(request):
    queryset = Paciente.objects.filter(establecimiento=request.user.establecimiento, pueblo_indigena=True).order_by(
        '-updated_at')
    return export_queryset_to_excel(queryset, filename='pacientes_pueblo_indigenas')


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
