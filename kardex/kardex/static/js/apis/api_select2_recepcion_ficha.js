$(function () {
  // Inicializa select2 en el campo RUT del formulario de recepción
  const $rut = $('#id_rut');
  if (!$rut.length) return;

  $rut.select2({
    placeholder: 'Buscar por RUT',
    width: '100%',
    ajax: {
      url: '/api/recepcion-ficha/',
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return { search: params.term };
      },
      processResults: function (data) {
        const results = (data.results || []).map(item => {
          const paciente = (item.ficha && item.ficha.ingreso_paciente && item.ficha.ingreso_paciente.paciente) || {};
          const rut = paciente.rut || '';
          const nombre = `${paciente.nombre || ''} ${paciente.apellido_paterno || ''} ${paciente.apellido_materno || ''}`.trim();
          return {
            id: item.id,  // ID del movimiento (se usa para cargar detalles)
            text: `${rut} - ${nombre}`
          };
        });
        return { results };
      }
    },
    minimumInputLength: 1
  });

  // Cuando se selecciona un resultado, cargar y rellenar el formulario
  $rut.on('select2:select', function (e) {
    const movId = e.params.data.id;
    if (movId) llenarPorMovimiento(movId);
  });

  function llenarPorMovimiento(movId) {
    $.ajax({
      url: `/api/recepcion-ficha/${movId}/`,
      method: 'GET',
      success: function (data) {
        console.log('Datos recibidos en llenarPorMovimiento:', data);

        const f = data.ficha || {};
        const p = (f.ingreso_paciente && f.ingreso_paciente.paciente) || {};

        const nombreCompleto = `${p.nombre || ''} ${p.apellido_paterno || ''} ${p.apellido_materno || ''}`.trim();
        $('#nombre_mov').val(nombreCompleto);

        if (p.rut) {
          const optRut = new Option(p.rut, movId, true, true);
          $('#id_rut').empty().append(optRut).trigger('change');
          console.log('Opción RUT agregada y seleccionada:', p.rut);
        }

        if (f.numero_ficha && f.id) {
          const optFicha = new Option(f.numero_ficha, f.id, true, true);
          $('#id_ficha').empty().append(optFicha).trigger('change');
          console.log('Opción Ficha agregada y seleccionada:', f.numero_ficha);
        }

        if (data.servicio_clinico) $('#servicio_clinico_ficha').val(data.servicio_clinico).trigger('change');
        if (data.profesional) $('#profesional_movimiento').val(data.profesional).trigger('change');
        if (typeof data.observacion_entrada !== 'undefined') $('#observacion_entrada_ficha').val(data.observacion_entrada || '');
      },
      error: function (err) {
        console.error('Error en AJAX:', err);
      }
    });
  }
});

