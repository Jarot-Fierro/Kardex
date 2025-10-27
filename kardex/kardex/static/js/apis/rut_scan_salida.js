(function(){
  function debounce(fn, wait){
    let t; return function(){
      const ctx=this, args=arguments; clearTimeout(t);
      t=setTimeout(function(){ fn.apply(ctx,args); }, wait);
    };
  }

  function normalizeRut(val){
    if(!val) return '';
    return String(val).trim();
  }

  function cargarPorPrimerResultado(items){
    try{
      if(!Array.isArray(items) || items.length === 0) return;
      var first = items[0];
      // Usa la función global existente para cargar campos por fichaId
      if(first && typeof first.id !== 'undefined' && typeof window.cargarDatosSalidaFicha === 'function'){
        window.cargarDatosSalidaFicha(first.id);
      }
    }catch(_){/* noop */}
  }

  document.addEventListener('DOMContentLoaded', function(){
    var $rut = document.getElementById('id_rut');
    if(!$rut) return;

    var form = $rut.form || document.querySelector('#form-salida');
    var lastInputTs = 0;

    // Evita que Enter dispare submit automático
    $rut.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
    });

    if(form){
      form.addEventListener('submit', function(e){
        var now = Date.now();
        if(now - lastInputTs < 600){
          e.preventDefault();
          e.stopPropagation();
          return false;
        }
      }, true);
    }

    var runQuery = debounce(function(){
      var rut = normalizeRut($rut.value || '');
      if(!rut) return;
      lastInputTs = Date.now();

      var url = '/api/ingreso-paciente-ficha/';
      var params = new URLSearchParams({ search: rut, tipo: 'rut' });
      fetch(url + '?' + params.toString(), {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      })
      .then(function(res){ return res.json().catch(function(){ return {}; }); })
      .then(function(data){
        var items = Array.isArray(data) ? data : (data.results || []);
        var existe = Array.isArray(items) && items.length > 0;
        console.log('[rut_scan_salida] Consulta RUT', rut, 'existe=', existe, items);
        window.dispatchEvent(new CustomEvent('salidaRutConsultado', {
          detail: { rut: rut, existe: existe, data: items }
        }));
        // Cargar automáticamente por el primer resultado si existe
        if(existe){
          cargarPorPrimerResultado(items);
        }
      })
      .catch(function(err){
        console.warn('[rut_scan_salida] Error consultando API de RUT:', err);
        window.dispatchEvent(new CustomEvent('salidaRutConsultado', {
          detail: { rut: rut, existe: false, data: [], error: true }
        }));
      });
    }, 250);

    $rut.addEventListener('input', runQuery);
    $rut.addEventListener('paste', function(){ setTimeout(runQuery, 0); });
  });
})();