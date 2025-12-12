/* pedidos.js 
   - Tras confirmar cancelación: espera breve y elimina la tarjeta
*/

/* ------- Funciones de selección ------ */
function seleccionar(selector, nodo) {
  return (nodo || document).querySelector(selector);
}
function seleccionarTodos(selector, nodo) {
  return Array.prototype.slice.call((nodo || document).querySelectorAll(selector));
}

/* ------- Elementos clave del DOM ------- */
var contenedorPedidos = seleccionar('#orders');
var botonSimular      = seleccionar('#btn-simular');
var plantillaPedido   = seleccionar('#order-template');

var modalCancelar = seleccionar('#confirm-cancel');
var modalSi       = seleccionar('#confirm-yes');
var modalNo       = seleccionar('#confirm-no');

/* ------- Estado del modal ------- */
var cancelacionPendiente = null; //Cuando no hay cancelacion en curso pq nadie le ha dado al select "cancelado"
// Estructura esperada:
// {
//   elementoPedido: HTMLElement, (Pedido que se quiere cancelar)
//   elementoSelect: HTMLSelectElement, (El select afectado)
//   valorPrevio: string (valor anterior a intentar cancelar)
// }

/* Cuántos ms esperar antes de eliminar la tarjeta tras confirmar */
var RETRASO_ELIMINAR_MS = 2000;

/* ------- Lógica de estados ------- */
// Traduce el value del option a texto para el badge
function etiquetaDeEstado(valor) {
  if (valor === 'espera') return 'Espera';
  if (valor === 'produccion') return 'Producción';
  if (valor === 'retirar') return 'Para retirar';
  if (valor === 'cancelado') return 'Cancelado';
//   return valor; --> fallback que ahora no es util
}

function aplicarEstadoAPedido(elementoPedido, valorEstado) {
  var estados = ['espera', 'produccion', 'retirar', 'cancelado'];
  for (var i = 0; i < estados.length; i++) {
    elementoPedido.classList.remove(estados[i]); //remueve estadis anteriores
  }
  elementoPedido.classList.add(valorEstado); //agrega el actual

  var insignia = seleccionar('.badge', elementoPedido);
  if (insignia) {
    insignia.textContent = etiquetaDeEstado(valorEstado); // agrega el estado al badge
  }
}

/* ------ Modal: abrir/cerrar ------ */
function abrirModal(contexto) {
  // contexto es un objeto con (divDelPedidoCompleto,Select.status,valorPrevio)
  cancelacionPendiente = contexto; //Guardo en el sistema el pedido que se intenta cancelar
  if (modalCancelar) modalCancelar.classList.add('is-open'); //el if es para evitar errores si movemos codigo html o css (verifica si existe o no el modal)
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) { //por seguridad -> ¿Existe una CancelacionPendiente y existe la propiedad elementoSelect dentro?
    cancelacionPendiente.elementoSelect.disabled = true; //Desactivo el select mientras el modal está abierto
  }
}

function cerrarModal() {
  if (modalCancelar) modalCancelar.classList.remove('is-open');
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) { 
    cancelacionPendiente.elementoSelect.disabled = false; //vuelvo a activar el select al cerrarse el modal
    cancelacionPendiente.elementoSelect.focus(); //focus al select del elemento que intento cancelar
  }
  cancelacionPendiente = null; //Redefino cancelacion pendiente a null
}

/* -------- Delegación de eventos en pedidos -------- */
function alEnfocarDentroDePedidos(e) /*solo como callback al registrar */{
  var objetivo = e.target //-> objeto especifico que disparo el evento
  if (objetivo && objetivo.classList.contains('status')) { //si existe el elemento y tiene la clase status (refuerzo por seguridad. soy desconfiado :c)
    // Solo se aplica cuando hay un select.status
    objetivo.setAttribute('data-prev', objetivo.value);
    /* objetivo.value -> valor actual del select cuando se enfoco (es,pro,ret,canc) 
    'data-prev' -> atributo para dato personalizado -> guardo el valor previo al focus
    para que, si abre el modal directamente y elige "NO" -> podamos volver a ese valor previo*/

  }
}

