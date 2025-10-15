$('#id_ficha').select2({
    placeholder: 'Buscar por número de ficha',
    width: '100%',
    ajax: {
        url: 'http://127.0.0.1:8000/api/ingreso-paciente-ficha/',
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return {
                search: params.term,
                tipo: 'ficha'
            };
        },
        processResults: function (data) {
            return {
                results: data.results.map(item => ({
                    id: item.id,
                    text: `Ficha: ${item.numero_ficha_sistema}`
                }))
            };
        }
    },
    minimumInputLength: 1
});
