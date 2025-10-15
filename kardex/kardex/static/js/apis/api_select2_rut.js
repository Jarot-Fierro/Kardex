// Consulta la API al salir del campo RUT y completa el formulario si existe
(function(){
    const API_URL = 'http://127.0.0.1:8000/api/ingreso-paciente-ficha/';

    function fillPaciente(paciente){
        if(!paciente) return;
        // Campos comunes del formulario (usar IDs reales presentes en la plantilla)
        function normalizeDate(iso){
            if(!iso) return '';
            const s = String(iso);
            const parts = s.includes('T') ? s.split('T')[0].split('-') : s.split('-');
            if(parts.length !== 3) return s;
            const [y,m,d] = parts; return `${d}/${m}/${y}`;
        }
        function setSelectValue(selector, value, label){
            if (value === null || value === undefined || value === '') return;
            const $el = $(selector);
            if ($el.length === 0) return;
            const valStr = String(value);
            if ($el.find(`option[value="${valStr}"]`).length === 0) {
                const text = (label !== undefined && label !== null && label !== '') ? String(label) : valStr;
                const newOpt = new Option(text, valStr, true, true);
                $el.append(newOpt);
            }
            $el.val(valStr).trigger('change');
        }
        const map = {
            // Identificación
            'id_rut': paciente.rut || '',
            'id_rut_madre': paciente.rut_madre || '',
            // Datos personales
            'nombre_paciente': paciente.nombre || '',
            'apellido_paterno_paciente': paciente.apellido_paterno || '',
            'apellido_materno_paciente': paciente.apellido_materno || '',
            'nombre_social_paciente': paciente.nombre_social || '',
            'sexo_paciente': paciente.sexo || '',
            'estado_civil_paciente': paciente.estado_civil || '',
            // Contacto y dirección
            'direccion_paciente': paciente.direccion || '',
            'numero_telefono1_paciente': paciente.numero_telefono1 || '',
            'numero_telefono2_paciente': paciente.numero_telefono2 || '',
            'ocupacion_paciente': paciente.ocupacion || '',
            // Relaciones
            'nombres_padre_paciente': paciente.nombres_padre || '',
            'nombres_madre_paciente': paciente.nombres_madre || ''
        };
        Object.keys(map).forEach(id => {
            const el = document.getElementById(id);
            if(!el) return;
            const val = map[id] ?? '';
            if (el.tagName === 'SELECT') {
                const hasOption = [...el.options].some(o => String(o.value) === String(val));
                if (hasOption) {
                    el.value = String(val);
                }
            } else {
                el.value = val;
            }
            const evt = new Event('change', { bubbles: true });
            el.dispatchEvent(evt);
        });
        // Selects con IDs de catálogos que pueden no tener la opción cargada aún
        setSelectValue('#genero_paciente', paciente.genero);
        setSelectValue('#id_genero', paciente.genero);
        setSelectValue('#comuna_paciente', paciente.comuna);
        setSelectValue('#prevision_paciente', paciente.prevision);
        // Fechas: normalizar y asignar a posibles IDs/inputs
        const ddmmyy = normalizeDate(paciente.fecha_nacimiento);
        if (ddmmyy) {
            const $fn1 = $('#fecha_nacimiento_paciente');
            const $fn2 = $('#id_fecha_nacimiento');
            if ($fn1.length) { $fn1.val(ddmmyy).trigger('change'); }
            if ($fn2.length) { $fn2.val(ddmmyy).trigger('change'); }
        }
        const ddmmyyFal = normalizeDate(paciente.fecha_fallecimiento);
        if (ddmmyyFal) {
            $('#fecha_fallecimiento_paciente').val(ddmmyyFal).trigger('change');
        }
        // Aplicar reglas dinámicas si están disponibles
        if (window._pacienteApplyRules) {
            try { window._pacienteApplyRules(); } catch(e) {}
        }
    }

    function buscarPorRut(rut){
        if(!rut) return;
        $.ajax({
            url: API_URL,
            dataType: 'json',
            data: { search: rut, tipo: 'rut' },
            success: function(data){
                const items = Array.isArray(data) ? data : (data.results || []);
                if(items.length > 0){
                    const ficha = items[0];
                    const paciente = ficha && ficha.paciente ? ficha.paciente : null;
                    fillPaciente(paciente);
                }
            },
            error: function(){
                // Silencioso: no bloquear al usuario si la API falla
            }
        });
    }

    // Ejecutar búsqueda al salir del input de RUT
    $(document).on('blur', '#id_rut', function(){
        const rut = $(this).val().trim();
        buscarPorRut(rut);
    });
})();
