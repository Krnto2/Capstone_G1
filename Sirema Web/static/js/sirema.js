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

  // Búsqueda en vivo (RF-05): al escribir o cambiar un filtro, la lista se actualiza sin recargar
  // la página. El botón del formulario sigue funcionando igual si no hay JavaScript.
  var SELECTOR_TEXTO = "input[type=search], input[type=text]";
  document.querySelectorAll("form[data-busqueda-en-vivo]").forEach(function (form) {
    var destino = document.querySelector(form.dataset.resultados);
    if (!destino || !window.fetch) return;
    var temporizador, controlador, ultima = consulta();

    function consulta() {
      var params = new URLSearchParams();
      new FormData(form).forEach(function (valor, clave) {
        if (clave !== "page" && String(valor).trim() !== "") params.append(clave, valor);
      });
      return params.toString();
    }

    function textoDeUnCaracter() {
      return Array.prototype.some.call(form.querySelectorAll(SELECTOR_TEXTO), function (campo) {
        return campo.value.trim().length === 1;
      });
    }

    function buscar() {
      if (textoDeUnCaracter()) return;  // RF-05: resultados desde el segundo carácter
      var q = consulta();
      if (q === ultima) return;
      ultima = q;
      var url = (form.getAttribute("action") || location.pathname) + (q ? "?" + q : "");
      if (controlador) controlador.abort();
      controlador = new AbortController();
      destino.classList.add("cargando");
      destino.setAttribute("aria-busy", "true");
      fetch(url, { credentials: "same-origin", signal: controlador.signal, headers: { "X-Requested-With": "fetch" } })
        .then(function (respuesta) {
          if (!respuesta.ok) throw new Error("HTTP " + respuesta.status);
          return respuesta.text();
        })
        .then(function (html) {
          var nuevo = new DOMParser().parseFromString(html, "text/html").querySelector(form.dataset.resultados);
          if (!nuevo) { form.submit(); return; }  // por ejemplo, la sesión expiró
          destino.innerHTML = nuevo.innerHTML;
          history.replaceState(null, "", url);
        })
        .catch(function (error) { if (error.name !== "AbortError") form.submit(); })
        .then(function () { destino.classList.remove("cargando"); destino.removeAttribute("aria-busy"); });
    }

    form.addEventListener("input", function (evento) {
      if (!evento.target.matches(SELECTOR_TEXTO)) return;
      clearTimeout(temporizador);
      temporizador = setTimeout(buscar, 300);
    });
    form.addEventListener("change", function (evento) {
      if (evento.target.matches("select, input[type=date]")) buscar();
    });
  });
})();
