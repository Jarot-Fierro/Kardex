function cargarDatosFicha(fichaId) {
    function setSelectValue(selector, value, label) {
        if (value === null || value === undefined || value === '') return;
        const $el = $(selector);
        if ($el.length === 0) return;
        const valStr = String(value);
        // Si no existe la opción, agregarla (compatible con select2)
        if ($el.find(`option[value="${valStr}"]`).length === 0) {
            const text = (label !== undefined && label !== null && label !== '') ? String(label) : valStr;
            const newOpt = new Option(text, valStr, true, true);
            $el.append(newOpt);
        }
        $el.val(valStr).trigger('change');
    }
    $.ajax({
        url: `http://127.0.0.1:8000/api/ingreso-paciente-ficha/${fichaId}/`,
        method: 'GET',
        success: function (data) {
            const paciente = data.paciente.paciente;

            const caratulaUrl = `/kardex/pdfs/ficha/${data.id}/`;
            const stickersUrl = `/kardex/pdfs/stickers/ficha/${data.id}/`;

            $('#btn-caratula')
                .removeClass('disabled')
                .attr('aria-disabled', 'false')
                .attr('href', caratulaUrl);

            $('#btn-stickers')
                .removeClass('disabled')
                .attr('aria-disabled', 'false')
                .attr('href', stickersUrl);

            // --- Sincronizar los campos select2 ---
            const fichaOption = new Option(data.numero_ficha, data.id, true, true);
            $('#id_ficha').append(fichaOption).trigger('change');

            if (paciente.rut) {
                const rutOption = new Option(paciente.rut, data.id, true, true);
                $('#id_rut').append(rutOption).trigger('change');
            }

            if (paciente.codigo) {
                const codigoOption = new Option(paciente.codigo, data.id, true, true);
                $('#id_codigo').append(codigoOption).trigger('change');
            }

            $('#nombre_paciente').val(paciente.nombre);
            $('#apellido_paterno_paciente').val(paciente.apellido_paterno);
            $('#apellido_materno_paciente').val(paciente.apellido_materno);
            $('#id_rut_madre').val(paciente.rut_madre);
            setSelectValue('#sexo_paciente', paciente.sexo);
            setSelectValue('#estado_civil_paciente', paciente.estado_civil);
            $('#nombres_padre_paciente').val(paciente.nombres_padre);
            $('#nombres_madre_paciente').val(paciente.nombres_madre);
            $('#nombre_pareja_paciente').val(paciente.nombre_pareja);
            $('#direccion_paciente').val(paciente.direccion);
            $('#numero_telefono1_paciente').val(paciente.numero_telefono1);
            $('#numero_telefono2_paciente').val(paciente.numero_telefono2);
            $('#pasaporte_paciente').val(paciente.pasaporte);
            $('#nip_paciente').val(paciente.nip);
            $('#rut_responsable_temporal_paciente').val(paciente.rut_responsable_temporal);
            $('#usar_rut_madre_como_responsable_paciente').prop('checked', paciente.usar_rut_madre_como_responsable).trigger('change');
            $('#recien_nacido_paciente').prop('checked', paciente.recien_nacido).trigger('change');
            $('#extranjero_paciente').prop('checked', paciente.extranjero).trigger('change');
            $('#fallecido_paciente').prop('checked', paciente.fallecido).trigger('change');
            // Normaliza fecha de fallecimiento si viene en ISO
            if (paciente.fecha_fallecimiento) {
                const isoFal = String(paciente.fecha_fallecimiento);
                const partsFal = isoFal.includes('T') ? isoFal.split('T')[0].split('-') : isoFal.split('-');
                if (partsFal.length === 3) {
                    const [y, m, d] = partsFal;
                    $('#fecha_fallecimiento_paciente').val(`${d}/${m}/${y}`).trigger('change');
                } else {
                    $('#fecha_fallecimiento_paciente').val(paciente.fecha_fallecimiento).trigger('change');
                }
            } else {
                $('#fecha_fallecimiento_paciente').val('');
            }
            $('#ocupacion_paciente').val(paciente.ocupacion);
            $('#representante_legal_paciente').val(paciente.representante_legal);
            $('#nombre_social_paciente').val(paciente.nombre_social);
            setSelectValue('#comuna_paciente', paciente.comuna);
            setSelectValue('#genero_paciente', paciente.genero);
            setSelectValue('#id_genero', paciente.genero);
            setSelectValue('#prevision_paciente', paciente.prevision);
            setSelectValue('#usuario_paciente', paciente.usuario);

            if (paciente.fecha_nacimiento) {
                // Normaliza a dd/mm/yyyy para widgets con formato texto y sincroniza posibles IDs
                const iso = String(paciente.fecha_nacimiento);
                const parts = iso.includes('T') ? iso.split('T')[0].split('-') : iso.split('-');
                if (parts.length === 3) {
                    const [year, month, day] = parts;
                    const ddmmyyyy = `${day}/${month}/${year}`;
                    // Form principal: en plantillas el for apunta a fecha_nacimiento_paciente
                    $('#fecha_nacimiento_paciente').val(ddmmyyyy).trigger('change');
                    // Fallback para algunos templates previos
                    $('#id_fecha_nacimiento').val(ddmmyyyy).trigger('change');
                }
            }

            if (data.created_at) {
            const [year, month, day] = data.created_at.split("T")[0].split("-");
            $('#ficha_created_at_text').text(`${day}/${month}/${year}`);
            } else {
                $('#ficha_created_at_text').text('-');
            }

            if (data.updated_at) {
                const [year, month, day] = data.updated_at.split("T")[0].split("-");
                $('#ficha_updated_at_text').text(`${day}/${month}/${year}`);
            } else {
                $('#ficha_updated_at_text').text('-');
            }
            if (data.codigo) {
                const newOption = new Option(data.codigo, data.codigo, true, true);
                $('#id_codigo').append(newOption).trigger('change');
            }

            // Aplicar reglas de negocio si existen
            if (window._pacienteApplyRules) {
                window._pacienteApplyRules();
            }
        },
        error: function () {
            alert('Error al cargar los datos de la ficha.');
        }
    });
}

// Aplica a los 3 campos
$('#id_ficha, #id_rut, #id_codigo').on('select2:select', function (e) {
    const fichaId = e.params.data.id;
    cargarDatosFicha(fichaId);
});
