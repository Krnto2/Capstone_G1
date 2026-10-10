/* SIREMA · edición de los puntos de control de un plan (CU-C2). */
(function () {
  "use strict";
  var lista = document.getElementById("lista-puntos");
  var plantilla = document.getElementById("plantilla-punto");
  var total = document.getElementById("id_puntos-TOTAL_FORMS");
  if (!lista || !plantilla || !total) return;

  function filasVisibles() {
    return Array.prototype.filter.call(lista.querySelectorAll("[data-fila-punto]"), function (f) { return !f.hidden; });
  }

  function numerar() {
    filasVisibles().forEach(function (fila, i) {
      fila.querySelector("[data-numero]").textContent = i + 1;
      var orden = fila.querySelector("input[name$='-ORDER']");
      if (orden) orden.value = i + 1;
    });
  }

  function alternarNumericos(fila) {
    var tipo = fila.querySelector("select[name$='-tipo_dato']");
    if (!tipo) return;
    var esNumerico = tipo.value === "numerico";
    fila.querySelectorAll("[data-solo-numerico]").forEach(function (b) { b.hidden = !esNumerico; });
  }

  function preparar(fila) {
    alternarNumericos(fila);
    var tipo = fila.querySelector("select[name$='-tipo_dato']");
    if (tipo) tipo.addEventListener("change", function () { alternarNumericos(fila); });
    fila.querySelector("[data-quitar]").addEventListener("change", function (e) {
      if (filasVisibles().length <= 1) { e.target.checked = false; alert("El plan debe tener al menos un punto de control."); return; }
      fila.hidden = true;
      numerar();
    });
    fila.querySelector("[data-subir]").addEventListener("click", function () {
      var anterior = fila.previousElementSibling;
      while (anterior && anterior.hidden) anterior = anterior.previousElementSibling;
      if (anterior) { lista.insertBefore(fila, anterior); numerar(); }
    });
    fila.querySelector("[data-bajar]").addEventListener("click", function () {
      var siguiente = fila.nextElementSibling;
      while (siguiente && siguiente.hidden) siguiente = siguiente.nextElementSibling;
      if (siguiente) { lista.insertBefore(siguiente, fila); numerar(); }
    });
    if (fila.querySelector("[data-quitar]").checked) fila.hidden = true;
  }

  document.querySelector("[data-agregar-punto]").addEventListener("click", function () {
    var indice = parseInt(total.value, 10);
    var html = plantilla.innerHTML.replace(/__prefix__/g, indice);
    var contenedor = document.createElement("div");
    contenedor.innerHTML = html.trim();
    var fila = contenedor.firstElementChild;
    lista.appendChild(fila);
    total.value = indice + 1;
    preparar(fila);
    numerar();
    fila.querySelector("input[name$='-descripcion']").focus();
  });

  lista.querySelectorAll("[data-fila-punto]").forEach(preparar);
  numerar();
  document.getElementById("form-plan").addEventListener("submit", numerar);
})();
