# Manual de usuario · SIREMA

SIREMA se usa desde el navegador del celular o del computador, conectado a la red del cuartel.
Ingrese con su **correo** y **contraseña**. Si la olvida, el administrador le asigna una nueva
(no hay recuperación por correo). Tras 5 intentos fallidos la cuenta se bloquea 15 minutos, y la
sesión se cierra sola tras 30 minutos sin actividad.

## Bombero

**Mis revisiones** (menú *Revisiones*). Lista sus revisiones ordenadas por urgencia, con tres pestañas:
*Pendientes*, *Vencidas* y *Realizadas*. Rojo significa vencida y ámbar que vence hoy o mañana.

**Ejecutar una revisión.**
1. Toque la revisión. Aparecen el equipo, su ubicación y los puntos de control del plan.
2. En cada punto, ingrese el valor (si lo pide) y toque **Conforme**, **Observ.** o **Falla**.
   Cada respuesta se guarda al instante: verá «Guardado» arriba a la derecha.
3. Si elige Observación o Falla, escriba un comentario: sin él la respuesta no se guarda.
4. Si un valor queda fuera del rango aceptable, el sistema se lo advierte y sugiere marcar Falla.
5. Use **Tomar fotografía** cuando el punto o el plan la exijan. La cámara se abre sola.
6. Si se corta la señal, siga respondiendo: las respuestas se envían al recuperar la conexión.
7. Cuando el botón **Finalizar revisión** se active, tóquelo. Si hubo alguna falla, describa el
   hallazgo y su criticidad. La jefatura será notificada.

Una revisión finalizada no se puede modificar.

**Inventario.** Busque por nombre o código (desde 2 caracteres) y filtre por unidad, cajonera,
categoría o estado. En la ficha de cada elemento verá su historial completo. Con **Trasladar**
registra un cambio de ubicación.

**Avisos.** La campana muestra las notificaciones sin leer: revisiones asignadas, recordatorios 24 horas
antes de la fecha límite y vencimientos. Al abrir un aviso queda marcado como leído.

## Jefatura

Además de lo anterior:

- **Panel de cumplimiento**: % de cumplimiento del período (revisiones en plazo / revisiones con fecha
  límite en el período), revisiones vencidas, hallazgos abiertos y elementos sin plan. Se filtra por
  período, unidad y categoría, y se exporta a PDF, XLSX o CSV.
- **Inventario**: registrar material (o cargar una planilla CSV/XLSX), modificar fichas y dar de baja.
  El código institucional es único y no se reutiliza, aunque el elemento esté dado de baja.
- **Planes de revisión**: defina qué se controla (puntos de control), cada cuánto y con cuántos días de
  tolerancia. Si modifica un plan con revisiones ya ejecutadas, el sistema crea una versión nueva.
- **Asignaciones**: busque el elemento, elija el plan, el bombero responsable y la fecha de la primera
  revisión. El programador genera las siguientes de forma automática.
- **Revisiones**: consulte todas las revisiones y reasigne el responsable de una revisión abierta.
- **Hallazgos**: márquelos *en reparación* y ciérrelos registrando la acción tomada.
- **Fotografías**: puede anular una foto indicando el motivo. No se elimina: queda en la bitácora.

## Administrador

- **Usuarios**: crear cuentas (RUT, nombre, correo, rol), editar, asignar rol, desactivar o reactivar y
  restablecer contraseñas. No se puede desactivar al único administrador activo.
- **Permisos por rol**: matriz de permisos de Bombero, Jefatura y Administrador.
- **Unidades y cajoneras** y **Categorías**: catálogos del inventario. No se eliminan si tienen elementos.
- **Bitácora**: registro inalterable de altas, modificaciones, bajas, movimientos, revisiones, cambios de
  permisos, anulaciones e inicios de sesión, filtrable por usuario, acción, entidad y fechas.
