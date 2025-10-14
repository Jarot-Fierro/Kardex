$('#id_rut').select2({
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
            // Si hay paginación DRF -> data.results, si no -> data (array)
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