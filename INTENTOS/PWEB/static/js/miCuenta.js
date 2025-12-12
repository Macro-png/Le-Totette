// ================== SELECCIÓN DE ELEMENTOS ==================
var formUsuario = document.getElementById("formUsuario");
var inputPassActual = document.getElementById("passActual");
var inputPassNueva = document.getElementById("passNueva");
var inputPassConfirmar = document.getElementById("passConfirmar");
var mensajeGeneral = document.getElementById("mensaje-general");

// ================== FUNCIONES DE APOYO (UI errores/ok) ==================
function mostrarError(input, mensaje) {
  // Aplica estilo rojo al input
  input.classList.remove("input-ok");
  input.classList.add("input-error");

  // Muestra el texto de error en el <small> hermano
  var errorText = input.parentElement.querySelector(".error-text");
  if (errorText) {
    errorText.textContent = mensaje || "";
    errorText.classList.add("mensaje-error");
  }
}

function limpiarError(input) {
  // Quita estilo de error y marca OK
  input.classList.remove("input-error");
  input.classList.add("input-ok");

  // Oculta el texto de error del <small>
  var errorText = input.parentElement.querySelector(".error-text");
  if (errorText) {
    errorText.textContent = "";
    errorText.classList.remove("mensaje-error");
  }
}

function setMensajeGeneralOk(texto) {
  mensajeGeneral.textContent = texto || "Operación realizada correctamente.";
  mensajeGeneral.className = "mensaje-general ok";
}

function setMensajeGeneralError(texto) {
  mensajeGeneral.textContent = texto || "Hay campos con errores. Corrígelos antes de continuar.";
  mensajeGeneral.className = "mensaje-general error";
}

// ================== REGLAS DE VALIDACIÓN ==================
function cumplePolitica(password) {
  // Mínimo 8 caracteres, al menos una letra y un número
  var tieneLongitud = password.length >= 8;
  var tieneLetra = /[a-zA-Z]/.test(password);
  var tieneNumero = /\d/.test(password);
  return tieneLongitud && tieneLetra && tieneNumero;
}

// ----- Validaciones individuales -----
function validarPassActual() {
  var valor = (inputPassActual.value || "").trim();

  if (valor === "") {
    mostrarError(inputPassActual, "La contraseña actual es obligatoria.");
    return false;
  }
  // (La verificación real con servidor se hará después; aquí solo validamos formato de entrada)
  limpiarError(inputPassActual);
  return true;
}

function validarPassNueva() {
  var actual = (inputPassActual.value || "").trim();
  var nueva = (inputPassNueva.value || "").trim();

  if (nueva === "") {
    mostrarError(inputPassNueva, "La nueva contraseña es obligatoria.");
    return false;
  }
  if (!cumplePolitica(nueva)) {
    mostrarError(
      inputPassNueva,
      "Debe tener al menos 8 caracteres, incluir letras y números."
    );
    return false;
  }
  if (actual && nueva === actual) {
    mostrarError(inputPassNueva, "La nueva contraseña no puede ser igual a la actual.");
    return false;
  }
  limpiarError(inputPassNueva);
  return true;
}

function validarPassConfirmar() {
  var nueva = (inputPassNueva.value || "").trim();
  var confirmar = (inputPassConfirmar.value || "").trim();

  if (confirmar === "") {
    mostrarError(inputPassConfirmar, "Debes confirmar la nueva contraseña.");
    return false;
  }
  if (nueva !== confirmar) {
    mostrarError(inputPassConfirmar, "Las contraseñas no coinciden.");
    return false;
  }
  limpiarError(inputPassConfirmar);
  return true;
}

// ================== VALIDACIÓN EN TIEMPO REAL ==================
function activarValidacionesTiempoReal() {
  inputPassActual.addEventListener("input", function () {
    validarPassActual();
  });

  inputPassNueva.addEventListener("input", function () {
    // Validamos nueva y, de paso, revalidamos confirmación si ya escribió algo
    var okNueva = validarPassNueva();
    if (inputPassConfirmar.value.trim() !== "") {
      validarPassConfirmar();
    }
    return okNueva;
  });

  inputPassConfirmar.addEventListener("input", function () {
    validarPassConfirmar();
  });
}

// ================== VALIDACIÓN GENERAL Y ENVÍO ==================
function validarFormulario(event) {
  // Bloquea el envío hasta comprobar todo
  if (event && typeof event.preventDefault === "function") {
    event.preventDefault();
  }

  var valido = true;

  if (!validarPassActual()) valido = false;
  if (!validarPassNueva()) valido = false;
  if (!validarPassConfirmar()) valido = false;

  if (valido) {
    setMensajeGeneralOk("✅ Contraseña actualizada correctamente.");
    // Aquí harías la petición al servidor (fetch/AJAX).
  } else {
    setMensajeGeneralError("⚠️ Hay campos con errores. Corrígelos antes de continuar.");
  }
}

// ================== INICIALIZACIÓN ==================
function init() {
  activarValidacionesTiempoReal();
  if (formUsuario) formUsuario.addEventListener("submit", validarFormulario);
  // Limpia mensaje general al tocar cualquier campo
  if (formUsuario) {
    formUsuario.addEventListener("input", function () {
      // Solo borra el estado visual del mensaje general si ya se mostró
      if (mensajeGeneral && (mensajeGeneral.classList.contains("ok") || mensajeGeneral.classList.contains("error"))) {
        mensajeGeneral.textContent = "";
        mensajeGeneral.className = "mensaje-general";
      }
    });
  }
}

init();
