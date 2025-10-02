import base64
from io import BytesIO

import barcode
from barcode.writer import ImageWriter
from django.shortcuts import render, get_object_or_404

from kardex.models import Paciente


def pdf_index(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    codigo_barras_base64 = generar_barcode_base64(paciente.codigo)

    context = {
        'paciente': paciente,
        'codigo_barras_base64': codigo_barras_base64
    }

    return render(request, 'pdfs/formato_caratula.html', context)


def generar_barcode_base64(codigo_paciente: str) -> str:
    buffer = BytesIO()
    codigo = barcode.get('code128', codigo_paciente, writer=ImageWriter())
    codigo.write(buffer, options={
        "module_height": 10.0,
        "font_size": 10,
        "quiet_zone": 1
    })

    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{base64_img}"


def pdf_index(request):
    return render(request, 'pdfs/formato_caratula.html')
