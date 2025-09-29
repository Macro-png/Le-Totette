
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

    return camposValidos

}