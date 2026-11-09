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

  // Modo claro / oscuro. El tema inicial lo aplica un script en <head> para evitar el destello.
  var CLAVE_TEMA = "sirema-tema";
  function temaActual() { return document.documentElement.getAttribute("data-bs-theme") === "dark" ? "oscuro" : "claro"; }
  function temaGuardado() { try { return localStorage.getItem(CLAVE_TEMA); } catch (e) { return null; } }
  function aplicarTema(tema, guardar) {
    document.documentElement.setAttribute("data-bs-theme", tema === "oscuro" ? "dark" : "light");
    if (guardar) { try { localStorage.setItem(CLAVE_TEMA, tema); } catch (e) { /* sin almacenamiento */ } }
    document.querySelectorAll("[data-cambiar-tema]").forEach(function (boton) {
      boton.setAttribute("aria-pressed", tema === "oscuro" ? "true" : "false");
      var accion = tema === "oscuro" ? "Activar modo claro" : "Activar modo oscuro";
      boton.title = accion;
      if (boton.hasAttribute("data-solo-icono")) boton.setAttribute("aria-label", accion);
    });
  }
  document.querySelectorAll("[data-cambiar-tema]").forEach(function (boton) {
    boton.addEventListener("click", function () { aplicarTema(temaActual() === "oscuro" ? "claro" : "oscuro", true); });
  });
  aplicarTema(temaActual(), false);
  if (window.matchMedia) {
    var oscuroSistema = window.matchMedia("(prefers-color-scheme: dark)");
    var alCambiarSistema = function (e) { if (!temaGuardado()) aplicarTema(e.matches ? "oscuro" : "claro", false); };
    if (oscuroSistema.addEventListener) oscuroSistema.addEventListener("change", alCambiarSistema);
  }

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

  // Formateo del RUT en vivo (RF-01): no hace falta escribir puntos ni guion, se agregan solos.
  function rutLimpio(valor) { return valor.replace(/[^0-9kK]/g, "").toUpperCase(); }
  function rutFormateado(limpio) {
    if (limpio.length < 2) return limpio;
    var cuerpo = limpio.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return cuerpo + "-" + limpio.slice(-1);
  }
  document.querySelectorAll("input[data-rut]").forEach(function (campo) {
    campo.addEventListener("input", function () {
      var utilesAntes = rutLimpio(campo.value.slice(0, campo.selectionStart)).length;
      campo.value = rutFormateado(rutLimpio(campo.value));
      var i = 0, utiles = 0;
      while (i < campo.value.length && utiles < utilesAntes) {
        if (/[0-9kK]/.test(campo.value[i])) utiles++;
        i++;
      }
      try { campo.setSelectionRange(i, i); } catch (e) { /* algunos navegadores no lo permiten */ }
    });
  });

  // La foto de perfil se guarda apenas se elige.
  document.querySelectorAll("[data-enviar-al-elegir]").forEach(function (campo) {
    campo.addEventListener("change", function () { if (campo.files.length) campo.form.submit(); });
  });

  // Listas de selección múltiple: filtro y contador. Filtrar solo oculta filas; lo marcado se conserva.
  function sinTildes(texto) { return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); }

  document.querySelectorAll("[data-seleccion]").forEach(function (caja) {
    var filtro = caja.querySelector("[data-seleccion-filtro]");
    var sinResultados = caja.querySelector("[data-seleccion-sin-resultados]");
    var contador = caja.querySelector("[data-seleccion-total]");
    var opciones = Array.prototype.slice.call(caja.querySelectorAll(".seleccion-opcion"));

    function contar() {
      var n = caja.querySelectorAll("input[type=checkbox]:checked").length;
      contador.textContent = n ? n + (n === 1 ? " seleccionado" : " seleccionados") : "Ninguno seleccionado";
    }
    caja.addEventListener("change", contar);
    contar();

    if (!filtro) return;
    filtro.hidden = false;
    filtro.addEventListener("keydown", function (evento) { if (evento.key === "Enter") evento.preventDefault(); });
    filtro.addEventListener("input", function () {
      var texto = sinTildes(filtro.value.trim());
      var visibles = 0;
      opciones.forEach(function (opcion) {
        var coincide = sinTildes(opcion.textContent).indexOf(texto) !== -1;
        opcion.hidden = !coincide;
        if (coincide) visibles++;
      });
      sinResultados.hidden = visibles > 0;
    });
  });

  // Resumen de la asignación múltiple: cada plan se aplica a cada elemento.
  document.querySelectorAll("[data-lote-resumen]").forEach(function (resumen) {
    var form = resumen.closest("form");
    function marcados(nombre) { return form.querySelectorAll('input[name="' + nombre + '"]:checked').length; }
    function plural(n, singular, varios) { return n + " " + (n === 1 ? singular : varios); }

    function actualizar() {
      var elementos = marcados("materiales"), planes = marcados("planes"), bomberos = marcados("responsables");
      resumen.hidden = !(elementos && planes && bomberos);
      resumen.textContent = "Se crearán " + plural(elementos * planes, "asignación", "asignaciones") + ": " +
        plural(elementos, "elemento", "elementos") + " × " + plural(planes, "plan", "planes") + ", a cargo de " +
        plural(bomberos, "bombero", "bomberos") + ".";
    }
    form.addEventListener("change", actualizar);
    actualizar();
  });
  // Borradores: lo escrito en un formulario queda en este dispositivo hasta enviarlo. Si el bombero sale
  // de la página, recibe una llamada o el celular recarga la pestaña, al volver lo encuentra.
  var Borradores = (function () {
    var usuario = document.body.getAttribute("data-usuario");
    var almacen = null;
    try { almacen = window.localStorage; almacen.setItem("sirema-prueba", "1"); almacen.removeItem("sirema-prueba"); }
    catch (e) { almacen = null; }
    if (!usuario || !almacen) return null;
    var prefijo = "sirema-borrador-" + usuario + "-";
    var vigencia = 7 * 24 * 60 * 60 * 1000;
    var saliendo = false;

    function leer(clave) {
      try {
        var dato = JSON.parse(almacen.getItem(clave));
        return dato && Date.now() - dato.t < vigencia ? dato.v : null;
      } catch (e) { return null; }
    }
    function guardar(clave, valor) {
      if (saliendo) return;
      try { almacen.setItem(clave, JSON.stringify({ t: Date.now(), v: valor })); } catch (e) { /* sin espacio */ }
    }
    function borrar(clave) { try { almacen.removeItem(clave); } catch (e) { /* sin almacenamiento */ } }
    function borrarTodos() {
      saliendo = true;
      Object.keys(almacen).forEach(function (k) { if (k.indexOf(prefijo) === 0) borrar(k); });
    }
    function aviso(alDescartar) {
      var caja = document.createElement("div");
      caja.className = "aviso-inline mb-3";
      caja.setAttribute("role", "status");
      caja.textContent = "Se recuperó lo que había escrito. ";
      if (alDescartar) {
        var boton = document.createElement("button");
        boton.type = "button";
        boton.className = "btn btn-link btn-sm p-0 align-baseline";
        boton.textContent = "Descartar";
        boton.addEventListener("click", function () { alDescartar(); caja.remove(); });
        caja.appendChild(boton);
      }
      return caja;
    }
    // Quita los borradores vencidos de cualquier usuario.
    Object.keys(almacen).forEach(function (k) { if (k.indexOf("sirema-borrador-") === 0 && !leer(k)) borrar(k); });
    return { clave: function (sufijo) { return prefijo + sufijo; }, leer: leer, guardar: guardar, borrar: borrar,
             borrarTodos: borrarTodos, aviso: aviso };
  })();
  window.SiremaBorradores = Borradores;

  if (Borradores) {
    var NO_SE_GUARDAN = ["hidden", "password", "file", "submit", "button", "reset", "image"];

    var camposDe = function (form) {
      return Array.prototype.filter.call(form.elements, function (c) {
        return c.name && c.name !== "csrfmiddlewaretoken" && !c.disabled && NO_SE_GUARDAN.indexOf(c.type) === -1;
      });
    };
    var valoresDe = function (form) {
      var datos = {};
      camposDe(form).forEach(function (c) {
        if (c.type === "checkbox") {
          datos[c.name] = datos[c.name] || [];
          if (c.checked) datos[c.name].push(c.value);
        } else if (c.type === "radio") {
          if (!(c.name in datos)) datos[c.name] = "";
          if (c.checked) datos[c.name] = c.value;
        } else if (c.type === "select-multiple") {
          datos[c.name] = Array.prototype.filter.call(c.options, function (o) { return o.selected; })
            .map(function (o) { return o.value; });
        } else {
          datos[c.name] = c.value;
        }
      });
      return datos;
    };
    var aplicarA = function (form, datos) {
      camposDe(form).forEach(function (c) {
        if (!(c.name in datos)) return;
        var v = datos[c.name];
        if (c.type === "checkbox") c.checked = v.indexOf(c.value) !== -1;
        else if (c.type === "radio") c.checked = c.value === v;
        else if (c.type === "select-multiple") Array.prototype.forEach.call(c.options, function (o) { o.selected = v.indexOf(o.value) !== -1; });
        else c.value = v;
        c.dispatchEvent(new Event("change", { bubbles: true }));
      });
    };

    Array.prototype.filter.call(document.querySelectorAll("form"), function (form) {
      return form.method === "post" && !form.hasAttribute("data-sin-borrador") &&
        !form.querySelector("input[type=password], input[type=file]") && camposDe(form).length > 0;
    }).forEach(function (form, indice) {
      var clave = Borradores.clave(location.pathname + "#" + indice);
      var inicial = JSON.stringify(valoresDe(form));
      var temporizador;
      form.setAttribute("data-borrador", clave);

      function guardar() {
        clearTimeout(temporizador);
        if (form.hasAttribute("data-enviado")) return;
        var actual = JSON.stringify(valoresDe(form));
        if (actual === inicial) Borradores.borrar(clave);
        else Borradores.guardar(clave, JSON.parse(actual));
      }
      function programar() { clearTimeout(temporizador); temporizador = setTimeout(guardar, 300); }

      var guardado = Borradores.leer(clave);
      if (guardado && JSON.stringify(guardado) !== inicial) {
        var original = JSON.parse(inicial);
        aplicarA(form, guardado);
        form.insertBefore(Borradores.aviso(function () { aplicarA(form, original); Borradores.borrar(clave); }),
                          form.firstChild);
      }
      form.addEventListener("input", programar);
      form.addEventListener("change", programar);
      window.addEventListener("pagehide", guardar);
      document.addEventListener("visibilitychange", function () { if (document.visibilityState === "hidden") guardar(); });
    });

    // Al enviar se descarta el borrador, salvo sin conexión. Al cerrar sesión se borran todos los del usuario.
    document.addEventListener("submit", function (evento) {
      if (evento.defaultPrevented) return;
      var form = evento.target;
      if ((form.getAttribute("action") || "").indexOf("/accesos/salir/") !== -1) { Borradores.borrarTodos(); return; }
      var clave = form.getAttribute("data-borrador");
      if (clave && navigator.onLine !== false) {
        form.setAttribute("data-enviado", "1");
        Borradores.borrar(clave);
      }
    });
  }
})();
