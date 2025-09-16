document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('formModal');

    if (modal) {
        // Si el formulario está en un modal
        modal.addEventListener('shown.bs.modal', function () {
            $('.field_select').select2({
                dropdownParent: $('#formModal'),
                width: '100%',
                language: 'es',
                theme: 'bootstrap-5',
            });
        });

        modal.addEventListener('hidden.bs.modal', function () {
            $('.field_select').select2('destroy');
        });
    } else {
        // Si el formulario es estático
        $('.field_select').select2({
            width: '100%',
            language: 'es',
            theme: 'bootstrap-5',
        });
    }
});
