import base64
from io import BytesIO

import barcode
from barcode.writer import ImageWriter
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from kardex.models import Ficha
from kardex.models import Paciente


@permission_required('kardex.view_paciente', raise_exception=True)
def pdf_index(request, ficha_id=None, paciente_id=None):
    ficha = None
    ingreso = None

    if ficha_id is not None:
        ficha = get_object_or_404(Ficha, id=ficha_id)
        ingreso = ficha.ingreso_paciente
        paciente = ingreso.paciente
    elif paciente_id is not None:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        # Obtener la ficha asociada al ingreso del establecimiento del usuario logueado
        establecimiento = getattr(request.user, 'establecimiento', None)
        if establecimiento is None:
            raise Http404("El usuario no tiene un establecimiento asociado")
        ficha = Ficha.objects.filter(
            ingreso_paciente__paciente=paciente,
            ingreso_paciente__establecimiento=establecimiento
        ).first()
        if ficha is None:
            raise Http404("El paciente no tiene una ficha asociada para el establecimiento del usuario")
        ingreso = ficha.ingreso_paciente
    else:
        # Si no se proporciona ningún ID, retornar 404
        raise Http404("Se requiere ficha")

    # Generar código de barras basado en el número de ficha (zero-padded a 4 dígitos)
    numero_ficha_str = str(ficha.numero_ficha or '').zfill(4)
    codigo_barras_base64 = generar_barcode_base64(numero_ficha_str)

    context = {
        'paciente': paciente,
        'ficha': ficha,
        'ingreso': ingreso,
        'codigo_barras_base64': codigo_barras_base64
    }

    return render(request, 'pdfs/formato_caratula.html', context)


@permission_required('kardex.view_paciente', raise_exception=True)
def pdf_stickers(request, ficha_id=None, paciente_id=None):
    ficha = None
    ingreso = None

    if ficha_id is not None:
        ficha = get_object_or_404(Ficha, id=ficha_id)
        ingreso = ficha.ingreso_paciente
        paciente = ingreso.paciente
    elif paciente_id is not None:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        # Obtener la ficha asociada al ingreso del establecimiento del usuario logueado
        establecimiento = getattr(request.user, 'establecimiento', None)
        if establecimiento is None:
            raise Http404("El usuario no tiene un establecimiento asociado")
        ficha = Ficha.objects.filter(
            ingreso_paciente__paciente=paciente,
            ingreso_paciente__establecimiento=establecimiento
        ).first()
        if ficha is None:
            raise Http404("El paciente no tiene una ficha asociada para el establecimiento del usuario")
        ingreso = ficha.ingreso_paciente
    else:
        # Si no se proporciona ningún ID, retornar 404
        raise Http404("Se requiere ficha")

    # Generar código de barras basado en el número de ficha (zero-padded a 4 dígitos)
    numero_ficha_str = str(ficha.numero_ficha or '').zfill(4)
    codigo_barras_base64 = generar_barcode_base64(numero_ficha_str)

    context = {
        'paciente': paciente,
        'ficha': ficha,
        'ingreso': ingreso,
        'codigo_barras_base64': codigo_barras_base64,
        'sticker_range': range(24)

    }

    return render(request, 'pdfs/formato_stickers.html', context)


def generar_barcode_base64(codigo_paciente: str) -> str:
    buffer = BytesIO()
    codigo = barcode.get('code128', codigo_paciente, writer=ImageWriter())
    codigo.write(buffer, options={
        "module_height": 10.0,
        "font_size": 10,
        "quiet_zone": 1,
        "write_text": False,
    })

    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{base64_img}"
