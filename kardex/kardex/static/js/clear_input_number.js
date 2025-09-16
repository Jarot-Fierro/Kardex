document.addEventListener("DOMContentLoaded", () => {
    const formModal = document.getElementById('formModal');
    if (!formModal) return;

    function setupUnlimitedField(checkbox, input) {
        if (!checkbox || !input) return;

        function toggleInputState() {
            if (checkbox.checked) {
                input.value = 0;
                input.disabled = true;
            } else {
                input.disabled = false;
            }
        }

        // Estado inicial
        toggleInputState();

        // Escuchar cambios
        checkbox.onchange = toggleInputState;
    }

    window.initUnlimitedFields = function(formContext = formModal) {
        setupUnlimitedField(formContext.querySelector('#unlimited_gigabytes_plan'),
                            formContext.querySelector('#gigabytes_plan'));
        setupUnlimitedField(formContext.querySelector('#unlimited_minutes_plan'),
                            formContext.querySelector('#minutes_plan'));
        setupUnlimitedField(formContext.querySelector('#unlimited_messages_plan'),
                            formContext.querySelector('#messages_plan'));
    };

    // Inicializa en el formulario actual
    initUnlimitedFields();
});
