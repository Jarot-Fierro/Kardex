function validateNumber(input) {
    let value = input.value;

    // Solo permite números (elimina cualquier cosa que no sea dígito)
    value = value.replace(/[^0-9]/g, '');

    // Si el valor comienza con 0 y tiene más de un dígito, lo elimina (ej. "0123")
    if (value.length > 1 && value.startsWith('0')) {
        value = value.slice(1);
    }

    // Si es 0, lo eliminamos
    if (value === '0') {
        value = '';
    }

    // Asignamos el valor limpio al input
    input.value = value;
}