/* pedidosadmin.js
   Manejo de la UI para la lista de pedidos en admin.
   (Archivo completo - cambios mínimos en URLs AJAX)
*/

/* ---------- variables globales / selección de nodos ---------- */
var contenedorPedidos = document.querySelector('.orders');
var modalCancelar = document.querySelector('.modal-cancel');
var cancelacionPendiente = null;

/* -------- Delegación de eventos en pedidos -------- */
function alEnfocarDentroDePedidos(e) {
  var objetivo = e.target;
  if (objetivo && objetivo.classList.contains('status')) {
    objetivo.setAttribute('data-prev', objetivo.value);
  }
}

function alCambiarEstado(e) {
  var objetivo = e.target;
  if (!objetivo.classList.contains('status')) return;

  var selectEstado   = objetivo;
  var elementoPedido = selectEstado.closest('.order');

  var nuevoValor  = selectEstado.value;
  var valorPrevio = selectEstado.getAttribute('data-prev');

  if (nuevoValor === 'cancelado') {
    abrirModal({
      elementoPedido: elementoPedido,
      elementoSelect: selectEstado,
      valorPrevio: valorPrevio
    });
    return;
  }
  aplicarEstadoAPedido(elementoPedido, nuevoValor);
  selectEstado.setAttribute('data-prev', nuevoValor);

  // INICIO NUEVO "envío Ajax para persistir cambio de estado en backend"
  try {
    var pedidoId = elementoPedido.getAttribute('data-id') || elementoPedido.getAttribute('data-order-id') || (function(){
      var h = elementoPedido.querySelector('h3');
      if (h) {
        var m = h.textContent.replace(/\D/g,'');
        return m || '';
      }
      return '';
    })();
    if (pedidoId) {
      var xhr = new XMLHttpRequest();
      // URL corregida para coincidir con la ruta Flask: /actualizar_estado_pedido
      xhr.open('POST', '/actualizar_estado_pedido', true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.onload = function() {
        if (xhr.status === 200) {
          // éxito (se puede mostrar notificación)
        } else {
          // revertir visualmente al valor previo
          selectEstado.value = valorPrevio || 'espera';
          aplicarEstadoAPedido(elementoPedido, valorPrevio || 'espera');
        }
      };
      xhr.onerror = function() {
        // en error de red, revertir
        selectEstado.value = valorPrevio || 'espera';
        aplicarEstadoAPedido(elementoPedido, valorPrevio || 'espera');
      };
      xhr.send('pedido_id=' + encodeURIComponent(pedidoId) + '&estado=' + encodeURIComponent(nuevoValor));
    }
  } catch (e) {
    console.log('Error al enviar cambio de estado:', e);
    selectEstado.value = valorPrevio || 'espera';
    aplicarEstadoAPedido(elementoPedido, valorPrevio || 'espera');
  }
  // FIN NUEVO
}

function aplicarEstadoAPedido(elementoPedido, estado) {
  var badge = elementoPedido.querySelector('.estado-texto');
  if (badge) badge.textContent = estado;
}

/* -------- Modal de confirmación para cancelar -------- */
function abrirModal(data) {
  modalCancelar.classList.add('is-open');
  cancelacionPendiente = data;
}

function cerrarModal() {
  if (modalCancelar) modalCancelar.classList.remove('is-open');
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) {
    cancelacionPendiente.elementoSelect.disabled = false;
    cancelacionPendiente.elementoSelect.focus();
  }
  cancelacionPendiente = null;
}

function alConfirmarCancelacion() {
  if (!cancelacionPendiente) return;

  var elementoPedido = cancelacionPendiente.elementoPedido;
  var selectEstado   = cancelacionPendiente.elementoSelect;

  aplicarEstadoAPedido(elementoPedido, 'cancelado');
  selectEstado.value = 'cancelado';

  window.setTimeout(function () { elementoPedido.parentNode.removeChild(elementoPedido); }, 400);

  // INICIO NUEVO "envío Ajax para persistir cancelación en backend"
  try {
    var pedidoId2 = elementoPedido.getAttribute('data-id') || elementoPedido.getAttribute('data-order-id') || (function(){
      var h = elementoPedido.querySelector('h3');
      if (h) {
        var m = h.textContent.replace(/\D/g,'');
        return m || '';
      }
      return '';
    })();
    if (pedidoId2) {
      var xhr2 = new XMLHttpRequest();
      // URL corregida para coincidir con la ruta Flask: /actualizar_estado_pedido
      xhr2.open('POST', '/actualizar_estado_pedido', true);
      xhr2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr2.onload = function() {
        // opcional: manejar respuesta
      };
      xhr2.onerror = function() {
        console.log('Error al notificar cancelación al servidor');
      };
      xhr2.send('pedido_id=' + encodeURIComponent(pedidoId2) + '&estado=cancelado');
    }
  } catch (e) {
    console.log('Error al enviar cancelación:', e);
  }
  // FIN NUEVO

  cerrarModal();
}

function alRechazarCancelacion() {
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) {
    cancelacionPendiente.elementoSelect.value = cancelacionPendiente.valorPrevio || 'espera';
  }
  cerrarModal();
}

/* INIT */
(function inicializar() {
  if (!contenedorPedidos) return;
  contenedorPedidos.addEventListener('focusin', alEnfocarDentroDePedidos, false);
  contenedorPedidos.addEventListener('change', alCambiarEstado, false);
})();
