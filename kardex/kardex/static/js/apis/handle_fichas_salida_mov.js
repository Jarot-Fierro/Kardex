function cargarDatosSalidaFicha(fichaId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/ingreso-paciente-ficha/${fichaId}/`,
        method: 'GET',
        success: function (data) {
            const paciente = data.paciente || {};

            // --- Rellenar nombre ---
            const nombreCompleto = `${paciente.nombre} ${paciente.apellido_paterno} ${paciente.apellido_materno}`;
            $('#nombre_mov').val(nombreCompleto);

            // --- Sincronizar los campos select2 ---
            const fichaOption = new Option(data.numero_ficha_sistema, data.id, true, true);
            $('#id_ficha').empty().append(fichaOption).trigger('change');


            if (paciente.rut) {
                const rutOption = new Option(paciente.rut, paciente.rut, true, true); // ✅ Usa el rut como value
                $('#id_rut').empty().append(rutOption).trigger('change');
            }

        },
        error: function () {
            alert('Error al cargar los datos de la ficha.');
        }
    });
}
$('#id_ficha, #id_rut').on('select2:select', function (e) {
    const fichaId = e.params.data.id;
    cargarDatosSalidaFicha(fichaId);
});
