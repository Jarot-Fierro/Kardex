function cargarDatosFicha(fichaId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/ingreso-paciente-ficha/${fichaId}/`,
        method: 'GET',
        success: function (data) {
            const paciente = data.ingreso_paciente.paciente;

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
            // id_ficha: mostrar número de ficha del sistema y asegurar opción
            setSelectValue('#id_ficha', data.id, data.numero_ficha_sistema);

            // id_rut: mostrar RUT del paciente
            if (paciente.rut) {
                setSelectValue('#id_rut', data.id, paciente.rut);
            }

            // id_codigo: mostrar código del paciente
            if (paciente.codigo) {
                setSelectValue('#id_codigo', paciente.codigo, paciente.codigo);
            }

            $('#nombre_paciente').val(paciente.nombre);
            $('#apellido_paterno_paciente').val(paciente.apellido_paterno);
            $('#apellido_materno_paciente').val(paciente.apellido_materno);
            $('#id_rut_madre').val(paciente.rut_madre);
            $('#sexo_paciente').val(paciente.sexo).trigger('change');
            $('#estado_civil_paciente').val(paciente.estado_civil).trigger('change');
            $('#nombres_padre_paciente').val(paciente.nombres_padre);
            $('#nombres_madre_paciente').val(paciente.nombres_madre);
            $('#nombre_pareja_paciente').val(paciente.nombre_pareja);
            $('#direccion_paciente').val(paciente.direccion);
            $('#numero_telefono1_paciente').val(paciente.numero_telefono1);
            $('#numero_telefono2_paciente').val(paciente.numero_telefono2);
            $('#pasaporte_paciente').val(paciente.pasaporte);
            $('#nie_paciente').val(paciente.nie);
            $('#rut_responsable_temporal_paciente').val(paciente.rut_responsable_temporal);
            $('#usar_rut_madre_como_responsable_paciente').prop('checked', paciente.usar_rut_madre_como_responsable).trigger('change');
            $('#recien_nacido_paciente').prop('checked', paciente.recien_nacido).trigger('change');
            $('#extranjero_paciente').prop('checked', paciente.extranjero).trigger('change');
            $('#fallecido_paciente').prop('checked', paciente.fallecido).trigger('change');
            $('#fecha_fallecimiento_paciente').val(paciente.fecha_fallecimiento);
            $('#ocupacion_paciente').val(paciente.ocupacion);
            $('#representante_legal_paciente').val(paciente.representante_legal);
            $('#nombre_social_paciente').val(paciente.nombre_social);
            $('#comuna_paciente').val(paciente.comuna).trigger('change');
            $('#prevision_paciente').val(paciente.prevision).trigger('change');
            $('#usuario_paciente').val(paciente.usuario).trigger('change');

            if (paciente.fecha_nacimiento) {
                const [year, month, day] = paciente.fecha_nacimiento.split("-");
                $('#id_fecha_nacimiento').val(`${day}/${month}/${year}`);
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