function alCambiarEstado(e) {
  var objetivo = e.target;
  if (!objetivo.classList.contains('status')) return; //si no tiene la clase status -> se para la funcion

  var selectEstado   = objetivo; //El select que disparo el evento
  var elementoPedido = selectEstado.closest('.order'); // -> Ancestro mas cercano llamado .order
  /*Padre del Select en focus*/
  
  var nuevoValor  = selectEstado.value; //-> Nuevo valor despues del cambio
  var valorPrevio = selectEstado.getAttribute('data-prev'); //-> tomo el valor previo en focusin
  
  if (nuevoValor === 'cancelado') { // si el valor al momento de cambiar es "cancelado":
    abrirModal({
      elementoPedido: elementoPedido,
      elementoSelect: selectEstado,
      valorPrevio: valorPrevio
    });
    return;
  }
  // Si es cualquier otro valor:
  aplicarEstadoAPedido(elementoPedido, nuevoValor);
  selectEstado.setAttribute('data-prev', nuevoValor);
}

/* -------- Eventos del modal -------- */
function alConfirmarCancelacion() {
  if (!cancelacionPendiente) return; //(refuerzo) Si no hay ninguna cancelacion pendiente se para la funcion

  var elementoPedido = cancelacionPendiente.elementoPedido; //Padre del select -> Tarjeta completa
  var selectEstado   = cancelacionPendiente.elementoSelect; //Select que dispara el evento

  // Reflejar de inmediato el estado cancelado (badge y clase)
  aplicarEstadoAPedido(elementoPedido, 'cancelado');
  selectEstado.value = 'cancelado';
  // selectEstado.setAttribute('data-prev', 'cancelado'); -> no util

  // Espera breve y elimina la tarjeta
  window.setTimeout(function () {elementoPedido.parentNode.removeChild(elementoPedido);}, 
  RETRASO_ELIMINAR_MS);

  cerrarModal(); // -> se ejecuta por fuera para que se cierre de inmediato
}

function alRechazarCancelacion() {
  if (cancelacionPendiente && cancelacionPendiente.elementoSelect) {
    cancelacionPendiente.elementoSelect.value = cancelacionPendiente.valorPrevio || 'espera'; //el "espera" es por si acaso el valorPrevio es undefinied
  }
  cerrarModal();
}

/* ==========================
   Simulación de pedido nuevo (autoincremental)
   ========================== */
function obtenerSiguienteNumeroPedido() {
  var numeros = seleccionarTodos('.order__number', contenedorPedidos).map(function (span) {
    var n = parseInt(span.textContent, 10); //El 10 es para que el numero sea en base 10
    return isNaN(n) ? 0 : n; 
    //Si el texto no era un numero -> retorna 0. si lo era, retorna la variable n
  });
  /* El .map recorre el array de spans y retorna un array con ints (el map siempre recorre un array y le aplica una funcion a cada elemento y retorna un nuevo array resultante)*/
  var maximo = 0;
  // ORDENO LA LISTA (POR SI ACASO)
  for (var i = 0; i < numeros.length; i++) {
    if (numeros[i] > maximo) maximo = numeros[i];
  }
  return maximo + 1;
}

function construirPedidoDesdePlantilla(siguienteNumero) {
  var fragmento = document.importNode(plantillaPedido.content, true);
  // Creo una copia total del nodo template (el true es para que se copie TODO)
  var elementoPedido  = seleccionar('.order', fragmento);
  var spanNumero      = seleccionar('.order__number', elementoPedido);
  var selectEstado    = seleccionar('.status', elementoPedido);

  spanNumero.textContent = String(siguienteNumero);
  elementoPedido.setAttribute('data-order-id', String(siguienteNumero));

  aplicarEstadoAPedido(elementoPedido, 'espera');
  if (selectEstado) {
    selectEstado.value = 'espera';
    selectEstado.setAttribute('data-prev', 'espera');
  }
  return elementoPedido;
}

function alClicSimularPedido() {
  var siguiente   = obtenerSiguienteNumeroPedido();
  var nuevoPedido = construirPedidoDesdePlantilla(siguiente);
  contenedorPedidos.appendChild(nuevoPedido);
}


/* ==========================
   Inicialización
   ========================== */
function inicializarPedidos() {
  // if (!contenedorPedidos) return; 

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

inicializarPedidos();
