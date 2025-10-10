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
        const results = (data.results || []).map(item => ({ id: item.id, text: item.text }));
        return { results };
      }
    },
    minimumInputLength: 1
  });

  function llenarPorMovimiento(movId) {
    $.ajax({
      url: `/api/recepcion-ficha/${movId}/`,
      method: 'GET',
      success: function (data) {
        const p = data.paciente || {};
        const f = data.ficha || {};
        // Nombre completo en el input del formulario
        const nombreCompleto = `${p.nombre || ''} ${p.apellido_paterno || ''} ${p.apellido_materno || ''}`.trim();
        $('#nombre_mov').val(nombreCompleto);
        // Sincronizar select2 RUT
        if (p.rut) {
          const opt = new Option(p.rut, data.movimiento.id, true, true);
          $rut.empty().append(opt).trigger('change');
        }
        // Sincronizar Ficha si existe un select
        const $ficha = $('#ficha_movimiento, #id_ficha');
        if ($ficha.length && f.id && f.numero_ficha) {
          const optF = new Option(f.numero_ficha, f.id, true, true);
          $ficha.empty().append(optF).trigger('change');
        }
      },
      error: function () {
        Swal.fire('Error', 'No se pudo cargar la información del movimiento.', 'error');
      }
    });
  }

  $rut.on('select2:select', function (e) {
    const movId = e.params.data.id;
    llenarPorMovimiento(movId);
  });

  // Guardado por AJAX
  $('#btn-guardar').on('click', function () {
    const selected = $rut.select2('data');
    if (!selected || !selected.length) {
      Swal.fire('Información', 'Debe seleccionar un RUT con movimiento pendiente.', 'info');
      return;
    }
    const movId = selected[0].id;
    const fechaEntrada = $('#fecha_entrada_ficha').val();
    const obs = $('#observacion_entrada_ficha').val();
    $.ajax({
      url: `/api/recepcion-ficha/${movId}/mark_received/`,
      method: 'POST',
      data: {
        fecha_entrada: fechaEntrada,
        observacion_entrada: obs,
        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
      },
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      success: function (resp) {
        if (resp && resp.ok) {
          Swal.fire('Éxito', 'Recepción registrada correctamente.', 'success');
          try { $('#Table').DataTable().ajax.reload(null, false); } catch (e) {}
        } else {
          Swal.fire('Error', (resp && resp.error) || 'No se pudo registrar la recepción.', 'error');
        }
      },
      error: function () {
        Swal.fire('Error', 'No se pudo registrar la recepción.', 'error');
      }
    });
  });
});
