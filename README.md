# SIREMA

**Sistema de Revisiones y Mantenciones**

Aplicación web para el control de las mantenciones y revisiones periódicas del material menor de la Octava Compañía del Cuerpo de Bomberos de Talcahuano.

Proyecto APT desarrollado en la asignatura Capstone, Ingeniería en Informática, Duoc UC Sede San Andrés.

---

## Descripción

La Octava Compañía opera equipos delicados y críticos, como motores de combustión, equipos de medición de gases y herramientas hidráulicas de rescate. Por norma y por seguridad, esos equipos deben revisarse periódicamente: encenderlos, medir su estado, verificar niveles y dejar constancia del resultado.

Hoy esas revisiones se realizan de memoria o en papel. No existe un calendario, no queda registro de quién revisó ni con qué resultado, y una falla puede descubrirse recién durante la emergencia.

SIREMA convierte esa práctica informal en un proceso controlado. Define para cada equipo un plan de revisión con su frecuencia, lo asigna a un bombero responsable y lo ejecuta como una lista de verificación con resultado, valores medidos y observaciones. El sistema conserva el historial completo, avisa lo pendiente o vencido y entrega a la jefatura un panel con el estado real del material.

El aporte de valor es que la jefatura pueda conocer el estado real de cada equipo antes de que ocurra la emergencia, y que cada revisión quede asociada a un equipo identificable y a un responsable.

---

## A quién va dirigido

| Usuario | Qué hace en el sistema |
|---|---|
| Bombero | Ejecuta las revisiones asignadas desde el celular, junto al carro, consulta el inventario y registra traslados. |
| Jefatura | Administra el material, define y asigna los planes de revisión, da seguimiento a los hallazgos y consulta el panel y los reportes. |
| Administrador | Gestiona usuarios, permisos por rol y catálogos, y consulta la bitácora de auditoría. |

---

## Alcance

**Incluye**

- Gestión de usuarios con rol asignado y restricción de funciones según ese rol.
- Inventario del material menor, con código institucional único por elemento.
- Registro de la ubicación en carro y cajonera, y de los movimientos entre ellas.
- Búsqueda y filtros por nombre, código, ubicación, categoría y estado.
- Definición de planes de revisión por frecuencia y su asignación a bomberos.
- Ejecución de la revisión como lista de verificación con resultado, valores medidos y observaciones.
- Notificaciones de revisiones pendientes o vencidas.
- Panel de indicadores de cumplimiento, historial por equipo y reportes exportables.
- Bitácora de auditoría de toda acción relevante.

**No incluye**

- Material mayor y vehículos.
- Integración con sistemas externos.
- Aplicación móvil nativa.

---

## Arquitectura de la solución

El sistema se despliega en un servidor local dentro del cuartel y opera sobre la red interna, sin requerir conexión permanente a internet. Los usuarios acceden desde el navegador de sus celulares o computadores conectados a esa misma red.

La solución se ejecuta en contenedores, separando el servidor web, la aplicación y la base de datos. Los datos residen en un volumen persistente, de modo que sobreviven a la recreación de los contenedores y a los reinicios del equipo. El servidor está configurado para levantar los servicios de forma automática al arrancar, y se contemplan respaldos periódicos de la base de datos con procedimiento de restauración verificado.

La aplicación se organiza en cuatro módulos de dominio construidos sobre un modelo de datos común:

| Módulo | Responsabilidad |
|---|---|
| Accesos | Usuarios, roles, autenticación, control de permisos y bitácora de auditoría. |
| Inventario | Material menor, código institucional único, ubicaciones y movimientos. |
| Revisiones | Planes de revisión, asignación de responsables, ejecución con registro de resultados, fotografías, hallazgos y notificaciones. |
| Reportes | Panel de cumplimiento y exportación de reportes. |

Cada revisión queda enlazada a un equipo registrado en el inventario y a un responsable, lo que sostiene la trazabilidad completa del material.

---

## Ejecución del proyecto

La aplicación está en la carpeta `Sirema Web`. Su [README](Sirema%20Web/README.md) explica las dos formas de ejecutarla:

