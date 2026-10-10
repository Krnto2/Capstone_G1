/*
 * SIREMA · captura de fotografías desde la cámara del celular (CU-C10).
 * El navegador abre la cámara trasera con <input capture="environment">; el
 * archivo original se envía sin recomprimir para conservar la fecha de captura
 * de sus metadatos. El servidor lo redimensiona y calcula su SHA-256.
 */
window.SiremaCamara = (function () {
  "use strict";
  var TIPOS = ["image/jpeg", "image/png", "image/webp"];
  var MAXIMO = 10 * 1024 * 1024;

  function validar(archivo) {
    if (!archivo) return "No se seleccionó ninguna imagen.";
    if (archivo.type && TIPOS.indexOf(archivo.type) === -1) return "Formato no admitido: use JPEG, PNG o WebP.";
    if (archivo.size > MAXIMO) return "La fotografía supera los 10 MB permitidos.";
    return null;
  }

  function subir(url, archivo, punto, csrf) {
    var error = validar(archivo);
    if (error) return Promise.reject({ mensaje: error, red: false });
    var datos = new FormData();
    datos.append("archivo", archivo, archivo.name || "foto.jpg");
    if (punto) datos.append("punto", punto);
    return fetch(url, {
      method: "POST",
      body: datos,
      headers: { "X-CSRFToken": csrf },
      credentials: "same-origin"
    }).then(function (respuesta) {
      return respuesta.json().catch(function () { return { ok: false, error: "Respuesta no válida del servidor." }; })
        .then(function (json) {
          if (!respuesta.ok || !json.ok) throw { mensaje: json.error || "No se pudo subir la fotografía.", red: false };
          return json;
        });
    }, function () {
      throw { mensaje: "Sin conexión. Vuelva a tomar la fotografía al recuperar la señal.", red: true };
    });
  }

  return { subir: subir, validar: validar };
})();
