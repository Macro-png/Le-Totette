/* pedidos.js (versión simple)
   - Sin flashes, sin animaciones
   - Modal aparece/desaparece (sin transiciones)
   - Tras confirmar cancelación: espera breve y elimina la tarjeta
*/

/* ==========================
   Utilidades de selección
   ========================== */
function seleccionar(selector, nodo) {
  return (nodo || document).querySelector(selector);
}
function seleccionarTodos(selector, nodo) {
  return Array.prototype.slice.call((nodo || document).querySelectorAll(selector));
}

/* ==========================
   Elementos clave del DOM
   ========================== */
var contenedorPedidos = seleccionar('#orders');
var botonSimular      = seleccionar('#btn-simular');
var plantillaPedido   = seleccionar('#order-template');

var modalCancelar = seleccionar('#confirm-cancel');
var modalSi       = seleccionar('#confirm-yes');
var modalNo       = seleccionar('#confirm-no');

/* ==========================
   Estado del modal
   ========================== */
var cancelacionPendiente = null; 
// Estructura esperada:
// {
//   elementoPedido: HTMLElement,
//   elementoSelect: HTMLSelectElement,
//   valorPrevio: string
// }

/* Cuántos ms esperar antes de eliminar la tarjeta tras confirmar */
var RETRASO_ELIMINAR_MS = 2000;

/* ==========================
   Lógica de estados
   ========================== */
function etiquetaDeEstado(valor) {
  if (valor === 'espera') return 'Espera';
  if (valor === 'produccion') return 'Producción';
  if (valor === 'retirar') return 'Para retirar';
  if (valor === 'cancelado') return 'Cancelado';
//   return valor;
}

function aplicarEstadoAPedido(elementoPedido, valorEstado) {
  var estados = ['espera', 'produccion', 'retirar', 'cancelado'];
  for (var i = 0; i < estados.length; i++) {
    elementoPedido.classList.remove(estados[i]);
  }
  elementoPedido.classList.add(valorEstado);

  var insignia = seleccionar('.badge', elementoPedido);
  if (insignia) {
    insignia.textContent = etiquetaDeEstado(valorEstado);
  }
}

/* ==========================
   Modal: abrir/cerrar
   ========================== */
function abrirModal(contexto) {
  cancelacionPendiente = contexto;
  if (modalCancelar) modalCancelar.classList.add('is-open');
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) {
    cancelacionPendiente.elementoSelect.disabled = true;
  }
}

function cerrarModal() {
  if (modalCancelar) modalCancelar.classList.remove('is-open');
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) {
    cancelacionPendiente.elementoSelect.disabled = false;
    cancelacionPendiente.elementoSelect.focus();
  }
  cancelacionPendiente = null;
}

/* ==========================
   Delegación de eventos en pedidos
   ========================== */
function alEnfocarDentroDePedidos(e) {
  var objetivo = e.target || e.srcElement;
  if (objetivo && objetivo.classList && objetivo.classList.contains('status')) {
    objetivo.setAttribute('data-prev', objetivo.value);
  }
}

function alCambiarEstado(e) {
  var objetivo = e.target || e.srcElement;
  if (!objetivo || !objetivo.classList || !objetivo.classList.contains('status')) return;

  var selectEstado   = objetivo;
  var elementoPedido = selectEstado.closest('.order');
  if (!elementoPedido) return;

  var nuevoValor  = selectEstado.value;
  var valorPrevio = selectEstado.getAttribute('data-prev') || '';

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
}

/* ==========================
   Eventos del modal
   ========================== */
function alConfirmarCancelacion() {
  if (!cancelacionPendiente) return;

  var elementoPedido = cancelacionPendiente.elementoPedido;
  var selectEstado   = cancelacionPendiente.elementoSelect;

  // Reflejar de inmediato el estado cancelado (badge y clase)
  aplicarEstadoAPedido(elementoPedido, 'cancelado');
  if (selectEstado) {
    selectEstado.value = 'cancelado';
    selectEstado.setAttribute('data-prev', 'cancelado');
  }

  // Espera breve y elimina la tarjeta SIN animaciones
  window.setTimeout(function () {
    if (elementoPedido && elementoPedido.parentNode) {
      elementoPedido.parentNode.removeChild(elementoPedido);
    }
  }, RETRASO_ELIMINAR_MS);

  cerrarModal();
}

function alRechazarCancelacion() {
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) {
    cancelacionPendiente.elementoSelect.value = cancelacionPendiente.valorPrevio || 'espera';
  }
  cerrarModal();
}

/* ==========================
   Simulación de pedido nuevo
   ========================== */
function obtenerSiguienteNumeroPedido() {
  var numeros = seleccionarTodos('.order__number', contenedorPedidos).map(function (span) {
    var n = parseInt(span.textContent, 10);
    return isNaN(n) ? 0 : n;
  });
  var maximo = 0;
  for (var i = 0; i < numeros.length; i++) {
    if (numeros[i] > maximo) maximo = numeros[i];
  }
  return maximo + 1;
}

function construirPedidoDesdePlantilla(siguienteNumero) {
  var fragmento       = document.importNode(plantillaPedido.content, true);
  var elementoPedido  = seleccionar('.order', fragmento);
  var spanNumero      = seleccionar('.order__number', elementoPedido);
  var selectEstado    = seleccionar('.status', elementoPedido);

  if (spanNumero) spanNumero.textContent = String(siguienteNumero);
  elementoPedido.setAttribute('data-order-id', String(siguienteNumero));

  aplicarEstadoAPedido(elementoPedido, 'espera');
  if (selectEstado) {
    selectEstado.value = 'espera';
    selectEstado.setAttribute('data-prev', 'espera');
  }
  return elementoPedido;
}

function alClicSimularPedido() {
  var siguiente  = obtenerSiguienteNumeroPedido();
  var nuevoPedido = construirPedidoDesdePlantilla(siguiente);
  contenedorPedidos.appendChild(nuevoPedido);

  try { nuevoPedido.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  catch (err) { nuevoPedido.scrollIntoView(); }
}

/* ==========================
   Inicialización
   ========================== */
function inicializarPedidos() {
  if (!contenedorPedidos) return;

  contenedorPedidos.addEventListener('focusin', alEnfocarDentroDePedidos, false);
  contenedorPedidos.addEventListener('change',  alCambiarEstado,          false);

  if (modalSi) modalSi.addEventListener('click', alConfirmarCancelacion, false);
  if (modalNo) modalNo.addEventListener('click', alRechazarCancelacion,  false);

  if (botonSimular) botonSimular.addEventListener('click', alClicSimularPedido, false);

  // Inicializar data-prev de los selects existentes
  var selectsIniciales = seleccionarTodos('.status', contenedorPedidos);
  for (var i = 0; i < selectsIniciales.length; i++) {
    var s = selectsIniciales[i];
    s.setAttribute('data-prev', s.value);
  }
}

/* Arranque */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', inicializarPedidos, false);
} else {
  inicializarPedidos();
}