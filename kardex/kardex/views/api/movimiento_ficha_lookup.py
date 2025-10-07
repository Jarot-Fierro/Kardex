from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from kardex.models import Paciente, Ficha


@login_required
@require_GET
def movimiento_ficha_lookup(request):
    """
    Lookup by rut or ficha number within current user's establishment.
    Returns: { ok, results: [ {rut, nombre_completo, numero_ficha} ] }
    If both rut and ficha provided, will try to resolve consistent match; otherwise return best candidates.
    """
    est = getattr(request.user, 'establecimiento', None)
    if est is None:
        return JsonResponse({'ok': False, 'error': 'Usuario sin establecimiento asociado'}, status=400)

    rut = (request.GET.get('rut') or '').strip()
    nf = (request.GET.get('ficha') or '').strip()

    results = []

    if rut:
        pacientes = Paciente.objects.filter(
            ingresopaciente__establecimiento=est,
            rut__iexact=rut
        ).distinct()
        for p in pacientes:
            ficha = (Ficha.objects
                     .filter(ingreso_paciente__establecimiento=est, ingreso_paciente__paciente=p)
                     .order_by('-id')
                     .first())
            results.append({
                'rut': p.rut,
                'nombre_completo': f"{p.nombre} {p.apellido_paterno} {p.apellido_materno}".strip(),
                'numero_ficha': ficha.numero_ficha if ficha else None,
                'ficha_id': ficha.id if ficha else None,
            })
    elif nf:
        fichas = Ficha.objects.filter(
            ingreso_paciente__establecimiento=est,
            numero_ficha=nf
        ).select_related('ingreso_paciente__paciente')
        for f in fichas:
            p = f.ingreso_paciente.paciente if f.ingreso_paciente else None
            results.append({
                'rut': getattr(p, 'rut', None),
                'nombre_completo': (
                    f"{getattr(p, 'nombre', '')} {getattr(p, 'apellido_paterno', '')} {getattr(p, 'apellido_materno', '')}").strip() if p else None,
                'numero_ficha': f.numero_ficha,
                'ficha_id': f.id,
            })

    return JsonResponse({'ok': True, 'results': results})
