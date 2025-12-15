// ------------------ SELECCIÓN DE ELEMENTOS ------------------
var form = document.getElementById("formProducto");
var btnAgregarfiltros = document.getElementById("agregarfiltros");
var contenedorfiltros = document.getElementById("contenedor-filtros");
const MAX_FILTROS = 3;

// ------------------ FUNCIONES DE APOYO ------------------
function mostrarError(input, mensaje) {
  input.classList.remove("input-ok");
  input.classList.add("input-error");

  var errorText = input.parentElement.querySelector(".error-text");
  errorText.textContent = mensaje;
  errorText.classList.add("mensaje-error");
}

function limpiarError(input) {
  input.classList.remove("input-error");
  input.classList.add("input-ok");

  var errorText = input.parentElement.querySelector(".error-text");
  errorText.textContent = "";
  errorText.classList.remove("mensaje-error");
}
// Contar filtros actuales
function getCantidadfiltros() {
  return contenedorfiltros.querySelectorAll(".filtros").length;
}
// Habilitar/Deshabilitar botón "+" según tope
function actualizarEstadoBotonAgregar() {
  var cantidad = getCantidadfiltros();
  var alMaximo = cantidad >= MAX_FILTROS;

  btnAgregarfiltros.disabled = alMaximo;
  btnAgregarfiltros.title = alMaximo 
    ? "Ya alcanzaste el máximo de " + MAX_FILTROS + " filtros."
    : "Agregar un nuevo filtro";
    // Operador ternario -> manera corta de if-else -> ? si es true, : si es false
}

// ------------------ VALIDACIONES INDIVIDUALES ------------------

function validarNombre() {
  var input = document.getElementById("nombre");
  var valor = input.value.trim();

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
  var valor = input.value.trim();

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
  var valor = input.value.trim().replace(",", ".");
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
  var archivo = input.files[0];

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





// ------------------ AGREGAR NUEVO FILTRO------------------
function agregarfiltros() {
  if (getCantidadfiltros() >= MAX_FILTROS) {
    alert("Solo puedes tener " + MAX_FILTROS + " filtros en total.");
    actualizarEstadoBotonAgregar();
    return;
  }

  // Crear nuevo bloque .filtros
  const div = document.createElement("div");
  div.classList.add("filtros");

  div.innerHTML = `
      <label>Filtro</label>
      <input type="text" class="filtro" name="filtros[]">
      <small class="error-text"></small>
  `;

  contenedorfiltros.appendChild(div);

  actualizarEstadoBotonAgregar();
}


// ------------------ VALIDACIÓN EN TIEMPO REAL ------------------
function activarValidaciones() {
  document.getElementById("nombre").addEventListener("input", validarNombre);
  document.getElementById("caract").addEventListener("input", validarCaracteristicas);
  document.getElementById("precio").addEventListener("input", validarPrecio);
  document.getElementById("archivo").addEventListener("change", validarArchivo);


}

// ------------------ VALIDACIÓN GENERAL DEL FORMULARIO ------------------
function validarFormulario() {
  event.preventDefault();

  var valido = true; 
  /* valido es una variable de control -> si durante la validacion encuentra un error, se cambia a false. Si no, al final tendrá true -> significara que no hay ningun error en el form */

  if (!validarNombre()) valido = false;
  if (!validarCaracteristicas()) valido = false;
  if (!validarPrecio()) valido = false;
  if (!validarArchivo()) valido = false;


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
btnAgregarfiltros.addEventListener("click", agregarfiltros);
form.addEventListener("submit", validarFormulario);
activarValidaciones();
// Ajusta el estado inicial del botón según la cantidad de filtros ya presentes en el HTML
actualizarEstadoBotonAgregar();

