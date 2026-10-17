# SIREMA

Sistema web para el control de mantenciones y revisiones periódicas del material menor de la
**Octava Compañía del Cuerpo de Bomberos de Talcahuano**.
Proyecto APT Capstone · Duoc UC, Sede San Andrés · APT122 sección 004D · Grupo 1.

Implementa la ERS v1.0 (RF-01 a RF-12, RNF-01 a RNF-11) y la arquitectura del DAS v1.0: monolito
modular en capas con **Django 5.2**, **PostgreSQL 16**, **Bootstrap 5** servido localmente y
**Docker Compose** con cuatro contenedores. Funciona en la red del cuartel sin internet.

## Estructura del repositorio

```
config/       configuración (settings base, desarrollo y producción) y URL raíz
nucleo/       almacenamiento de fotografías (SHA-256), tipos enumerados, utilidades
accesos/      usuarios, roles, permisos, autenticación y bitácora inmutable
inventario/   unidades, cajoneras, categorías, material, movimientos, bajas, carga masiva
revisiones/   planes, puntos de control, asignaciones, revisiones, fotos, hallazgos,
              notificaciones, programador de tareas y API JSON de ejecución
reportes/     panel de cumplimiento y exportación PDF / XLSX / CSV
templates/    plantilla base, componentes y páginas de error
static/       CSS y JS propios; Bootstrap 5 y Bootstrap Icons en static/vendor (sin CDN)
docker/       Dockerfile, nginx.conf, crontab, entrypoint y script del certificado TLS
docs/         openapi.yaml (API JSON) y manual de usuario
```

Regla de dependencias (DAS 4.3.5): `reportes → revisiones → inventario → accesos → nucleo`.
Inventario no importa revisiones: la baja de un elemento se avisa con la señal
`material_dado_de_baja`, y el historial de la ficha recibe las revisiones mediante
`inventario/registro.py` (patrón observador).

## 1. Ejecutar en un computador de desarrollo (Windows, Linux o macOS)

