(function () {
    var input = document.getElementById('archivo');
    var imgPreview = document.getElementById('preview');
    var objURLActual = null;

    input.addEventListener('change', function () {
      var file = input.files[0];

      // Validación básica de tipo (usar PNG, etc.)
      var valido = /^image\/(jpeg|jpg|png)$/i.test(file.type);
      if (!valido) {
        alert('Por favor sube una imagen JPG o PNG.');
        input.value = '';
        imgPreview.style.display = 'none';
        if (objURLActual) URL.revokeObjectURL(objURLActual);
        objURLActual = null;
        return;
      }

      // Libero el URL anterior si existía
      if (objURLActual) URL.revokeObjectURL(objURLActual);

      // Creo un Object URL y lo asigno al <img>
      objURLActual = URL.createObjectURL(file);
      imgPreview.src = objURLActual;
      imgPreview.style.display = 'block';
    });
  })();