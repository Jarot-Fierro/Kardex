$(document).ready(function () {
    $('#device_select').on('change', function () {
        const deviceType = new URLSearchParams(window.location.search).get('type');
        const deviceId = $(this).val();

        if (!deviceType || !deviceId) {
            $('#official-field').val('');
            $('#id_official').val('');
            return;
        }

        $.getJSON(`/inventario/api/get-official/?type=${deviceType}&device_id=${deviceId}`, function (data) {
            $('#official-field').val(data.official_name);
            $('#id_official').val(data.id_official);
            console.log('Official data loaded successfully:', data.official_name);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            $('#official-field').val('Error obteniendo datos');
            $('#id_official').val('');
            console.error('Error loading official data:', textStatus, errorThrown);
        });
    });
});