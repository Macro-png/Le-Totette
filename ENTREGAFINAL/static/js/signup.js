
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
        const regex = /^[a-zA-Z]+$/
        nombreValido = regex.test(nombreInput.value);
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

    camposValidos = emailValido && contrasenaValida && nombreValido && contrasenaRequisitos

    if (nombreValido) {
        if (document.getElementById("nombre").classList.contains("error")) {
            document.getElementById("nombre").classList.remove("error")
        }
        document.getElementById("nombre").placeholder=""
    } else {
        document.getElementById("nombre").classList.add("error")
        document.getElementById("nombre").placeholder="Nombre inválido"

        document.getElementById("nombre").value=""
    }

    if (contrasenaValida) {
        if (document.getElementById("verificarcontrasena").classList.contains("error")) {
            document.getElementById("verificarcontrasena").classList.remove("error")
        }
        document.getElementById("verificarcontrasena").placeholder=""
    } else {
        document.getElementById("verificarcontrasena").classList.add("error")
        if(contrasenaRequisitos){
            document.getElementById("verificarcontrasena").placeholder="No coincide"

            document.getElementById("verificarcontrasena").value=""
        }
        else{
            document.getElementById("verificarcontrasena").placeholder="Error en la contrasena"

            document.getElementById("verificarcontrasena").value=""
        }
    }

    if (contrasenaRequisitos) {
        if (document.getElementById("contrasena").classList.contains("error")) {
            document.getElementById("contrasena").classList.remove("error")
        }
        document.getElementById("contrasena").placeholder=""
    } else {
        document.getElementById("contrasena").classList.add("error")
        document.getElementById("contrasena").placeholder="Min. 6 digitos"

        document.getElementById("contrasena").value=""
    }

    if (emailValido) {
        if (document.getElementById("email").classList.contains("error")) {
            document.getElementById("email").classList.remove("error")
        }
        document.getElementById("email").placeholder=""
    } else {
        document.getElementById("email").classList.add("error")
        document.getElementById("email").placeholder="Email inválido"
        
        document.getElementById("email").value=""
    }

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







