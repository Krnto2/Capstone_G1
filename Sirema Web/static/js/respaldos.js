/* SIREMA · pantalla de respaldos: elegir un respaldo del servidor para restaurar. */
(function () {
  "use strict";

  var form = document.querySelector("[data-form-restaurar]");
  if (!form) return;
  var origen = form.querySelector("input[name=origen]");
  var seleccion = form.querySelector("[data-restaurar-seleccion]");
  var etiqueta = form.querySelector("[data-restaurar-etiqueta]");
  var bloqueArchivo = form.querySelector("[data-restaurar-archivo]");
  var archivo = form.querySelector("input[name=archivo]");

  function mostrar(valor, texto) {
    origen.value = valor || "";
    seleccion.classList.toggle("d-none", !valor);
    bloqueArchivo.classList.toggle("d-none", !!valor);
    if (valor) {
      etiqueta.textContent = texto;
      if (archivo) archivo.value = "";
    }
  }

  document.querySelectorAll("[data-restaurar-origen]").forEach(function (boton) {
    boton.addEventListener("click", function () {
      mostrar(boton.dataset.restaurarOrigen, boton.dataset.restaurarNombre);
      document.getElementById("restaurar").scrollIntoView({ behavior: "smooth" });
      var clave = form.querySelector("input[name=contrasena]");
      if (clave) clave.focus({ preventScroll: true });
    });
  });

  form.querySelector("[data-restaurar-quitar]").addEventListener("click", function () { mostrar("", ""); });

  if (origen.value) mostrar(origen.value, origen.value.split("/").pop());

  // Evita un segundo envío mientras se sube y restaura un archivo grande.
  form.addEventListener("submit", function (evento) {
    if (evento.defaultPrevented) return;
    var boton = form.querySelector("button[type=submit]");
    boton.disabled = true;
    boton.innerHTML = '<span class="spinner-border spinner-border-sm" aria-hidden="true"></span> Restaurando…';
  });
})();
