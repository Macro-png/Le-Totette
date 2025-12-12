// ------------------ SELECCIÓN DE ELEMENTOS ------------------
var form = document.getElementById("formProducto");
var btnAgregarColor = document.getElementById("agregarcolor");
var contenedorColores = document.getElementById("contenedor-colores"); /*Para llevar conteo de colores*/
const MAX_COLORES = 3;

// ------------------ FUNCIONES DE APOYO ------------------
function mostrarError(input, mensaje) {
  input.classList.remove("input-ok"); /*itera la classList, si no esta la class, no pasa nada. Solo la remueve si esta*/
  input.classList.add("input-error");

  var errorText = input.parentElement.querySelector(".error-text");
  if (errorText) {
    errorText.textContent = mensaje;
    errorText.classList.add("mensaje-error");
  }
}

function limpiarError(input) {
  input.classList.remove("input-error");
  input.classList.add("input-ok");

  var errorText = input.parentElement.querySelector(".error-text");
  if (errorText) {
    errorText.textContent = "";
    errorText.classList.remove("mensaje-error");
  }
}

// Contar colores actuales
function getCantidadColores() {
  return contenedorColores.querySelectorAll(".colores").length;
}

// Habilitar/Deshabilitar botón "+" según tope
function actualizarEstadoBotonAgregar() {
  var cantidad = getCantidadColores();
  var alMaximo = cantidad >= MAX_COLORES;

  btnAgregarColor.disabled = alMaximo;
  btnAgregarColor.title = alMaximo
    ? "Ya alcanzaste el máximo de " + MAX_COLORES + " colores."
    : "Agregar un nuevo color";
  // Operador ternario: ? si es true, : si es false
}

// ------------------ VALIDACIONES INDIVIDUALES ------------------
function validarNombre() {
  var input = document.getElementById("nombre");
  var valor = (input.value || "").trim();

  if (valor === "") {
    mostrarError(input, "El nombre es obligatorio.");
    return false;
  } else if (valor.length < 3) {
    mostrarError(input, "Debe tener al menos 3 caracteres.");
    return false;
  } else {
    limpiarError(input);
    return true;
  }
}

function validarCaracteristicas() {
  var input = document.getElementById("caract");
  var valor = (input.value || "").trim();

  if (valor === "") {
    mostrarError(input, "Las características son obligatorias.");
    return false;
  } else if (valor.length < 10) {
    mostrarError(input, "Debe contener al menos 10 caracteres.");
    return false;
  } else {
    limpiarError(input);
    return true;
  }
}

function validarPrecio() {
  var input = document.getElementById("precio");
  var valor = (input.value || "").trim().replace(",", ".");
  var numero = parseFloat(valor);

  if (valor === "") {
    mostrarError(input, "El precio es obligatorio.");
    return false;
  } else if (isNaN(numero) || numero <= 0) {
    mostrarError(input, "Ingrese un precio válido (número mayor a 0).");
    return false;
  } else {
    limpiarError(input);
    return true;
  }
}

function validarArchivo() {
  var input = document.getElementById("archivo");
  var archivo = input.files && input.files[0];

  if (!archivo) {
    mostrarError(input, "Debe subir una imagen del producto.");
    return false;
  } else {
    var extension = archivo.name.split(".").pop().toLowerCase();
    var extensionesValidas = ["jpg", "jpeg", "png"];

    if (extensionesValidas.indexOf(extension) === -1) {
      mostrarError(input, "Formato no válido. Solo JPG, JPEG o PNG.");
      return false;
    } else {
      limpiarError(input);
      return true;
    }
  }
}

function validarColor(input) {
  var valor = (input.value || "").trim();
  var regexHex = /^#?([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$/; // Hex de 3 o 6

  if (valor === "") {
    mostrarError(input, "El color es obligatorio.");
    return false;
  } else if (!regexHex.test(valor)) {
    mostrarError(input, "Formato inválido. Use código hexadecimal (ej: #FAD6B1).");
    return false;
  } else {
    limpiarError(input);
    return true;
  }
}

// ------------------ AGREGAR NUEVO COLOR ------------------
function agregarColor() {
  if (getCantidadColores() >= MAX_COLORES) {
    // Defensa adicional por si el botón no estuviera deshabilitado
    alert("Solo puedes tener " + MAX_COLORES + " colores en total.");
    actualizarEstadoBotonAgregar();
    return;
  }

  var cantidadActual = getCantidadColores();
  var nuevoNumero = cantidadActual + 1;

  // Crear nuevo bloque .colores
  var nuevoDiv = document.createElement("div");
  nuevoDiv.className = "colores";

  // Label
  var nuevoLabel = document.createElement("label");
  nuevoLabel.setAttribute("for", "color" + nuevoNumero);
  nuevoLabel.textContent = "Código hexadecimal del color " + nuevoNumero;

  // Input
  var nuevoInput = document.createElement("input");
  nuevoInput.type = "text";
  nuevoInput.id = "color" + nuevoNumero;
  nuevoInput.className = "color";

  // Small de error
  var nuevoSmall = document.createElement("small");
  nuevoSmall.className = "error-text";

  // Ensamblar
  nuevoDiv.appendChild(nuevoLabel);
  nuevoDiv.appendChild(nuevoInput);
  nuevoDiv.appendChild(nuevoSmall);
  contenedorColores.appendChild(nuevoDiv);

  // Validación en tiempo real para el nuevo input
  nuevoInput.addEventListener("input", function () {
    validarColor(nuevoInput);
  });

  actualizarEstadoBotonAgregar();
}

// ------------------ VALIDACIÓN EN TIEMPO REAL ------------------
function activarValidaciones() {
  // Campos principales
  document.getElementById("nombre").addEventListener("input", validarNombre);
  document.getElementById("caract").addEventListener("input", validarCaracteristicas);
  document.getElementById("precio").addEventListener("input", validarPrecio);
  document.getElementById("archivo").addEventListener("change", validarArchivo);

  // Todos los colores presentes (incluye el primero)
  var inputsColor = contenedorColores.querySelectorAll("input.color");
  inputsColor.forEach(function (c) {
    c.addEventListener("input", function () {
      validarColor(c);
    });
  });
}

// ------------------ VALIDACIÓN GENERAL DEL FORMULARIO ------------------
function validarFormulario(event) {
  event.preventDefault();

  var valido = true; 
  // Variable de control -> si encuentra un error, cambia a false

  if (!validarNombre()) valido = false;
  if (!validarCaracteristicas()) valido = false;
  if (!validarPrecio()) valido = false;
  if (!validarArchivo()) valido = false;

  // Validar todos los colores
  var colores = contenedorColores.querySelectorAll("input.color");
  for (var i = 0; i < colores.length; i++) {
    if (!validarColor(colores[i])) {
      valido = false;
    }
  }
  var mensaje = document.getElementById("mensaje-general");

  if (valido) {
    mensaje.textContent = "✅ Producto agregado correctamente.";
    mensaje.className = "mensaje-general ok";
    form.submit()
    } else {
      mensaje.textContent = "⚠️ Hay campos con errores. Corrígelos antes de continuar.";
      mensaje.className = "mensaje-general error";
    }
  }
  
// ------------------ EVENTOS PRINCIPALES ------------------
if (btnAgregarColor) btnAgregarColor.addEventListener("click", agregarColor);
if (form) form.addEventListener("submit", validarFormulario);
activarValidaciones();
// Ajusta el estado inicial del botón según la cantidad de colores ya presentes en el HTML
actualizarEstadoBotonAgregar();
