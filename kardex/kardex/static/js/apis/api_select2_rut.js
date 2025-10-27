
$(document).ready(function () {
    const $rutField = $('#id_rut');
    if ($rutField.length === 0) return;

    let lastRut = null;

    function normalizeRut(rut) {
        return String(rut || '').trim().toUpperCase();
    }

    // Evitar que ENTER envíe el formulario
    $rutField.on('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            return false;
        }
    });

    // Evento al salir del campo
    $rutField.on('blur', function () {
        const rut = normalizeRut($rutField.val());
        if (!rut || rut === lastRut) return;

        lastRut = rut;

        console.log('[rut_scan] Consultando RUT:', rut);

        $.ajax({
            url: '/api/ingreso-paciente-ficha/',
            type: 'GET',
            dataType: 'json',
            data: { search: rut, tipo: 'rut' },
            success: function (data) {
                console.log('[rut_scan] Respuesta API:', data);
                const items = Array.isArray(data) ? data : (data.results || []);
                if (items.length > 0) {
                    const first = items[0];
                    if (first && typeof first.id !== 'undefined') {
                        console.log('[rut_scan] Cargando ficha:', first.id);
                        if (typeof window.cargarDatosFicha === 'function') {
                            window.cargarDatosFicha(first.id);
                        }
                    }
                } else {
                    console.log('[rut_scan] No se encontró ficha para RUT:', rut);
                }
            },
            error: function (xhr, status, error) {
                console.error('[rut_scan] Error en AJAX:', status, error);
            }
        });
    });
});
