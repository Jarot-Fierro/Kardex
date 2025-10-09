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
            return {
                results: data.results.map(item => {
                    const paciente = item.ingreso_paciente.paciente;
                    return {
                        id: item.id,
                        text: `${paciente.rut}`
                    };
                })
            };
        }
    },
    minimumInputLength: 1
});