- **Computador de desarrollo:** con Python 3.12 y SQLite, sin Docker.
- **Servidor del cuartel:** con Docker Compose, en cuatro contenedores (proxy, web, programador y base de datos), incluyendo el procedimiento de respaldo y restauración.

Una vez instalado, el sistema queda disponible para todos los dispositivos conectados a la red del cuartel a través de la dirección del servidor.

---

## Equipo

| Integrante | Rol | Responsabilidades |
|---|---|---|
| **Renato Pomeri Navarrete** | Jefe de proyecto y analista de requisitos | Planificación y control del avance, relación con la contraparte, levantamiento y especificación de requerimientos, coordinación de la implantación y capacitación en el cuartel. |
| **Fernando Molina Figueroa** | Arquitecto de datos y desarrollador back end | Diseño e implementación del modelo de datos, lógica de negocio de los módulos de inventario y revisiones, seguridad de acceso, respaldos y su restauración. |
| **Fabián Fica Villagra** | Desarrollador front end y encargado de calidad | Diseño de interfaces y del prototipo, construcción de las vistas responsivas y del panel de indicadores, elaboración y ejecución del plan de pruebas y seguimiento de los hallazgos. |

---

## Metodología de trabajo

El proyecto se desarrolla con una **metodología tradicional en cascada**, en la que cada etapa se cierra con un producto documentado y validado antes de iniciar la siguiente.

La elección responde a las características del encargo: los requerimientos derivan de normas y prácticas de revisión estables en el tiempo, la contraparte tiene disponibilidad acotada y necesita validar documentos concretos en instancias puntuales, y el plazo de la asignatura es fijo.

| Etapa | Producto que la cierra |
|---|---|
| 1. Levantamiento de requerimientos | Acta de levantamiento con el proceso actual documentado |
| 2. Análisis y especificación | Documento de requerimientos validado por la contraparte |
| 3. Diseño | Documento de diseño con arquitectura, modelo de datos y diagramas UML |
| 4. Construcción | Sistema funcional con el código versionado en este repositorio |
| 5. Pruebas | Plan de pruebas con sus evidencias de ejecución |
| 6. Implantación y cierre | Sistema en operación, manual técnico y acta de entrega |

El trabajo se coordina mediante ramas por funcionalidad y revisión cruzada antes de integrar a la rama principal.

---

## Planificación

| Fase | Semanas | Contenido |
|---|---|---|
| Fase 1 | 1 a 4 | Definición del proyecto, levantamiento y especificación de requisitos |
| Fase 2 | 5 a 15 | Diseño, construcción de los módulos, pruebas, despliegue y documentación |
| Fase 3 | 16 a 18 | Presentación del proyecto ante la comisión evaluadora |

Hitos de entrega: definición del proyecto en la semana 4, informe de avance en la semana 10 e informe final en la semana 15.

---

## Estructura del repositorio

- **Documentacion**: especificación de requerimientos (ERS), documento de arquitectura (DAS), casos de uso y modelo de datos.
- **Fase 1**: evidencias grupales e individuales de la definición del proyecto.
- **Fase 2**: evidencias grupales e individuales del desarrollo del proyecto.
- **Sirema Web**: código fuente de la aplicación, organizado por módulos de dominio, con sus pruebas y archivos de despliegue.
- **.github/workflows**: ejecución automática de las pruebas.

---

## Tecnologías utilizadas

- **Python 3.12** y **Django 5.2**
- **PostgreSQL 16**
- **HTML** y **Bootstrap 5**
- **Docker Compose** y **Nginx**

---

## Estado del proyecto

Versión 0.9.0, candidata para pruebas de aceptación. La aplicación implementa los módulos de accesos, inventario, revisiones y reportes.

---

## Contexto académico

Este repositorio corresponde a un proyecto de titulación de Duoc UC y su uso es académico. El sistema se desarrolla para la Octava Compañía del Cuerpo de Bomberos de Talcahuano, que participa como contraparte del proyecto.
