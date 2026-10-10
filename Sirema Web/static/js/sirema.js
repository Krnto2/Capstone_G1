/* SIREMA · utilidades comunes de la interfaz (mejora progresiva: todo funciona sin JS). */
(function () {
  "use strict";

  // Confirmación antes de acciones irreversibles.
  document.addEventListener("submit", function (evento) {
    var form = evento.target;
    var boton = evento.submitter;
    var mensaje = (boton && boton.dataset.confirmar) || form.dataset.confirmar;
    if (mensaje && !window.confirm(mensaje)) evento.preventDefault();
  });

  // Mostrar u ocultar la contraseña (M1).
  document.querySelectorAll("[data-alternar-clave]").forEach(function (boton) {
    boton.addEventListener("click", function () {
      var campo = document.querySelector(boton.dataset.alternarClave);
      if (!campo) return;
      var visible = campo.type === "text";
      campo.type = visible ? "password" : "text";
      boton.setAttribute("aria-label", visible ? "Mostrar contraseña" : "Ocultar contraseña");
      boton.querySelector("i").className = visible ? "bi bi-eye" : "bi bi-eye-slash";
    });
  });

  // Los filtros del panel se aplican al cambiar.
  document.querySelectorAll("[data-autoenvio]").forEach(function (control) {
    control.addEventListener("change", function () { control.form.submit(); });
  });

  // RF-05: búsqueda desde el segundo carácter, sin apretar «Buscar».
  document.querySelectorAll("input[data-busqueda]").forEach(function (campo) {
    var temporizador;
    campo.addEventListener("input", function () {
      clearTimeout(temporizador);
      var largo = campo.value.trim().length;
      if (largo === 1) return;
      temporizador = setTimeout(function () { campo.form.submit(); }, 550);
    });
    if (campo.value) {
      campo.focus();
      campo.setSelectionRange(campo.value.length, campo.value.length);
    }
  });
})();
