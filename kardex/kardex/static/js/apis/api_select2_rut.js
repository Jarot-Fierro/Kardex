$(document).ready(function () {
    const $rutField = $('#id_rut');
    if ($rutField.length === 0) return;

    // Modo edición (select): mantener Select2 con búsqueda por RUT
    if ($rutField.is('select')) {
        $rutField.select2({
            placeholder: 'Buscar por RUT',
            width: '100%',
            ajax: {
                url: 'http://127.0.0.1:8000/api/ingreso-paciente-ficha/',
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
            url: 'http://127.0.0.1:8000/api/ingreso-paciente-ficha/',
            method: 'GET',
            dataType: 'json',
            data: { search: rut, tipo: 'rut' },
            success: function (response) {
                const items = Array.isArray(response) ? response : (response.results || []);
                if (!items.length) {
                    // No se encontró ficha para el RUT ingresado
                    return;
                }
                const ficha = items[0];
                const paciente = (ficha.ingreso_paciente && ficha.ingreso_paciente.paciente) ? ficha.ingreso_paciente.paciente : (ficha.paciente || {});

                // Actualizar botones de carátula y stickers si existen
                if (ficha.id) {
                    const caratulaUrl = `/kardex/pdfs/ficha/${ficha.id}/`;
                    const stickersUrl = `/kardex/pdfs/stickers/ficha/${ficha.id}/`;
                    $('#btn-caratula').removeClass('disabled').attr('aria-disabled', 'false').attr('href', caratulaUrl);
                    $('#btn-stickers').removeClass('disabled').attr('aria-disabled', 'false').attr('href', stickersUrl);
                }

                // Sincronizar select de FICHA si existe
                if (ficha.id && (ficha.numero_ficha || ficha.numero_ficha_sistema)) {
                    const labelFicha = ficha.numero_ficha || ficha.numero_ficha_sistema || ficha.id;
                    const $fichaSel = $('#id_ficha');
                    if ($fichaSel.length && $fichaSel.is('select')) {
                        const opt = new Option(labelFicha, ficha.id, true, true);
                        $fichaSel.append(opt).trigger('change');
                    }
                }

                // Sincronizar select de CÓDIGO si existe en la respuesta
                if (paciente && paciente.codigo) {
                    const $codigoSel = $('#id_codigo');
                    if ($codigoSel.length && $codigoSel.is('select')) {
                        const opt = new Option(paciente.codigo, paciente.codigo, true, true);
                        $codigoSel.append(opt).trigger('change');
                    }
                }

                // Rellenar campos del formulario con datos del paciente
                if (paciente) {
                    try {
                        $('#nombre_paciente').val(paciente.nombre || '');
                        $('#apellido_paterno_paciente').val(paciente.apellido_paterno || '');
                        $('#apellido_materno_paciente').val(paciente.apellido_materno || '');
                        $('#id_rut_madre').val(paciente.rut_madre || '');
                        if (paciente.sexo !== undefined) $('#sexo_paciente').val(paciente.sexo).trigger('change');
                        if (paciente.estado_civil !== undefined) $('#estado_civil_paciente').val(paciente.estado_civil).trigger('change');
                        $('#nombres_padre_paciente').val(paciente.nombres_padre || '');
                        $('#nombres_madre_paciente').val(paciente.nombres_madre || '');
                        $('#nombre_pareja_paciente').val(paciente.nombre_pareja || '');
                        $('#direccion_paciente').val(paciente.direccion || '');
                        $('#numero_telefono1_paciente').val(paciente.numero_telefono1 || '');
                        $('#numero_telefono2_paciente').val(paciente.numero_telefono2 || '');
                        $('#pasaporte_paciente').val(paciente.pasaporte || '');
                        $('#nie_paciente').val(paciente.nie || '');
                        $('#rut_responsable_temporal_paciente').val(paciente.rut_responsable_temporal || '');
                        $('#usar_rut_madre_como_responsable_paciente').prop('checked', !!paciente.usar_rut_madre_como_responsable).trigger('change');
                        $('#recien_nacido_paciente').prop('checked', !!paciente.recien_nacido).trigger('change');
                        $('#extranjero_paciente').prop('checked', !!paciente.extranjero).trigger('change');
                        $('#fallecido_paciente').prop('checked', !!paciente.fallecido).trigger('change');
                        $('#fecha_fallecimiento_paciente').val(paciente.fecha_fallecimiento || '');
                        $('#ocupacion_paciente').val(paciente.ocupacion || '');
                        $('#representante_legal_paciente').val(paciente.representante_legal || '');
                        $('#nombre_social_paciente').val(paciente.nombre_social || '');
                        if (paciente.comuna !== undefined) $('#comuna_paciente').val(paciente.comuna).trigger('change');
                        if (paciente.prevision !== undefined) $('#prevision_paciente').val(paciente.prevision).trigger('change');
                        if (paciente.usuario !== undefined) $('#usuario_paciente').val(paciente.usuario).trigger('change');
                        if (paciente.fecha_nacimiento) {
                            const parts = String(paciente.fecha_nacimiento).split('T')[0].split('-');
                            if (parts.length === 3) {
                                const [year, month, day] = parts;
                                $('#id_fecha_nacimiento').val(`${day}/${month}/${year}`);
                            }
                        }
                    } catch (e) {
                        // No bloquear si algún campo no existe en este formulario
                    }
                }

                // Fechas de la ficha si vienen
                if (ficha.created_at) {
                    const d = ficha.created_at.split('T')[0].split('-');
                    if (d.length === 3) $('#ficha_created_at_text').text(`${d[2]}/${d[1]}/${d[0]}`);
                }
                if (ficha.updated_at) {
                    const d = ficha.updated_at.split('T')[0].split('-');
                    if (d.length === 3) $('#ficha_updated_at_text').text(`${d[2]}/${d[1]}/${d[0]}`);
                }

                // Aplicar reglas adicionales si existen
                if (window._pacienteApplyRules) {
                    try { window._pacienteApplyRules(); } catch (e) {}
                }
            },
            error: function () {
                // Silencioso: se puede agregar un toast si se requiere
            }
        });
    });
});