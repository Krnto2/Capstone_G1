/*
 * SIREMA · ejecución de revisiones (CU-C7, pantalla M3).
 * Cada respuesta se guarda en el momento con una solicitud JSON (RF-08).
 * Si se corta la red, la respuesta queda en una cola local y se reenvía al
 * reconectar (curso alternativo 4.a).
 */
(function () {
  "use strict";
  var raiz = document.getElementById("revision");
  if (!raiz) return;

  var idRevision = raiz.dataset.revision;
  var claveCola = "sirema-cola-" + idRevision;
  var estado = document.getElementById("estado-guardado");
  var csrf = (document.querySelector("input[name=csrfmiddlewaretoken]") || {}).value || "";

  function urlPunto(id) { return raiz.dataset.urlPunto.replace(/\/0\/$/, "/" + id + "/"); }

  function mostrarEstado(tipo, texto) {
    var iconos = { ok: "bi-cloud-check", guardando: "bi-arrow-repeat", error: "bi-cloud-slash" };
    estado.className = "estado-guardado" + (tipo === "error" ? " error" : "");
    estado.innerHTML = '<i class="bi ' + iconos[tipo] + '" aria-hidden="true"></i> ' + texto;
  }

  // ---------------------------------------------------------- cola local --
  function leerCola() {
    try { return JSON.parse(localStorage.getItem(claveCola) || "{}"); } catch (e) { return {}; }
  }
  function guardarCola(cola) {
    try {
      if (Object.keys(cola).length) localStorage.setItem(claveCola, JSON.stringify(cola));
      else localStorage.removeItem(claveCola);
    } catch (e) { /* almacenamiento no disponible */ }
  }
  function encolar(idPunto, datos) { var cola = leerCola(); cola[idPunto] = datos; guardarCola(cola); }

  function procesarCola() {
    var cola = leerCola();
    var ids = Object.keys(cola);
    if (!ids.length) return;
    mostrarEstado("guardando", "Enviando respuestas pendientes…");
    ids.reduce(function (promesa, id) {
      return promesa.then(function () {
        return enviarDatos(id, cola[id]).then(function () {
          var actual = leerCola(); delete actual[id]; guardarCola(actual);
        });
      });
    }, Promise.resolve()).catch(function () { /* sigue en cola */ });
  }

  // ----------------------------------------------------------- progreso --
  function actualizarProgreso(json) {
    var resumen = json.resumen, faltan = json.faltantes;
    if (resumen) {
      var porcentaje = resumen.total ? Math.round(resumen.respondidos * 100 / resumen.total) : 0;
      document.getElementById("barra-progreso").style.width = porcentaje + "%";
      document.getElementById("texto-progreso").textContent = resumen.respondidos + " de " + resumen.total;
    }
    if (faltan) {
      document.getElementById("texto-faltantes").textContent = faltan.texto;
      var boton = document.getElementById("boton-finalizar");
      boton.classList.toggle("disabled", !faltan.completa);
      if (faltan.completa) { boton.removeAttribute("aria-disabled"); boton.removeAttribute("tabindex"); }
      else { boton.setAttribute("aria-disabled", "true"); boton.setAttribute("tabindex", "-1"); }
    }
  }

  // -------------------------------------------------------------- envío --
  function enviarDatos(idPunto, datos) {
    return fetch(urlPunto(idPunto), {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      credentials: "same-origin",
      body: JSON.stringify(datos)
    }).then(function (respuesta) {
      return respuesta.json().catch(function () { return { ok: false, error: "Respuesta no válida del servidor." }; })
        .then(function (json) {
          var seccion = document.getElementById("punto-" + idPunto);
          if (!respuesta.ok || !json.ok) {
            if (seccion) mostrarError(seccion, json.error || "No se pudo guardar.");
            mostrarEstado("error", "No guardado");
            throw { red: false };
          }
          if (seccion) {
            mostrarError(seccion, "");
            seccion.classList.add("respondido");
            seccion.classList.toggle("alerta", !!json.fuera_de_rango);
          }
          mostrarEstado("ok", "Guardado " + json.guardado);
          actualizarProgreso(json);
          return json;
        });
    }, function () {
      encolar(idPunto, datos);
      mostrarEstado("error", "Sin conexión: se enviará al reconectar");
      throw { red: true };
    });
  }

  function mostrarError(seccion, texto) {
    var caja = seccion.querySelector("[data-error]");
    if (caja) caja.textContent = texto;
  }

  function valorDe(seccion) {
    var tipo = seccion.dataset.tipo;
    if (tipo === "booleano") {
      var marcado = seccion.querySelector("input[data-campo=valor]:checked");
      return marcado ? marcado.value : "";
    }
    var campo = seccion.querySelector("[data-campo=valor]");
    return campo ? campo.value.trim() : "";
  }

  function fueraDeRango(seccion, valor) {
    if (seccion.dataset.tipo !== "numerico" || valor === "") return false;
    var numero = parseFloat(valor.replace(",", "."));
    if (isNaN(numero)) return false;
    var min = seccion.dataset.min, max = seccion.dataset.max;
    return (min !== "" && numero < parseFloat(min.replace(",", "."))) ||
           (max !== "" && numero > parseFloat(max.replace(",", ".")));
  }

  function enviarPunto(seccion) {
    var resultado = seccion.dataset.resultado;
    if (!resultado) return;
    var valor = valorDe(seccion);
    var observacion = (seccion.querySelector("[data-campo=observacion]") || {}).value || "";
    if ((seccion.dataset.tipo === "numerico" || seccion.dataset.tipo === "booleano") && !valor) {
      mostrarError(seccion, seccion.dataset.tipo === "numerico" ? "Ingrese el valor medido para guardar." : "Indique Sí o No para guardar.");
      return;
    }
    if (resultado !== "conforme" && !observacion.trim()) {
      mostrarError(seccion, "Escriba la observación para guardar el resultado.");
      return;
    }
    mostrarError(seccion, "");
    mostrarEstado("guardando", "Guardando…");
    enviarDatos(seccion.dataset.punto, { resultado: resultado, valor: valor, observacion: observacion.trim() })
      .catch(function () { /* el error ya se mostró */ });
  }

  // ------------------------------------------------------ comportamiento --
  document.querySelectorAll(".punto[data-punto]").forEach(function (seccion) {
    var temporizador;
    var bloqueObs = seccion.querySelector("[data-bloque-observacion]");
    var textoObs = seccion.querySelector("[data-campo=observacion]");
    var aviso = seccion.querySelector("[data-aviso-rango]");

    function programarEnvio() { clearTimeout(temporizador); temporizador = setTimeout(function () { enviarPunto(seccion); }, 700); }

    seccion.querySelectorAll(".btn-resultado").forEach(function (boton) {
      boton.addEventListener("click", function () {
        seccion.querySelectorAll(".btn-resultado").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        boton.setAttribute("aria-pressed", "true");
        seccion.dataset.resultado = boton.dataset.resultado;
        var pideObs = boton.dataset.resultado !== "conforme";
        if (bloqueObs) bloqueObs.hidden = !pideObs;
        if (pideObs && textoObs && !textoObs.value.trim()) { textoObs.focus(); mostrarError(seccion, "Escriba la observación para guardar el resultado."); return; }
        enviarPunto(seccion);
      });
    });

    seccion.querySelectorAll("[data-campo=valor]").forEach(function (campo) {
      var evento = campo.type === "radio" ? "change" : "input";
      campo.addEventListener(evento, function () {
        if (aviso) {
          var fuera = fueraDeRango(seccion, valorDe(seccion));
          aviso.hidden = !fuera;
          seccion.classList.toggle("alerta", fuera);
        }
        if (seccion.dataset.resultado) programarEnvio();
      });
    });

    if (textoObs) textoObs.addEventListener("input", function () { if (seccion.dataset.resultado) programarEnvio(); });
  });

  // ----------------------------------------------------------- fotografías --
  document.querySelectorAll("input[data-foto-punto]").forEach(function (entrada) {
    entrada.addEventListener("change", function () {
      var archivo = entrada.files && entrada.files[0];
      if (!archivo) return;
      var seccion = entrada.closest(".punto");
      var etiqueta = entrada.closest("[data-boton-foto]");
      etiqueta.classList.add("disabled");
      mostrarEstado("guardando", "Subiendo fotografía…");
      window.SiremaCamara.subir(raiz.dataset.urlFoto, archivo, entrada.dataset.fotoPunto, csrf)
        .then(function (json) {
          var enlace = document.createElement("a");
          enlace.href = json.url; enlace.target = "_blank"; enlace.rel = "noopener";
          var img = document.createElement("img");
          img.src = json.url; img.alt = "Fotografía de evidencia";
          enlace.appendChild(img);
          seccion.querySelector("[data-miniaturas]").appendChild(enlace);
          mostrarError(seccion, "");
          mostrarEstado("ok", "Fotografía guardada · SHA-256 " + json.hash.slice(0, 8) + "…");
          actualizarProgreso(json);
        })
        .catch(function (error) {
          mostrarError(seccion, error.mensaje || "No se pudo subir la fotografía.");
          mostrarEstado("error", "Fotografía no guardada");
        })
        .then(function () { etiqueta.classList.remove("disabled"); entrada.value = ""; });
    });
  });

  window.addEventListener("online", procesarCola);
  window.addEventListener("offline", function () { mostrarEstado("error", "Sin conexión"); });
  procesarCola();
})();
