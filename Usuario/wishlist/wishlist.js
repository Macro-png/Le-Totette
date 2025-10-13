// =============================
// Funciones de selección simples
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
var contenedorProductos = seleccionarElemento('.products');          // Contenedor principal
var modal               = seleccionarElemento('#confirm-remove-wish'); // Modal de confirmación
var botonSi             = seleccionarElemento('#remove-yes-wish');     // Botón "Sí, eliminar"
var botonNo             = seleccionarElemento('#remove-no-wish');      // Botón "No, conservar"

// =============================
// Estado
// =============================
var productoPendiente = null; // Guarda el producto que el usuario desea eliminar

// =============================
// Funciones principales
// =============================
function abrirModal(producto) {
  productoPendiente = producto;
  if (modal) {
    modal.classList.add('is-open');
  }
}

function cerrarModal() {
  if (modal) {
    modal.classList.remove('is-open');
  }
  productoPendiente = null;
}

// =============================
// Evento: clic en el tacho
// =============================
function alClickearEnLista(evento) {
  var elementoClickeado = evento.target;
  var botonEliminar = null;

  // Comprobación
  if (elementoClickeado.closest) {
    botonEliminar = elementoClickeado.closest('.btn-remove');
  }

  if (!botonEliminar) {
    return; // No se hizo clic en un botón de eliminar
  }

  if (!contenedorProductos.contains(botonEliminar)) {
    return; // Seguridad extra: el botón no pertenece al contenedor de productos
  }

  var producto = botonEliminar.closest('.product');
  if (producto) {
    abrirModal(producto);
  }
}

// =============================
// Eventos del modal
// =============================
function confirmarEliminacion() {
  if (!productoPendiente) return;
  var contenedor = productoPendiente.parentNode;
  if (contenedor) {
    contenedor.removeChild(productoPendiente);
  }
  cerrarModal();
}

function cancelarEliminacion() {
  cerrarModal();
}

// =============================
// Inicialización
// =============================
function inicializarWishlist() {
  if (contenedorProductos) {
    contenedorProductos.addEventListener('click', alClickearEnLista, false);
  }
  if (botonSi) {
    botonSi.addEventListener('click', confirmarEliminacion, false);
  }
  if (botonNo) {
    botonNo.addEventListener('click', cancelarEliminacion, false);
  }
}

// Llamada inicial
inicializarWishlist();
