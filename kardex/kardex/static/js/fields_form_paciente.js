(function () {
        function qs(sel) { return document.querySelector(sel); }
        function qid(id) { return document.getElementById(id); }
        const el = {
            rut: qid('id_rut'),
            nie: qid('nie_paciente'),
            pasaporte: qid('pasaporte_paciente'),
            ocupacion: qid('ocupacion_paciente'),
            nombre_pareja: qid('nombre_pareja_paciente'),
            rut_resp_temp: qid('rut_responsable_temporal_paciente'),
            usar_rut_madre: qid('usar_rut_madre_como_responsable_paciente'),
            rut_madre: qid('id_rut_madre'),
            recien_nacido: qid('recien_nacido_paciente'),
            extranjero: qid('extranjero_paciente'),
            fallecido: qid('fallecido_paciente'),
            fecha_fallecimiento: qid('fecha_fallecimiento_paciente'),
        };


        function setDisabled(inputs, disabled) {
            inputs.filter(Boolean).forEach(i => {
                i.disabled = !!disabled;
                if (disabled) {
                    if (i.type === 'checkbox' || i.type === 'radio') { i.checked = false; }
                    else { i.value = ''; }
                    i.removeAttribute('required');
                }
            });
        }
        function setEnabled(inputs) {
            inputs.filter(Boolean).forEach(i => { i.disabled = false; });
        }
        function setRequired(inputs, required) {
            inputs.filter(Boolean).forEach(i => {
                if (required) i.setAttribute('required', 'required'); else i.removeAttribute('required');
            });
        }

        function applyRules() {
            const rn = !!(el.recien_nacido && el.recien_nacido.checked);
            const ext = !!(el.extranjero && el.extranjero.checked);
            const fal = !!(el.fallecido && el.fallecido.checked);

            // Reset defaults: enable general fields
            setEnabled([el.rut, el.pasaporte, el.nie, el.ocupacion, el.nombre_pareja, el.rut_resp_temp, el.usar_rut_madre, el.fecha_fallecimiento]);

            // Clear required by default
            setRequired([el.rut, el.pasaporte, el.nie, el.fecha_fallecimiento, el.rut_resp_temp], false);

            if (!rn && !ext && !fal) {
                // Estándar, sin fallecimiento
                setEnabled([el.ocupacion, el.nombre_pareja]);
                setDisabled([el.nie, el.pasaporte, el.rut_resp_temp, el.usar_rut_madre, el.fecha_fallecimiento], true);
                setRequired([el.rut], true);
            }

            if (!rn && !ext && fal) {
                // Fallecido solo
                setEnabled([el.fecha_fallecimiento]);
                setDisabled([el.nie, el.pasaporte, el.rut_resp_temp, el.usar_rut_madre], true);
                setRequired([el.fecha_fallecimiento], true);
                setRequired([el.rut], true);
            }

            if (rn && !ext && !fal) {
                // Recien nacido solo
                setEnabled([el.rut_resp_temp, el.usar_rut_madre]);
                setDisabled([el.nie, el.pasaporte, el.ocupacion, el.nombre_pareja, el.fecha_fallecimiento], true);
                setRequired([el.rut_resp_temp], true);
                setRequired([el.rut_madre], true);
                setRequired([el.rut], false);
            }

            if (rn && !ext && fal) {
                // Recien nacido + Fallecido
                setEnabled([el.fecha_fallecimiento, el.rut_resp_temp, el.usar_rut_madre]);
                setDisabled([el.nombre_pareja, el.nie, el.pasaporte, el.ocupacion], true);
                setRequired([el.fecha_fallecimiento], true);
                setRequired([el.rut_resp_temp], false);
                setRequired([el.rut_madre], true);
                setRequired([el.rut], false);
            }

            if (!rn && ext && !fal) {
                // Extranjero solo
                setEnabled([el.nie, el.pasaporte]);
                setDisabled([el.rut_resp_temp, el.usar_rut_madre, el.ocupacion, el.fecha_fallecimiento], true);
                setRequired([el.nie, el.pasaporte], false);
                setRequired([el.rut], false);
            }

            if (!rn && ext && fal) {
                // Extranjero + Fallecido
                setEnabled([el.fecha_fallecimiento, el.nie, el.pasaporte, el.nombre_pareja]);
                setDisabled([el.rut_resp_temp, el.usar_rut_madre, el.ocupacion], true);
                setRequired([el.fecha_fallecimiento], true);
                setRequired([el.rut_resp_temp, el.rut], false);
            }

            if (rn && ext && !fal) {
                // Recien nacido + Extranjero (sin fallecer)
                setEnabled([el.nie, el.pasaporte, el.rut_resp_temp, el.usar_rut_madre]);
                setDisabled([el.nombre_pareja, el.ocupacion, el.fecha_fallecimiento], true);
                setRequired([el.rut_resp_temp], true);
                setRequired([el.rut_madre], true);
                setRequired([el.rut], false);
            }

            if (rn && ext && fal) {
                // Recien nacido + Extranjero + Fallecido
                setEnabled([el.fecha_fallecimiento, el.rut_resp_temp, el.usar_rut_madre, el.nie, el.pasaporte]);
                setDisabled([el.nombre_pareja, el.ocupacion], true);
                setRequired([el.fecha_fallecimiento], true);
                setRequired([el.rut_madre], true);
                setRequired([el.rut_resp_temp], false);
                setRequired([el.rut], false);
            }
        }

        function onSubmit(e) {
            const rn = el.recien_nacido && el.recien_nacido.checked;
            const ext = el.extranjero && el.extranjero.checked;
            const fal = el.fallecido && el.fallecido.checked;

            // Fallecido requires fecha_fallecimiento
            if (fal) {
                if (el.fecha_fallecimiento && !el.fecha_fallecimiento.value) {
                    e.preventDefault();
                    alert('Debe ingresar la fecha de fallecimiento.');
                    el.fecha_fallecimiento.focus();
                    return false;
                }
            }

            if (rn) {
                // Validate responsable: either rut_responsable_temporal or usar_rut_madre checked
                const hasTemp = el.rut_resp_temp && el.rut_resp_temp.value.trim() !== '';
                const useMadre = el.usar_rut_madre && el.usar_rut_madre.checked;
                if (!hasTemp && !useMadre) {
                    e.preventDefault();
                    alert('Debe ingresar RUT responsable temporal o activar "Usar RUT de la madre como responsable".');
                    if (el.rut_resp_temp) el.rut_resp_temp.focus();
                    return false;
                }
            }

            if (!rn && ext) {
                const hasNie = el.nie && el.nie.value.trim() !== '';
                const hasPas = el.pasaporte && el.pasaporte.value.trim() !== '';
                if (!hasNie && !hasPas) {
                    e.preventDefault();
                    alert('Para pacientes extranjeros, debe ingresar al menos NIE o Pasaporte.');
                    if (el.nie) el.nie.focus();
                    return false;
                }
            }

            if (!rn && !ext && !fal) {
                if (el.rut && el.rut.value.trim() === '') {
                    e.preventDefault();
                    alert('El campo RUT es obligatorio para pacientes estándar.');
                    el.rut.focus();
                    return false;
                }
            }
        }

        document.addEventListener('change', function (ev) {
            if (!ev.target) return;
            const id = ev.target.id;
            if (['recien_nacido_paciente', 'extranjero_paciente', 'fallecido_paciente'].includes(id)) {
                applyRules();
            }
        });

        document.addEventListener('DOMContentLoaded', function () {
            applyRules();
            // Attach submit validation
            const form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', onSubmit);
            }
        });
        // Expose rules applier for other scripts (e.g., AJAX fill)
        window._pacienteApplyRules = applyRules;
    })();