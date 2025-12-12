function validar() {
    
    let emailValido = false
    let contrasenaValida = false
    let camposValidos = false

 
    const emailInput = document.getElementById("email")
    const contrasenaInput = document.getElementById("contrasena")


    if (emailInput.value === "") {
        emailValido = false
    } else {
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        emailValido = regex.test(emailInput.value); //si es mail da true, sino false
    }

    if (contrasenaInput.value === "") {
        contrasenaValida = false
    } else {
        contrasenaValida = true
    }



    if (contrasenaValida) {
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

    camposValidos = emailValido && contrasenaValida

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

    return camposValidos

}
