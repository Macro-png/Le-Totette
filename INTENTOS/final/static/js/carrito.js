// carrito.js
// =============================
// Utilidades simples
// =============================
function seleccionarElemento(selector, nodo) {
  return (nodo || document).querySelector(selector);
}

function seleccionarTodosLosElementos(selector, nodo) {
  return Array.prototype.slice.call((nodo || document).querySelectorAll(selector));
}

// =============================
// Elementos clave
// =============================
var contenedorItems = seleccionarElemento('.cart-items');      // Lista de productos
var modal           = seleccionarElemento('#confirm-remove');  // Modal de confirmación
var botonSi         = seleccionarElemento('#remove-yes');      // Botón "Sí, eliminar"
var botonNo         = seleccionarElemento('#remove-no');       // Botón "No, conservar"

// =============================
// Estado actual
// =============================
var itemPendiente = null; // Guarda el producto que el usuario intenta eliminar

// =============================
// Funciones principales
// =============================
function abrirModal(item) {
  itemPendiente = item;
  if (modal) modal.classList.add('is-open');
}

function cerrarModal() {
  if (modal) modal.classList.remove('is-open');
  itemPendiente = null;
}

// =============================
// Evento: clic en el tacho
// =============================
function alClickearEnLista(evento) {
  var elementoClickeado = evento.target;
  // Verifico que el clic provenga de un botón con clase .btn-remove (el tacho rojo)
  var botonEliminar = elementoClickeado.closest ? elementoClickeado.closest('.btn-remove') : null;  
  /* Busca el padre del icono (el boton con la clase btn-remove) -> el operador ternario es por si se abre en un navegador antiguo que no soporta el evento closest */
    
    // Si no se hizo clic en un botón de eliminar o si ese botón no pertenece al contenedor de productos,
    // corto la ejecución (no hago nada)
  if (!botonEliminar || !contenedorItems.contains(botonEliminar)) return;

  // Si sí se hizo clic en un tacho válido, busco el producto completo (.cart-item) al que pertenece ese botón
  var item = botonEliminar.closest('.cart-item');
  if (item) abrirModal(item);
}

// =============================
// Eventos del modal
// =============================
function confirmarEliminacion() {
  if (!itemPendiente) return;
  var contenedor = itemPendiente.parentNode; //Me dirijo al padre que tiene todos los cart-item
  if (contenedor) contenedor.removeChild(itemPendiente); //si existe ese contenedor -> remueve el hijo que seleccionamos
  cerrarModal();
}

function cancelarEliminacion() {
  cerrarModal();
}

// =============================
// Inicialización
// =============================
function inicializarCarrito() {
  if (contenedorItems) contenedorItems.addEventListener('click', alClickearEnLista, false);
  if (botonSi) botonSi.addEventListener('click', confirmarEliminacion, false);
  if (botonNo) botonNo.addEventListener('click', cancelarEliminacion, false);
}

// Llamada inicial
inicializarCarrito();
