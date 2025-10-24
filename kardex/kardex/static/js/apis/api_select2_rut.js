$(document).ready(function () {
    const $rutField = $('#id_rut');
    if ($rutField.length === 0) return;

    // Modo edición (select): mantener Select2 con búsqueda por RUT
    if ($rutField.is('select')) {
        $rutField.select2({
            placeholder: 'Buscar por RUT',
            width: '100%',
            ajax: {
                url: 'http://10.8.85.141:8000/api/ingreso-paciente-ficha/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        search: params.term,
                        tipo: 'rut'
                    };
                },
                processResults: function (data) {
                    const items = Array.isArray(data) ? data : (data.results || []);
                    return {
                        results: items.map(item => ({
                            id: item.id,
                            text: item.paciente && item.paciente.rut ? item.paciente.rut : 'Sin RUT'
                        }))
                    };
                }
            },
            minimumInputLength: 1
        });
        return;
    }

    // Modo creación (input): consumir API al perder foco (blur)
    let lastQueriedRut = null;
    $rutField.on('blur', function () {
        const rut = ($rutField.val() || '').trim();
        if (!rut) return;
        if (rut === lastQueriedRut) return; // evita consultas repetidas innecesarias
        lastQueriedRut = rut;

        $.ajax({
            url: 'http://10.8.85.141:8000/api/ingreso-paciente-ficha/',
            method: 'GET',
            dataType: 'json',
            data: { search: rut, tipo: 'rut' },
            success: function (response) {
                const items = Array.isArray(response) ? response : (response.results || []);
                if (!items.length) return;
                const ficha = items[0];
                if (window.cargarDatosFicha && ficha && ficha.id) {
                    try { window.cargarDatosFicha(ficha.id); } catch (e) {}
                }
            },
            error: function () {
                // Silencioso: se puede agregar un toast si se requiere
            }
        });
    });
});