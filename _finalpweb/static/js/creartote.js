
//Función de Expresión Invocada Inmediatamente

//cuando se carga la página:

//Se ejecuta la IIFE: 
// La IIFE se ejecuta inmediatamente. 
// Dentro de ella, se realiza la inicialización del código.

//Se seleccionan los elementos del DOM: 
//Se asignan los elementos HTML (<input> y <img>) a las variables input e imgPreview.

//Se configura el event listener:
// Se le dice al input que "escuche" un evento de tipo change.
// Esto significa que el código dentro del listener solo se ejecutará
// cuando el usuario seleccione un nuevo archivo.

//La IIFE termina, pero el listener continúa:
// La ejecución de la IIFE finaliza, pero el event listener
// que creó permanece activo, esperando a que el evento change ocurra.
// Este es un ejemplo de cómo una IIFE crea un cierre (closure),
// permitiendo que el listener acceda a las variables que estaban en el ámbito de la IIFE.

//OTRAS VENTAJAS:
//para evitar la contaminación del ámbito global.
// encapsular variables y la lógica en una función anónima
// que se ejecuta de inmediato, se aísla el código del resto de la aplicación.

(function () {
    var input = document.getElementById('archivo');
    var imgPreview = document.getElementById('preview');
    var objURLActual = null;
    //Se inicializa una variable para almacenar la URL temporal del objeto de la imagen.
    // La inicialización a null indica que aún no hay ninguna URL asignada.

    input.addEventListener('change', function () {
      //el evento se dispara cuando cambiamos el file
      var file = input.files[0];
      //La propiedad input.files es un objeto FileList con todos los archivos seleccionados.
      // Se accede al primer archivo ([0]) porque se espera que el usuario seleccione uno solo.


      // Validación básica de tipo (usar PNG, etc.)
      var valido = /^image\/(jpeg|jpg|png)$/i.test(file.type);
      if (!valido) { //se ejecuta si archivo no es una imagen
        alert('Por favor sube una imagen JPG o PNG.'); //Muestra un mensaje de advertencia al usuario.
        input.value = ''; //Limpia el campo de entrada, borrando el archivo seleccionado.
        imgPreview.style.display = 'none'; //oculta imagen de vista previa
        if (objURLActual) URL.revokeObjectURL(objURLActual);
        //Libera la memoria de cualquier URL de objeto anterior que pudiera existir.

        objURLActual = null;
        return; //Sale de la función para detener el proceso.
      }

      // Libero el URL anterior si existía
      if (objURLActual) URL.revokeObjectURL(objURLActual);

      // Creo un Object URL y lo asigno al <img>
      objURLActual = URL.createObjectURL(file);
      //Genera una URL interna del navegador que apunta al archivo 
      // seleccionado por el usuario. Esta es una "pseudo-URL" 
      // que permite acceder al archivo local.
      imgPreview.src = objURLActual;
      //Asigna esta URL temporal al atributo src de la etiqueta <img>,
      // lo que provoca que el navegador cargue y muestre la imagen.
      imgPreview.style.display = 'block';
      // Hace visible el elemento <img>, que estaba oculto por defecto
    });
  })();