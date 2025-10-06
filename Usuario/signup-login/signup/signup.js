
function validar() {
    
    let nombreValido = false
    let emailValido = false
    let contrasenaValida = false
    let camposValidos = false
    let contrasenaRequisitos = false

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
        contrasenaRequisitos = false
    } else {
        const regex = /^.{6,}$/;
        contrasenaRequisitos = regex.test(contrasenaInput.value);
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

    if (contrasenaRequisitos) {
        if (document.getElementById("contrasena").classList.contains("error")) {
            document.getElementById("contrasena").classList.remove("error")
        }
    } else {
        document.getElementById("contrasena").classList.add("error")
    }

    if (emailValido) {
        if (document.getElementById("email").classList.contains("error")) {
            document.getElementById("email").classList.remove("error")
        }
    } else {
        document.getElementById("email").classList.add("error")
    }

    camposValidos = emailValido && contrasenaValida && nombreValido && contrasenaRequisitos

    if (camposValidos) {
        if (document.getElementById("textoerror").classList.contains("textoerrorsi")) {
            document.getElementById("textoerror").classList.remove("textoerrorsi")
        }
        document.getElementById("textoerror").classList.add("textoerrorno")
    } else {
        if (document.getElementById("textoerror").classList.contains("textoerrorno")) {
            document.getElementById("textoerror").classList.remove("textoerrorno")
        }
        document.getElementById("textoerror").classList.add("textoerrorsi")
    }

    return camposValidos

}






