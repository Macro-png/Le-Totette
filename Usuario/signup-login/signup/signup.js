
function validar() {
    
    let nombreValido = false
    let emailValido = false
    let contrasenaValida = false
    let camposValidos = false

    const nombreInput = document.getElementById("nombre")
    const emailInput = document.getElementById("email")
    const contrasenaInput = document.getElementById("contrasena")
    const verificarContrasenaInput = document.getElementById("verificarcontrasena")

    if (nombreInput.value === "") {
        nombreValido = false
    } else {
        nombreValido = true
    }

    if (emailInput.value === "") {
        emailValido = false
    } else {
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        emailValido = regex.test(emailInput.value); //si es mail da true, sino false
    }

    if (contrasenaInput.value === "") {
        contrasenaValida = false
    } else {
        if (verificarContrasenaInput.value === contrasenaInput.value) {
            contrasenaValida = true
        } else {
            contrasenaValida = false
        }
    }

    if (nombreValido) {
        if (document.getElementById("nombre").classList.contains("error")) {
            document.getElementById("nombre").classList.remove("error")
        }
    } else {
        document.getElementById("nombre").classList.add("error")
    }

    if (contrasenaValida) {
        if (document.getElementById("verificarcontrasena").classList.contains("error")) {
            document.getElementById("verificarcontrasena").classList.remove("error")
        }
    } else {
        document.getElementById("verificarcontrasena").classList.add("error")
    }

    if (emailValido) {
        if (document.getElementById("email").classList.contains("error")) {
            document.getElementById("email").classList.remove("error")
        }
    } else {
        document.getElementById("email").classList.add("error")
    }

    camposValidos = emailValido && contrasenaValida && nombreValido

    return camposValidos

}






