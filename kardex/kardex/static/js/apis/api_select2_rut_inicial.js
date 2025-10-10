$(document).ready(function () {
    // Tomamos el RUT y el código inicial desde inputs ocultos renderizados en el template
    const rutInicial = $('#rut_inicial').val();
    const codigoInicial = $('#codigo_inicial').val();

    if (rutInicial) {
        // Consumir API por RUT
        cargarPacientePorBusqueda(rutInicial, 'rut');
    } else if (codigoInicial) {
        // Consumir API por CÓDIGO si no hay RUT
        cargarPacientePorBusqueda(codigoInicial, 'codigo');
    }
});

// Función genérica para consumir la API por RUT o CÓDIGO
function cargarPacientePorBusqueda(valor, tipoBusqueda) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/ingreso-paciente-ficha/?search=${encodeURIComponent(valor)}&tipo=${tipoBusqueda}`,
        method: 'GET',
        success: function (response) {
            if (response && response.results && response.results.length > 0) {
                const ficha = response.results[0];
                const paciente = ficha.ingreso_paciente.paciente;

                // Actualizar botones de carátula y stickers
                const caratulaUrl = `/kardex/pdfs/ficha/${ficha.id}/`;
                const stickersUrl = `/kardex/pdfs/stickers/ficha/${ficha.id}/`;

                $('#btn-caratula')
                    .removeClass('disabled')
                    .attr('aria-disabled', 'false')
                    .attr('href', caratulaUrl);

                $('#btn-stickers')
                    .removeClass('disabled')
                    .attr('aria-disabled', 'false')
                    .attr('href', stickersUrl);

                // Sincronizar select2 de RUT si existe
                if (paciente.rut) {
                    const rutOption = new Option(paciente.rut, ficha.id, true, true);
                    $('#id_rut').append(rutOption).trigger('change');
                }

                // Sincronizar select2 de FICHA
                if (ficha.numero_ficha) {
                    const fichaOption = new Option(ficha.numero_ficha, ficha.id, true, true);
                    $('#id_ficha').append(fichaOption).trigger('change');
                }

                // Sincronizar select2 de CÓDIGO
                if (paciente.codigo) {
                    const codigoOption = new Option(paciente.codigo, paciente.codigo, true, true);
                    $('#id_codigo').append(codigoOption).trigger('change');
                }

                // Rellenar los campos del formulario
                rellenarCamposPaciente(paciente);

                // Fechas de creación y actualización de la ficha
                if (ficha.created_at) {
                    const [year, month, day] = ficha.created_at.split("T")[0].split("-");
                    $('#ficha_created_at_text').text(`${day}/${month}/${year}`);
                } else {
                    $('#ficha_created_at_text').text('-');
                }

                if (ficha.updated_at) {
                    const [year, month, day] = ficha.updated_at.split("T")[0].split("-");
                    $('#ficha_updated_at_text').text(`${day}/${month}/${year}`);
                } else {
                    $('#ficha_updated_at_text').text('-');
                }
            }
        },
        error: function () {
            alert('Error al cargar los datos del paciente.');
        }
    });
}

// Función para rellenar los campos del formulario
function rellenarCamposPaciente(paciente) {
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

    // Aplicar reglas adicionales si existen
    if (window._pacienteApplyRules) {
        window._pacienteApplyRules();
    }
}

// Eventos de select2
$('#id_ficha, #id_rut, #id_codigo').on('select2:select', function (e) {
    const fichaId = e.params.data.id;
    cargarDatosFicha(fichaId); // Se mantiene la función original para cargar ficha
});