Requisitos: Python 3.12. Sin PostgreSQL, el proyecto usa SQLite para desarrollo.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows   (Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py runserver
```

Abra http://127.0.0.1:8000.

### Usuarios de demostración

Los crea `python manage.py cargar_datos_demo`. Son datos **ficticios**, solo para desarrollo y la
presentación (definidos en `accesos/demo.py`). Con `DEBUG` activo, la pantalla de inicio de sesión
también los muestra: basta tocar un correo para completar el formulario.

| Correo | Contraseña | Rol |
|---|---|---|
| `admin@sirema.local` | `Bomberos2026` | Administrador |
| `jefatura@sirema.local` | `Bomberos2026` | Jefatura |
| `j.soto@sirema.local` | `Bomberos2026` | Bombero |
| `m.rivas@sirema.local` | `Bomberos2026` | Bombero |
| `p.lagos@sirema.local` | `Bomberos2026` | Bombero |

Si una cuenta queda bloqueada por 5 intentos fallidos, desbloquéela con `python manage.py axes_reset`.

Para partir desde cero, borre `db.sqlite3` y la carpeta `media/`, y repita `migrate` y `cargar_datos_demo`.
En Windows la exportación PDF abre una vista lista para imprimir («Guardar como PDF»), porque WeasyPrint
necesita bibliotecas de Linux. En el contenedor Docker el PDF se descarga directamente.

### Usar PostgreSQL en desarrollo

La aplicación usa PostgreSQL cuando existe la variable `POSTGRES_DB`. La forma más simple es levantar solo
la base de datos con Docker:

```bash
docker run -d --name sirema-pg -e POSTGRES_DB=sirema -e POSTGRES_USER=sirema -e POSTGRES_PASSWORD=sirema -p 5432:5432 postgres:16
```

Luego, en la misma terminal donde ejecutará Django (PowerShell):

```powershell
$env:POSTGRES_DB="sirema"; $env:POSTGRES_USER="sirema"; $env:POSTGRES_PASSWORD="sirema"; $env:POSTGRES_HOST="localhost"
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py runserver
```

También puede instalar PostgreSQL 16 para Windows desde postgresql.org, crear la base `sirema` y el
usuario `sirema` con pgAdmin, y definir las mismas variables.

## 2. Instalar en el servidor del cuartel (Docker Compose)

Requisitos: Docker Engine y Docker Compose. Internet solo se necesita para construir la imagen. En el
cuartel puede cargarse con `docker save` / `docker load`.

```bash
cp .env.example .env                                  # edite TODAS las claves
sh docker/generar_certificado.sh sirema.local 192.168.1.10
docker compose build
docker compose up -d
docker compose ps                                     # los 4 contenedores deben quedar «healthy»
```

Para probar en un computador con datos de demostración (nunca en el cuartel):

```bash
docker compose exec sirema-web python manage.py cargar_datos_demo
```

Luego abra https://localhost y acepte la advertencia del certificado autofirmado. En este modo la pantalla de
ingreso no muestra los usuarios de prueba: están en la sección «Usuarios de demostración».
`docker compose down` detiene los contenedores y conserva los datos; `docker compose down -v` los borra.

| Contenedor | Imagen | Función |
|---|---|---|
| `sirema-proxy` | nginx:1.27-alpine | HTTPS (443, y 80 que redirige), estáticos, fotos con X-Accel-Redirect |
| `sirema-web` | sirema-web:0.9.0 | Django + Gunicorn (puerto 8000 interno); migra y crea el primer administrador |
| `sirema-scheduler` | sirema-web:0.9.0 | cron: `generar_revisiones` 05:30, `emitir_avisos` cada hora, `respaldo_diario` 03:00 |
| `sirema-db` | postgres:16 | Base de datos (puerto 5432 solo interno) |

Volúmenes: `pgdata`, `media` (fotografías), `static` y `respaldos`. Todos los servicios usan
`restart: unless-stopped` y comprobaciones de salud, así que vuelven solos tras un corte de luz (RNF-03).
Al arrancar, el programador recupera las revisiones de los días que el servidor estuvo apagado.

Instale `docker/certs/sirema.crt` como certificado de confianza en los celulares y computadores de la
compañía, y acceda a `https://sirema.local` (o a la IP del servidor).

### Respaldos y restauración (RNF-05)

`respaldo_diario` guarda cada día `sirema.dump` (pg_dump) y `media.tar.gz` en el volumen `respaldos`.
Conserva 30 diarios y 12 mensuales. Para la copia semanal externa, copie la carpeta más reciente a un disco:

```bash
docker compose cp sirema-scheduler:/respaldos/diarios /ruta/al/disco/sirema-$(date +%Y%m%d)
```

Restauración:

```bash
docker compose cp respaldo/sirema.dump sirema-db:/tmp/sirema.dump
docker compose exec sirema-db pg_restore -U sirema -d sirema --clean --if-exists /tmp/sirema.dump
docker compose cp respaldo/media.tar.gz sirema-web:/tmp/media.tar.gz
docker compose exec sirema-web tar -xzf /tmp/media.tar.gz -C /
```

## 3. Pruebas automatizadas (RNF-07)

```bash
pytest --cov=accesos --cov=inventario --cov=revisiones --cov=reportes --cov=nucleo
```

80 pruebas organizadas por caso de prueba del ERS (CP-01 a CP-12). Cobertura actual: 74 % global y
79–96 % en servicios, modelos, programador e indicadores. GitHub Actions (`.github/workflows/sirema-pruebas.yml`, en la raíz del repositorio)
las ejecuta sobre PostgreSQL 16 y exige al menos 70 %.

## 4. Trazabilidad de requisitos

| Requisito | Implementación |
|---|---|
| RF-01 Gestión de usuarios | `accesos/views.py` (Usuario*), `accesos/forms.py`; RUT y correo únicos, único administrador protegido |
| RF-02 Autenticación y roles | Argon2, django-axes (5 intentos / 15 min), `LoginRequiredMiddleware`, `accesos/permisos.py`, matriz rol-permiso |
| RF-03 Material | `inventario/services.py`, `Material.dar_de_baja`, `inventario/importacion.py` (CSV/XLSX) |
| RF-04 Código único | índice único parcial `uq_material_codigo_institucional` + `services.verificar_codigo` |
| RF-05 Búsqueda | `MaterialQuerySet.buscar`, `FiltroMaterial` (desde 2 caracteres, filtros combinados) |
| RF-06 Movimientos | `Material.trasladar` (movimiento + ubicación en una transacción) |
| RF-07 Planes | `revisiones/services.py` (`guardar_plan` con versiones, `asignar_plan`), `programador.py` |
| RF-08 Ejecución | `services.registrar_resultado` / `finalizar`, `api.py`, `static/js/revision.js` (autoguardado y cola local) |
| RF-09 Notificaciones y panel | `programador.emitir_avisos`, `revisiones/notificaciones.py`, `reportes/indicadores.py` |
| RF-10 Historial, reportes, bitácora | ficha del elemento, `reportes/exportacion.py`, `accesos/auditoria.py` |
| RF-11 Evidencia fotográfica | `nucleo/almacenamiento.py` (SHA-256, 1 MB), `services.adjuntar_fotografia` / `anular_fotografia` |
| RF-12 Hallazgos | `services.finalizar` (hallazgo obligatorio si hay falla), `cerrar_hallazgo` |
| RNF-01 Usabilidad | mobile-first desde 360 px, botones de 48 px o más, un toque por resultado, contraste AA |
| RNF-08 Integridad | claves foráneas, CHECK por cada enumerado, `transaction.atomic`, `select_for_update` |
| RNF-09 Auditoría | `evento_auditoria` con valores anterior y nuevo; disparador que rechaza UPDATE/DELETE |
| RNF-10 Español | `es-cl`, fechas dd-mm-aaaa, zona `America/Santiago` |

### Decisiones de implementación respecto del modelo de datos

- Las 19 tablas y sus columnas conservan los nombres del modelo relacional (`db_table` y `db_column`).
- Los tipos enumerados se implementan como `varchar` con una restricción CHECK por columna: la misma
  garantía de integridad que un ENUM de PostgreSQL, compatible con las migraciones de Django.
- `rol_permiso` y `resultado_punto` usan clave primaria compuesta (`CompositePrimaryKey` de Django 5.2).
  La clave foránea compuesta `fotografia → resultado_punto` se crea con SQL en PostgreSQL
  (`revisiones/migrations/0002`).
- Se agregó `UNIQUE (id_asignacion, fecha_programada)` en `revision` y el usuario técnico «sistema»
  (DAS 4.2.5).

Versión del software: **0.9.0** (versión candidata para pruebas de aceptación, DAS 9.2).
