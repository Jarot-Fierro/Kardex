document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".ajax-form").forEach(form => {
        form.addEventListener("submit", e => {
            e.preventDefault();

            // Resetear errores anteriores
            form.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
            form.querySelectorAll(".invalid-feedback").forEach(el => el.remove());

            fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        // Mostrar mensaje de éxito
                        Swal.fire({
                            icon: data.level || 'success',
                            title: 'Operación exitosa',
                            text: data.message || 'Operación completada',
                            confirmButtonColor: '#198754'
                        }).then(() => {
                            // Recargar página completa al dar OK
                            window.location.reload();
                        });

                        // Cerrar modal (por si sigue abierto)
                        const modalEl = document.querySelector("#formModal");
                        if (modalEl) {
                            const modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) modal.hide();
                        }

                    } else {
                        // Mostrar mensaje de error general
                        if (data.message) {
                            Swal.fire({
                                icon: data.level || 'error',
                                title: 'Error',
                                text: data.message,
                                confirmButtonColor: '#dc3545'
                            });
                        }

                        // Errores campo a campo
                        for (let field in data.errors) {
                            let input = form.querySelector(`[name="${field}"]`);
                            if (input) {
                                input.classList.add("is-invalid");
                                let div = document.createElement("div");
                                div.classList.add("invalid-feedback");
                                div.textContent = data.errors[field].join(", ");
                                input.insertAdjacentElement("afterend", div);
                            }
                        }
                    }
                });
        });
    });
});
