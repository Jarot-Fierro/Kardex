document.addEventListener("DOMContentLoaded", function() {
    const formModal = document.getElementById('formModal');
    if (!formModal) return;

    const baseForm = formModal.querySelector('form');
    const initialFormHTML = baseForm ? baseForm.innerHTML : '';
    const initialFormAction = baseForm ? (baseForm.getAttribute('action') || window.location.pathname) : window.location.pathname;

    function applyFormReplacement(form, htmlContent, actionUrl) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlContent, 'text/html');
        const fetchedForm = doc.querySelector('form.ajax-form') || doc.querySelector('.ajax-form form') || doc.querySelector('.ajax-form');
        if (!fetchedForm) return;

        const formFields = fetchedForm.querySelector('.row') || fetchedForm;
        const currentFields = form.querySelector('.row') || form;
        currentFields.innerHTML = formFields.innerHTML;

        form.action = actionUrl;

        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

        // Inicializa campos ilimitados en el nuevo form
        if (typeof initUnlimitedFields === 'function') {
            initUnlimitedFields(form);
        }
    }

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = btn.getAttribute('data-url');
            formModal.querySelector('.modal-title').textContent = 'Editar Registro';

            const currentForm = formModal.querySelector('form');
            if (!currentForm) return;

            fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(resp => resp.text())
                .then(html => applyFormReplacement(currentForm, html, url))
                .catch(err => console.error('Error loading form data:', err));
        });
    });

    document.querySelectorAll('.new-record-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            formModal.querySelector('.modal-title').textContent = 'Nuevo Registro';
            const form = formModal.querySelector('form');
            if (!form) return;

            if (initialFormHTML) form.innerHTML = initialFormHTML;
            form.reset();
            form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
            form.action = initialFormAction || window.location.pathname;

            if (typeof initUnlimitedFields === 'function') {
                initUnlimitedFields(form);
            }
        });
    });

    formModal.addEventListener('hidden.bs.modal', function() {
        const form = formModal.querySelector('form');
        if (!form) return;
        form.reset();
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
    });
});
